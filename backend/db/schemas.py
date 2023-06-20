from typing import List
from pydantic import BaseModel, Extra
from datetime import datetime
import json
## Anime ##


class AnimeBase(BaseModel):
    name: str
    description: str


class AnimeCreate(AnimeBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AnimeUpdate(AnimeCreate):
    pass


class Anime(AnimeUpdate):
    id: int
    poster_img: str

    class Config:
        orm_mode = True

## Type ##


class TypeBase(BaseModel):
    type_name: str


class TypeCreate(TypeBase):
    pass


class TypeUpdate(TypeBase):
    pass


class Type(TypeBase):
    id: int

    class Config:
        orm_mode = True

## User ##

# BASE


class UserBase(BaseModel):
    email: str


class UserLogin(UserBase):
    password: str

# POST


class UserCreate(UserBase):
    username: str
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


class User(UserBase):
    id: int
    profile_picture: str = None
    username: str

    class Config:
        orm_mode = True


class UserPublic(BaseModel):
    id: int
    profile_picture: str = None
    username: str

    class Config:
        orm_mode = True

## Author ##


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


## Music ##


class MusicBase(BaseModel):
    name: str
    release_date: datetime
    avg_note: float = None


class MusicCreate(MusicBase):
    authors: list[int]
    anime_id: int
    type_id: int

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
    anime: Anime
    type: Type

    class Config:
        orm_mode = True


class Music(MusicBase):
    id: int
    poster_img: str
    authors: List[Author]
    anime: Anime
    type: Type

    class Config:
        orm_mode = True

## Review ##


class ReviewBase(BaseModel):
    note_visual: float
    note_music: float
    description: str = None


class ReviewCreate(ReviewBase):
    music_id: int


class ReviewUpdate(ReviewCreate):
    pass


class Review(ReviewBase):
    id: int
    creation_date: datetime
    user: UserPublic
    music_id: int

    class Config:
        orm_mode = True
## Token ##


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
