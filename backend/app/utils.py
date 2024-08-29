from datetime import datetime, timedelta
from os import getenv

import jwt
from app.db.models import User
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db_session: Session, email: str):
    try:
        res = db_session.scalars(
            select(User).filter(User.email == email)
        ).one()
    except Exception as e:
        print(f"Error when getting user by email : {e}")
        res = None

    return res


def authenticate_user(db_session: Session, email: str, password: str):
    user: User | None = get_user(db_session, email)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM")
    )
    return encoded_jwt
