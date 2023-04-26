from sqlalchemy.orm import Session
from fastapi import Depends
from db.schemas import AccountUpdate, AccountCreate
from db.models import Account
from .base import BaseService
from db.session import get_session


class AccountsService(BaseService[Account, AccountCreate, AccountUpdate]):
    def __init__(self, db_session: Session):
        super(AccountsService, self).__init__(Account, db_session)


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
