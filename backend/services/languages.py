from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.schemas.languages import LanguageCreate, LanguageUpdate
from db.models import AnimeTranslation, Language, User
from .base import BaseService
from db.session import get_session
from sqlalchemy import exc


class LanguageService(BaseService[Language, LanguageCreate, LanguageUpdate]):
    def __init__(self, db_session: Session):
        super(LanguageService, self).__init__(Language, db_session)

    def create(self, obj: LanguageCreate, current_user: User):
        if current_user.is_manager:
            db_obj: Language = self.model(**obj.dict())
            print(
                f"In BaseService : before {type(obj)} and after {type(db_obj)}")
            self.db_session.add(db_obj)
            try:
                self.db_session.commit()
            except exc.IntegrityError as e:
                self.db_session.rollback()
                if "Duplicate entry" in str(e):
                    raise HTTPException(
                        status_code=409, detail="Conflict Error")
                else:
                    raise e
            return db_obj
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def update(self, id: int, obj: LanguageUpdate, current_user: User):
        if current_user.is_manager:
            db_obj = self.db_session.get(Language, id)
            print(f"Update : {db_obj}")
            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            self.db_session.commit()
            return db_obj
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def delete(self, id: int, current_user: User):
        if current_user.is_manager:
            db_obj = self.db_session.query(self.model).get(id)
            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def get_languages_by_anime(self, id):
        return self.db_session.query(Language).join(Language.anime_translations).where(AnimeTranslation.id_anime == id).all()


def get_service(db_session: Session = Depends(get_session)) -> LanguageService:
    return LanguageService(db_session)
