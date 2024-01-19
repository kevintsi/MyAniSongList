from datetime import datetime, timedelta
from os import getenv
import jwt
from sqlalchemy.orm import Session
from app.db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db_session: Session, email: str):
    try:
        res = db_session.query(User).filter(User.email == email).one()
    except:
        res = None

    return res


def authenticate_user(db_session: Session, email: str, password: str):
    user: User = get_user(db_session, email)
    print(f"User in utils.py : {user}")
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
    expire = datetime.utcnow() + expires_delta
    print(expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, getenv(
        "SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    return encoded_jwt
