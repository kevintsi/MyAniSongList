from app.db.models import AnimeTranslation, Language, TypeTranslation, User
from app.db.schemas.languages import LanguageCreate, LanguageUpdate
from app.db.session import get_session
from fastapi import Depends, HTTPException, status
from sqlalchemy import exc, select
from sqlalchemy.orm import Session

from .base import BaseService


class LanguageService(BaseService[Language, LanguageCreate, LanguageUpdate]):
    def __init__(self, db_session: Session):
        super(LanguageService, self).__init__(Language, db_session)

    def create(self, obj: LanguageCreate):
        db_obj: Language = self.model(**obj.dict())
        print(
            f"In BaseService : before {type(obj)} and after {type(db_obj)}"
        )
        self.db_session.add(db_obj)
        try:
            self.db_session.commit()
        except exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error",
                )
            else:
                raise e
        return db_obj

    def update(self, id: int, obj: LanguageUpdate):
        db_obj = self.db_session.get(Language, id)

        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Language id not found",
            )

        print(f"Update : {db_obj}")
        for column, value in obj.dict(exclude_unset=True).items():
            setattr(db_obj, column, value)
        self.db_session.commit()
        return db_obj

    def delete(self, id: int):
        db_obj = self.db_session.get(self.model, id)

        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Language id not found",
            )

        self.db_session.delete(db_obj)
        self.db_session.commit()

    def get_languages_by_anime(self, id: int):
        return self.db_session.scalars(
            select(Language)
            .join(Language.anime_translations)
            .where(AnimeTranslation.id_anime == id)
        ).all()

    def get_languages_by_type(self, id: int):
        return self.db_session.scalars(
            select(Language)
            .join(Language.type_translations)
            .where(TypeTranslation.id_type == id)
        ).all()


def get_service(
    db_session: Session = Depends(get_session),
) -> LanguageService:
    return LanguageService(db_session)
