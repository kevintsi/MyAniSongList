from io import BytesIO

import sqlalchemy
from app.db.models import User
from app.db.schemas.users import UserCreate, UserUpdate
from app.db.session import get_session
from app.firebase import bucket
from app.utils import get_password_hash
from fastapi import Depends, UploadFile, status
from PIL import Image
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from .base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db_session: Session):
        super(UserService, self).__init__(User, db_session)

    def search(self, term: str):
        stmt = select(User).filter(User.username.like(f"%{term}%"))
        return stmt

    def create(self, obj: UserCreate):
        db_obj: User = User(
            username=obj.username,
            email=obj.email,
            password=get_password_hash(obj.password),
        )
        print(f"converted to User model : ${db_obj}")
        self.db_session.add(db_obj)
        try:
            self.db_session.commit()
            return db_obj
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error",
                )
            else:
                raise e

    def update(self, id, obj: UserUpdate, pfp: UploadFile):

        user: User | None = self.db_session.get(User, id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if pfp:
            image = Image.open(BytesIO(pfp.file.read()))
            print(f"Image : {image}")
            webp_buffer = BytesIO()
            image.save(webp_buffer, format="WEBP", quality=100)
            webp_buffer.seek(0)
            filename = pfp.filename.rsplit(".", 1)[0] + ".webp"
            blob = bucket.blob(f"profile_pictures/{filename}")
            blob.upload_from_file(webp_buffer, content_type="image/webp")
            blob.make_public()
            user.profile_picture = blob.public_url

        for col, value in obj.dict(exclude_unset=True).items():
            if col == "password":
                setattr(user, col, get_password_hash(value))
            else:
                setattr(user, col, value)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error",
                )
            else:
                raise e

        return user


def get_service(db_session: Session = Depends(get_session)) -> UserService:
    return UserService(db_session)
