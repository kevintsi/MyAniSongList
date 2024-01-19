import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.db.schemas.types import TypeCreate, TypeUpdate
from app.db.models import Language, Type, TypeTranslation, User
from .base import BaseService
from app.db.session import get_session


class TypeService(BaseService[Type, TypeCreate, TypeUpdate]):
    def __init__(self, db_session: Session):
        super(TypeService, self).__init__(Type, db_session)

    def create(self, obj: TypeCreate, user: User):
        if user.is_manager:
            db_obj: Type = self.model(**obj.dict())
            print(
                f"In BaseService : before {type(obj)} and after {type(db_obj)}")
            self.db_session.add(db_obj)
            try:
                self.db_session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                self.db_session.rollback()
                if "Duplicate entry" in str(e):
                    raise HTTPException(
                        status_code=409, detail="Conflict Error")
                else:
                    raise e
        else:
            raise HTTPException(status_code=401, detail="Forbidden")
        return db_obj

    def list(self, lang: str):
        lang_obj = self.db_session.query(
            Language).filter(Language.code == lang).first()

        if lang_obj:
            res = self.db_session.query(TypeTranslation, Type).join(Type.type_translations).filter(
                TypeTranslation.id_language == lang_obj.id)
            return [Type(id=row.Type.id, name=row.TypeTranslation.name)for row in res]
        else:
            raise HTTPException(
                status_code=404, detail="Error language")

    def update(self, id: int, obj: TypeUpdate, user: User):
        if user.is_manager:
            db_obj = self.db_session.get(Type, id)
            print(f"Update : {db_obj}")
            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            self.db_session.commit()
            return db_obj
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def add_translation(self, obj: TypeCreate, lang: str, id, user: User):
        if user.is_manager:
            lang_obj: Language = self.db_session.query(
                Language).filter(Language.code == lang).first()

            music_type: Type = self.db_session.query(
                Type).filter(Type.id == id).first()

            if lang_obj and music_type:
                try:

                    type_translation: Type = TypeTranslation(
                        type=music_type,
                        name=obj.name,
                        language=lang_obj
                    )
                    print(
                        f"In BaseService : before {type(obj)} and after {type(type_translation)}")
                    self.db_session.add(type_translation)
                    self.db_session.commit()
                except sqlalchemy.exc.IntegrityError as e:
                    self.db_session.rollback()
                    if "Duplicate entry" in str(e):
                        raise HTTPException(
                            status_code=409, detail="Conflict Error")
                    else:
                        raise e
            else:
                raise HTTPException(
                    status_code=404, detail="Error language or id type")
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def update_translation(self, obj: TypeUpdate, lang: str, id, user: User):
        if user.is_manager:
            lang_obj: Language = self.db_session.query(
                Language).filter(Language.code == lang).first()

            type: Type = self.db_session.query(
                Type).filter(TypeTranslation.id_type == id, Language.id == lang_obj.id).first()

            if lang_obj and type:
                try:

                    type_translation: Type = TypeTranslation(
                        type=type,
                        name=obj.name,
                        language=lang_obj
                    )
                    print(
                        f"In BaseService : before {type(obj)} and after {type(type_translation)}")
                    self.db_session.add(type_translation)
                    self.db_session.commit()
                except sqlalchemy.exc.IntegrityError as e:
                    self.db_session.rollback()
                    if "Duplicate entry" in str(e):
                        raise HTTPException(
                            status_code=409, detail="Conflict Error")
                    else:
                        raise e
            else:
                raise HTTPException(
                    status_code=404, detail="Error language or id type")
        else:
            raise HTTPException(status_code=401, detail="Forbidden")


def get_service(db_session: Session = Depends(get_session)) -> TypeService:
    return TypeService(db_session)
