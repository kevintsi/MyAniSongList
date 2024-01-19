import json
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    creation_year: str


class AuthorCreate(AuthorBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AuthorUpdate(AuthorCreate):
    pass


class Author(AuthorBase):
    id: int
    poster_img: str

    class Config:
        orm_mode = True
