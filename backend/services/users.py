from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import Depends, UploadFile
from db.schemas.users import UserUpdate, UserCreate
from db.models import User
from .base import BaseService
from db.session import get_session
from starlette.exceptions import HTTPException
import sqlalchemy
from utils import get_password_hash
from datetime import datetime
from firebase import bucket


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db_session: Session):
        super(UserService, self).__init__(User, db_session)

    def search(self, term: str):
        return self.db_session.query(User).filter(User.username.like(f"%{term}%"))

    def create(self, obj: UserCreate):
        db_obj: User = User(
            username=obj.username,
            email=obj.email,
            password=get_password_hash(obj.password)
        )
        print(f"converted to User model : ${db_obj}")
        self.db_session.add(db_obj)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        print("End create")

    def update(self, id, obj: UserUpdate, pfp: UploadFile):
        # if not os.path.exists("static/profile_pictures"):
        #     os.makedirs("static/profile_pictures")

        # with open(f"static/profile_pictures/{pfp.filename}", "wb") as f:
        #     f.write(pfp.file.read())

        blob = bucket.blob(f"profile_pictures/{pfp.filename}")
        blob.upload_from_file(pfp.file, content_type="image/png")
        blob.make_public()

        stmt = (
            update(User)
            .where(User.id == id)
            .values(
                username=obj.username,
                email=obj.email,
                password=get_password_hash(obj.password),
                profile_picture=blob.public_url
            )
        )
        print(stmt)

        self.db_session.execute(stmt)
        self.db_session.commit()


def get_service(db_session: Session = Depends(get_session)) -> UserService:
    return UserService(db_session)
