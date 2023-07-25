from enum import Enum
from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from db.schemas.musics import MusicCreate, MusicUpdate
from starlette.exceptions import HTTPException
from db.models import Music, Author, User
from .base import BaseService
from db.session import get_session
import sqlalchemy
from firebase import bucket


class OrderMusicBy(str, Enum):
    AVG_NOTE = "avg_note"
    NAME = "name"


class MusicService(BaseService[Music, MusicCreate, MusicUpdate]):
    def __init__(self, db_session: Session):
        super(MusicService, self).__init__(Music, db_session)

    def get_most_popular(self):
        return self.db_session.query(Music).order_by(Music.avg_note.desc()).limit(5).all()

    def get_last_added(self):
        return self.db_session.query(Music).order_by(Music.creation_date.desc()).limit(5).all()

    def list(self, order_by):
        if order_by:
            if order_by == OrderMusicBy.AVG_NOTE:
                return self.db_session.query(Music).order_by(Music.avg_note.desc())

        return self.db_session.query(Music).order_by(Music.name)

    def search(self, term: str):
        return self.db_session.query(Music).filter(Music.name.like(f"%{term}%"))

    def get_musics_anime(self, id_anime: int):
        musics = self.db_session.query(
            Music).filter(Music.anime_id == id_anime).order_by(Music.release_date.desc()).all()

        return musics

    def get_musics_artist(self, id_artist: int):
        artist: Author = self.db_session.query(
            Author).get(id_artist)
        musics = sorted(
            artist.musics, key=lambda m: m.release_date, reverse=True)
        return musics

    def create(self, obj: MusicCreate, poster_img: UploadFile, user: User):
        if user.is_manager:
            blob = bucket.blob(f"music_poster_images/{poster_img.filename}")
            blob.upload_from_file(poster_img.file, content_type="image/png")
            blob.make_public()

            list_author = []

            for id in obj.authors:
                list_author.append(self.db_session.get(Author, id))

            print(list_author)

            db_obj: Music = Music(
                name=obj.name,
                release_date=obj.release_date,
                anime_id=obj.anime_id,
                type_id=obj.type_id,
                poster_img=blob.public_url,
            )

            print(db_obj)

            db_obj.authors = list_author

            print(f"converted to Music model : ${db_obj}")
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
            return db_obj.id
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def add_to_favorite(self, id: str, user: User):
        music = self.db_session.get(Music, id)

        if music is None:
            raise HTTPException(status_code=404, detail="Music not found")

        user.favorites.append(music)

        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=409, detail="Conflict Error")
            else:
                raise e
        print("End add to favorite")

    def get_favorites(self, user: User):
        return user.favorites

    def get_user_favorites(self, id: int):
        user = self.db_session.get(User, id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user.favorites

    def remove_from_favorite(self, id: str, user: User):
        music = self.db_session.get(Music, id)

        if music is None:
            raise HTTPException(status_code=404, detail="Music not found")

        user.favorites.remove(music)

        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=409, detail="Conflict Error")
            else:
                raise e
        print("End remove from favorite")

    def update(self, id, obj: MusicUpdate, poster_img: UploadFile, user: User):
        if user.is_manager:
            db_obj = self.db_session.get(Music, id)

            list_author = []

            for id in obj.authors:
                list_author.append(self.db_session.get(Author, id))

            for column, value in obj.dict(exclude_unset=True).items():
                if column == "authors":
                    db_obj.authors = list_author
                else:
                    setattr(db_obj, column, value)

            if poster_img is not None:
                blob = bucket.blob(
                    f"music_poster_images/{poster_img.filename}")
                blob.upload_from_file(
                    poster_img.file, content_type="image/png")
                blob.make_public()

                setattr(db_obj, "poster_img", blob.public_url)

            self.db_session.commit()
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def delete(self, id: int, user: User):
        if user.is_manager:
            db_obj = self.db_session.query(Music).get(id)
            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(status_code=401, detail="Forbidden")


def get_service(db_session: Session = Depends(get_session)) -> MusicService:
    return MusicService(db_session)
