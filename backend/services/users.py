from sqlalchemy.orm import Session
from fastapi import Depends
from db.schemas import UserUpdate, UserCreate
from db.models import User
from .base import BaseService
from db.session import get_session
from starlette.exceptions import HTTPException
import sqlalchemy
from utils import get_password_hash
from datetime import datetime


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


def get_user_service(db_session: Session = Depends(get_session)) -> UserService:
    return UserService(db_session)
