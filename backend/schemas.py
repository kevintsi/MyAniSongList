from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Anime(BaseModel):
    id: int
    name: str
    poster_img: str
    description: str


class Type(BaseModel):
    id: int
    type_name: str


class Account(BaseModel):
    id: int
    username: str
    email: str
    password: str
    profil_picture: str
    is_manager: bool
    creation_date: datetime


class Music(BaseModel):
    id: int
    name: str
    poster_img: str
    release_date: datetime
    anime: Anime
    type: Type


class Review(BaseModel):
    note_visual: float
    note_music: float
    description: Optional[str]
    creation_date: datetime
    music: Music
    account: Account
