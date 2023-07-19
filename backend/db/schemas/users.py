import json
from typing import List
from pydantic import BaseModel

from .musics import MusicShort


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
