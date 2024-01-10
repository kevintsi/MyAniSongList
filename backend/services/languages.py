from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.schemas.languages import LanguageCreate, LanguageUpdate
from db.models import Language
from .base import BaseService
from db.session import get_session
from sqlalchemy import exc


class LanguageService(BaseService[Language, LanguageCreate, LanguageUpdate]):
    def __init__(self, db_session: Session):
        super(LanguageService, self).__init__(Language, db_session)

    def create(self, obj: LanguageCreate):
        db_obj: Language = self.model(**obj.dict())
        print(f"In BaseService : before {type(obj)} and after {type(db_obj)}")
        self.db_session.add(db_obj)
        try:
            self.db_session.commit()
        except exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        return db_obj


def get_service(db_session: Session = Depends(get_session)) -> LanguageService:
    return LanguageService(db_session)
