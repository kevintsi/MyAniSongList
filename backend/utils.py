from sqlalchemy.orm import Session
from db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db_session: Session, username: str):
    return db_session.query(User).filter(User.username == username).one()


def authenticate_user(db_session: Session, username: str, password: str):
    user: User = get_user(db_session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
