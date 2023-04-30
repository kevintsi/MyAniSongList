from sqlalchemy.orm import Session
from fastapi import Depends
from db.schemas import AccountUpdate, AccountCreate
from db.models import Account
from .base import BaseService
from db.session import get_session
from starlette.exceptions import HTTPException
import sqlalchemy
from utils import get_password_hash
from datetime import datetime


class AccountsService(BaseService[Account, AccountCreate, AccountUpdate]):
    def __init__(self, db_session: Session):
        super(AccountsService, self).__init__(Account, db_session)

    def create(self, obj: AccountCreate):
        db_obj: Account = Account(
            username=obj.username,
            email=obj.email,
            password=get_password_hash(obj.password),
            creation_date=datetime.now()
        )
        print(f"converted to Account model : ${db_obj}")
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


def get_accounts_service(db_session: Session = Depends(get_session)) -> AccountsService:
    return AccountsService(db_session)


# def create_user(db: Session, user: schemas.AccountCreate):
#     hashed_password = str.encode(user.password)
#     user.password = bcrypt.hashpw(hashed_password, bcrypt.gensalt())
#     db_user = models.Account(
#         email=user.email,
#         password=user.password,
#         username=user.username,
#         creation_date=datetime.now()
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def update_user(db: Session, user: schemas.AccountUpdate):
#     hashed_password = str.encode(user.password)
#     user.password = bcrypt.hashpw(hashed_password, bcrypt.gensalt())
#     db_user = models.Account(
#         email=user.email,
#         password=user.password,
#         username=user.username,
#         creation_date=datetime.now()
#     )
#     (db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
