from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from db.schemas import AnimeCreate, AnimeUpdate
from starlette.exceptions import HTTPException
from db.models import Anime
from .base import BaseService
from db.session import get_session
import sqlalchemy
import os


class AnimeService(BaseService[Anime, AnimeCreate, AnimeUpdate]):
    def __init__(self, db_session: Session):
        super(AnimeService, self).__init__(Anime, db_session)

    def create(self, obj: AnimeCreate, poster_img: UploadFile):
        if not os.path.exists("static/poster_images"):
            os.makedirs("static/poster_images")

        with open(f"static/poster_images/{poster_img.filename}", "wb") as f:
            f.write(poster_img.file.read())

        db_obj: Anime = Anime(
            name=obj.name,
            poster_img=poster_img.filename,
            description=obj.description
        )

        print(f"converted to Anime model : ${db_obj}")
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


def get_anime_service(db_session: Session = Depends(get_session)) -> AnimeService:
    return AnimeService(db_session)
