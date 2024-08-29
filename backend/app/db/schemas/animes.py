import json

from pydantic import BaseModel


class AnimeBase(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class AnimeCreate(AnimeBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AnimeTranslationCreate(AnimeBase):
    pass


class AnimeUpdate(AnimeCreate):
    pass


class Anime(AnimeUpdate):
    id: int
    poster_img: str


class AnimeShort(BaseModel):
    name: str
    poster_img: str
