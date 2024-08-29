from datetime import datetime

from pydantic import BaseModel

from .musics import MusicShort
from .users import User


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
    user: User
    music: MusicShort

    class Config:
        orm_mode = True
