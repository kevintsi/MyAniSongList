from pydantic import BaseModel
from datetime import datetime

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

## Account ##


class AccountBase(BaseModel):
    username: str
    email: str


class AccountCreate(AccountBase):
    password: str
    creation_date: datetime = datetime.now()


class AccountUpdate(AccountCreate):
    profil_picture: str


class Account(AccountBase):
    id: int = None

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
    account: Account


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
