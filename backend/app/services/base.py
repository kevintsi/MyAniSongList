from typing import Any, Generic, Optional, Type, TypeVar

from app.db.models import Base
from fastapi import status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: Session):

        self.model = model
        self.db_session = db_session

    def get(self, id: Any) -> ModelType:
        obj: ModelType | None = self.db_session.get(self.model, id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
            )
        return obj

    def list(self):
        return self.db_session.scalars(select(self.model))

    def create(self, obj: CreateSchemaType) -> ModelType:
        db_obj: ModelType = self.model(**obj.dict())
        print(f"In BaseService : before {type(obj)} and after {type(db_obj)}")
        self.db_session.add(db_obj)
        try:
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error",
                )
            else:
                raise e
        return db_obj

    def update(self, id: Any, obj: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = self.get(id)
        print(f"Update : {db_obj}")
        for column, value in obj.dict(exclude_unset=True).items():
            setattr(db_obj, column, value)
        self.db_session.commit()
        return db_obj

    def delete(self, id: Any) -> None:
        db_obj = self.db_session.get(self.model, id)
        self.db_session.delete(db_obj)
        self.db_session.commit()
