from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from db.schemas.animes import AnimeCreate, AnimeUpdate
from starlette.exceptions import HTTPException
from db.models import Anime, User
from .base import BaseService
from db.session import get_session
import sqlalchemy
from firebase import bucket


class AnimeService(BaseService[Anime, AnimeCreate, AnimeUpdate]):
    def __init__(self, db_session: Session):
        super(AnimeService, self).__init__(Anime, db_session)

    def list(self):
        return self.db_session.query(Anime).order_by(Anime.name)

    def search(self, term: str):
        return self.db_session.query(Anime).filter(Anime.name.like(f"%{term}%"))

    def create(self, obj: AnimeCreate, poster_img: UploadFile, user: User):

        if user.is_manager:
            blob = bucket.blob(f"anime_poster_images/{poster_img.filename}")
            blob.upload_from_file(poster_img.file, content_type="image/png")
            blob.make_public()

            db_obj: Anime = Anime(
                name=obj.name,
                poster_img=blob.public_url,
                description=obj.description
            )

            print(f"converted to Anime model : {db_obj}")
            self.db_session.add(db_obj)
            try:
                self.db_session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                self.db_session.rollback()
                if "Duplicate entry" in str(e):
                    raise HTTPException(
                        status_code=409, detail="Conflict Error")
                else:
                    raise e
            print("End create")
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def update(self, id, obj: AnimeUpdate, poster_img: UploadFile, user: User):

        if user.is_manager:
            print(f"Data : {obj}, img : {poster_img}")

            db_obj = self.db_session.get(Anime, id)

            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            print(poster_img is not None)
            if poster_img is not None:
                blob = bucket.blob(
                    f"anime_poster_images/{poster_img.filename}")
                blob.upload_from_file(
                    poster_img.file, content_type="image/png")
                blob.make_public()

                setattr(db_obj, "poster_img", blob.public_url)

            self.db_session.commit()
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def delete(self, id: int, user: User):
        if user.is_manager:
            db_obj = self.db_session.query(Anime).get(id)
            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(status_code=401, detail="Forbidden")


def get_service(db_session: Session = Depends(get_session)) -> AnimeService:
    return AnimeService(db_session)
