from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile
import json

## Anime ##


class AnimeBase(BaseModel):
    name: str
    poster_img: str
    description: str


class AnimeCreate(AnimeBase):
    pass


class Anime(AnimeBase):
    id: int

    class Config:
        orm_mode = True

## Type ##


class TypeBase(BaseModel):
    type_name: str


class TypeCreate(TypeBase):
    pass


class Type(TypeBase):
    id: int

    class Config:
        orm_mode = True

## User ##

# BASE


class UserBase(BaseModel):
    username: str
    email: str

# POST


class UserCreate(UserBase):
    password: str

# UPDATE


class UserUpdate(UserCreate):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

# GET


class User(UserCreate):
    id: int
    profile_picture: str = None

    class Config:
        orm_mode = True

## Music ##


class MusicBase(BaseModel):
    name: str
    poster_img: str
    release_date: datetime
    anime: Anime
    type: Type


class MusicCreate(MusicBase):
    pass


class Music(MusicBase):
    id: int

    class Config:
        orm_mode = True

## Review ##


class ReviewBase(BaseModel):
    note_visual: float
    note_music: float
    description: str = None
    creation_date: datetime = None
    music: Music
    User: User


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
