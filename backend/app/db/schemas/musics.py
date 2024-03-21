from typing import List
from datetime import datetime
import json
from pydantic import BaseModel
from .types import Type

from .animes import Anime, AnimeShort
from .artists import Artist


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

    class Config:
        orm_mode = True


class MusicSearch(MusicBase):
    id: int
    poster_img: str
    type: Type
    avg_note: float

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
