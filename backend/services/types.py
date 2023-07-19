from sqlalchemy.orm import Session
from fastapi import Depends
from db.schemas.types import TypeCreate, TypeUpdate
from db.models import Type
from .base import BaseService
from db.session import get_session


class TypeService(BaseService[Type, TypeCreate, TypeUpdate]):
    def __init__(self, db_session: Session):
        super(TypeService, self).__init__(Type, db_session)


def get_service(db_session: Session = Depends(get_session)) -> TypeService:
    return TypeService(db_session)
