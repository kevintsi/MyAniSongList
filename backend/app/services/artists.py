from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends, UploadFile, status
from app.db.schemas.artists import ArtistCreate, ArtistUpdate
from starlette.exceptions import HTTPException
from app.db.models import Artist, User
from .base import BaseService
from app.db.session import get_session
import sqlalchemy
from app.firebase import bucket


class ArtistService(BaseService[Artist, ArtistCreate, ArtistUpdate]):
    def __init__(self, db_session: Session):
        super(ArtistService, self).__init__(Artist, db_session)

    def list(self):
        return select(Artist).order_by(Artist.name)

    def search(self, term: str):
        return select(Artist).filter(Artist.name.like(f"%{term}%"))

    def create(self, obj: ArtistCreate, poster_img: UploadFile, user: User):
        if user.is_manager:
            blob = bucket.blob(f"artist_poster_images/{poster_img.filename}")
            blob.upload_from_file(poster_img.file, content_type="image/png")
            blob.make_public()

            db_obj: Artist = Artist(
                name=obj.name,
                creation_year=obj.creation_year,
                poster_img=blob.public_url,
            )

            print(f"converted to Artist model : ${db_obj}")
            self.db_session.add(db_obj)
            try:
                self.db_session.commit()
                return db_obj
            except sqlalchemy.exc.IntegrityError as e:
                self.db_session.rollback()
                if "Duplicate entry" in str(e):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT, detail="Conflict Error")
                else:
                    raise e
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")

    def update(self, id, obj: ArtistUpdate, poster_img: UploadFile, user: User):
        if user.is_manager:
            db_obj = self.db_session.get(Artist, id)

            if db_obj is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Artist with this id not found")

            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)

            if poster_img is not None:
                blob = bucket.blob(
                    f"artist_poster_images/{poster_img.filename}")
                blob.upload_from_file(
                    poster_img.file, content_type="image/png")
                blob.make_public()

                setattr(db_obj, "poster_img", blob.public_url)

            self.db_session.commit()
            return db_obj
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")

    def delete(self, id: int, user: User):
        if user.is_manager:
            db_obj = self.db_session.get(Artist, id)

            if db_obj is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Artist id not found")

            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")


def get_service(db_session: Session = Depends(get_session)) -> ArtistService:
    return ArtistService(db_session)
