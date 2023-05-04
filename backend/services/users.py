from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import Depends, UploadFile
from db.schemas import UserUpdate, UserCreate
from db.models import User
from .base import BaseService
from db.session import get_session
from starlette.exceptions import HTTPException
import sqlalchemy
from utils import get_password_hash
from datetime import datetime
import json


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db_session: Session):
        super(UserService, self).__init__(User, db_session)

    def create(self, obj: UserCreate):
        db_obj: User = User(
            username=obj.username,
            email=obj.email,
            password=get_password_hash(obj.password),
            creation_date=datetime.now()
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
        return db_obj

    def update(self, id, obj: UserUpdate, pfp: UploadFile):
        with open(f"static/profile_pictures/{pfp.filename}", "wb") as f:
            f.write(pfp.file.read())
        # print(pfp.file.read())
        stmt = (
            update(User)
            .where(User.id == id)
            .values(
                username=obj.username,
                email=obj.email,
                password=get_password_hash(obj.password),
                profil_picture=pfp.filename
            )
        )
        print(stmt)

        self.db_session.execute(stmt)
        self.db_session.commit()


def get_user_service(db_session: Session = Depends(get_session)) -> UserService:
    return UserService(db_session)
