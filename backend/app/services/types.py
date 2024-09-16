import sqlalchemy
from app.db.models import Language, Type, TypeTranslation, User
from app.db.schemas.types import Type as TypeSchema
from app.db.schemas.types import TypeCreate, TypeUpdate
from app.db.session import get_session
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .base import BaseService


class TypeService(BaseService[Type, TypeCreate, TypeUpdate]):
    def __init__(self, db_session: Session):
        super(TypeService, self).__init__(Type, db_session)

    def create(self, obj: TypeCreate):
        db_obj: Type = self.model(**obj.dict())

        lang_obj: Language | None = self.db_session.scalars(
            select(Language).filter(Language.code == "fr")
        ).first()

        if lang_obj is None:
            raise HTTPException(
                status=status.HTTP_404_NOT_FOUND,
                detail="Default language missing (fr)",
            )

        type_translation: TypeTranslation = TypeTranslation(
            name=db_obj.name, type=db_obj, language=lang_obj
        )

        self.db_session.add(type_translation)
        try:
            self.db_session.commit()
            return db_obj
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error",
                )
            else:
                raise e

    def get_translation(self, id: int, lang: str):
        lang_obj: Language | None = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()

        type_obj: Type | None = self.db_session.get(Type, id)

        if lang_obj and type_obj:
            res = self.db_session.scalars(
                select(TypeTranslation).filter(
                    TypeTranslation.id_language == lang_obj.id,
                    TypeTranslation.id_type == type_obj.id,
                )
            ).first()

            return Type(id=res.type.id, name=res.name)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error language or id type",
            )

    def list(self, lang: str):
        lang_obj = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()

        if lang_obj:
            res = self.db_session.scalars(
                select(TypeTranslation).filter(
                    TypeTranslation.id_language == lang_obj.id
                )
            ).all()
            print(res)
            return [Type(id=row.type.id, name=row.name) for row in res]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Error language"
            )

    def update(self, id: int, obj: TypeUpdate):
        db_obj = self.db_session.get(Type, id)

        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Type id not found",
            )

        print(f"Update : {db_obj}")
        for column, value in obj.dict(exclude_unset=True).items():
            setattr(db_obj, column, value)
        self.db_session.commit()
        return db_obj

    def add_translation(self, obj: TypeCreate, lang: str, id):
        lang_obj: Language | None = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()

        music_type: Type | None = self.db_session.get(Type, id)

        if lang_obj and music_type:
            try:
                type_translation: TypeTranslation = TypeTranslation(
                    type=music_type, name=obj.name, language=lang_obj
                )
                print(
                    f"In BaseService : before {type(obj)} and after {type(type_translation)}"
                )
                self.db_session.add(type_translation)
                self.db_session.commit()
                return TypeSchema(
                    name=type_translation.name, id=music_type.id
                )

            except sqlalchemy.exc.IntegrityError as e:
                self.db_session.rollback()
                if "Duplicate entry" in str(e):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Conflict Error",
                    )
                else:
                    raise e
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error language or id type",
            )
        
    def update_translation(
        self, obj: TypeUpdate, lang: str, id
    ) -> Type:
        lang_obj: Language | None = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()

        type_obj: Type | None = self.db_session.get(Type, id)

        if lang_obj and type_obj:

            type_trans_obj: TypeTranslation = self.db_session.scalars(
                select(TypeTranslation).filter(
                    TypeTranslation.id_type == type_obj.id,
                    TypeTranslation.id_language == lang_obj.id,
                )
            ).first()

            type_trans_obj.name = obj.name

            self.db_session.commit()

            return TypeSchema(name=type_trans_obj.name, id=type_obj.id)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error language or id type",
            )

    def delete(self, id: int):
        db_obj: Type | None = self.db_session.get(Type, id)

        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error type id not found",
            )

        self.db_session.delete(db_obj)
        self.db_session.commit()


def get_service(db_session: Session = Depends(get_session)) -> TypeService:
    return TypeService(db_session)
