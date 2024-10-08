import json
from datetime import datetime

from pydantic import BaseModel

from .animes import Anime, AnimeShort
from .artists import Artist
from .types import Type


class MusicBase(BaseModel):
    name: str
    release_date: datetime


class MusicCreate(MusicBase):
    artists: list[int]
    anime_id: int
    type_id: int
    id_video: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class MusicUpdate(MusicCreate):
    pass


class MusicArtist(MusicBase):
    id: int
    poster_img: str
    anime: AnimeShort
    type: Type

    class Config:
        orm_mode = True


class MusicShort(BaseModel):
    id: int
    poster_img: str
    name: str
    avg_note: float
    release_date: datetime
    type: Type

    class Config:
        orm_mode = True


class MusicSearch(MusicBase):
    id: int
    poster_img: str

    class Config:
        orm_mode = True


class MusicAnime(MusicBase):
    id: int
    poster_img: str
    artists: list[Artist]
    type: Type

    class Config:
        orm_mode = True


class Music(MusicBase):
    id: int
    poster_img: str
    artists: list[Artist]
    avg_note: float = None
    anime: Anime = None
    type: Type = None
    id_video: str

    class Config:
        orm_mode = True
