from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from db.schemas import MusicCreate, MusicUpdate
from starlette.exceptions import HTTPException
from db.models import Music, Author
from .base import BaseService
from db.session import get_session
import sqlalchemy
import os


class MusicService(BaseService[Music, MusicCreate, MusicUpdate]):
    def __init__(self, db_session: Session):
        super(MusicService, self).__init__(Music, db_session)

    def create(self, obj: MusicCreate, poster_img: UploadFile):
        if not os.path.exists("static/music_poster_images"):
            os.makedirs("static/music_poster_images")

        with open(f"static/music_poster_images/{poster_img.filename}", "wb") as f:
            f.write(poster_img.file.read())

        author: Author = self.db_session.get(Author, obj.author_id)

        db_obj: Music = Music(
            name=obj.name,
            release_date=obj.release_date,
            anime_id=obj.anime_id,
            type_id=obj.type_id,
            poster_img=poster_img.filename,
        )

        db_obj.author.append(author)

        print(f"converted to Music model : ${db_obj}")
        self.db_session.add(db_obj)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        print("End create")
        return db_obj


def get_service(db_session: Session = Depends(get_session)) -> MusicService:
    return MusicService(db_session)
