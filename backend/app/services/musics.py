from enum import Enum
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends, UploadFile, status
from app.db.schemas.musics import MusicAnime, MusicArtist, MusicCreate, MusicUpdate, Music as MusicSchema
from app.db.schemas.animes import Anime as AnimeSchema
from app.db.schemas.types import Type as TypeSchema
from starlette.exceptions import HTTPException
from app.db.models import Anime, AnimeTranslation, Language, Music, Author, Type, TypeTranslation, User
from .base import BaseService
from app.db.session import get_session
import sqlalchemy
from app.firebase import bucket


class OrderMusicBy(str, Enum):
    AVG_NOTE = "avg_note"
    NAME = "name"


class MusicService(BaseService[Music, MusicCreate, MusicUpdate]):
    def __init__(self, db_session: Session):
        super(MusicService, self).__init__(Music, db_session)

    def get(self, id, lang):
        lang = self.db_session.scalars(
            select(Language).filter(Language.code == lang)).first()

        obj = self.db_session.execute(select(Music,
                                             AnimeTranslation,
                                             TypeTranslation
                                             ).join(Anime,
                                                    Anime.id == Music.anime_id).join(Type, Type.id == Music.type_id).join(Anime.anime_translations).join(Type.type_translations).filter(AnimeTranslation.id_language == lang.id, TypeTranslation.id_language == lang.id,  Music.id == id)).first()
        if lang and obj:
            return MusicSchema(name=obj.Music.name,
                               release_date=obj.Music.release_date,
                               id=obj.Music.id, poster_img=obj.Music.poster_img,
                               authors=obj.Music.authors,
                               avg_note=obj.Music.avg_note,
                               anime=AnimeSchema(id=obj.AnimeTranslation.id_anime, description=obj.AnimeTranslation.description,
                                                 poster_img=obj.AnimeTranslation.anime.poster_img, name=obj.AnimeTranslation.name),
                               type=TypeSchema(
                                   id=obj.TypeTranslation.id_type, name=obj.TypeTranslation.name),
                               id_video=obj.Music.id_video
                               )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="language id or music id not found")

    def get_most_popular(self):
        return self.db_session.scalars(select(Music).order_by(Music.avg_note.desc()).limit(5)).all()

    def get_latest(self):
        return self.db_session.scalars(select(Music).order_by(Music.release_date.desc()).limit(5)).all()

    def list(self, order_by):
        if order_by:
            if order_by == OrderMusicBy.AVG_NOTE:
                return self.db_session.scalars(select(Music).order_by(Music.avg_note.desc()))

        return self.db_session.scalars(select(Music).order_by(Music.name))

    def search(self, term: str):
        return self.db_session.query(Music).filter(Music.name.like(f"%{term}%"))

    def get_musics_anime(self, id_anime: int, lang: str):
        lang: Language = self.db_session.query(
            Language).filter(Language.code == lang).first()
        musics = self.db_session.query(
            Music, TypeTranslation).join(
            TypeTranslation,
            TypeTranslation.id_type == Music.type_id).join(Language,
                                                           Language.id ==
                                                           TypeTranslation.id_language).filter(Music.anime_id == id_anime,
                                                                                               TypeTranslation.id_language == lang.id).order_by(Music.release_date.desc()).all()

        return [MusicAnime(
            id=m.Music.id,
            poster_img=m.Music.poster_img,
            authors=m.Music.authors,
            type=TypeSchema(id=m.TypeTranslation.id_type,
                            name=m.TypeTranslation.name),
            name=m.Music.name,
            release_date=m.Music.release_date) for m in musics]

    def get_musics_artist(self, id_artist: int, lang: str):
        lang: Language = self.db_session.query(
            Language).filter(Language.code == lang).first()
        musics = self.db_session.query(Music, TypeTranslation).join(
            TypeTranslation,
            TypeTranslation.id_type == Music.type_id).join(Music.authors).join(Language,
                                                                               Language.id ==
                                                                               TypeTranslation.id_language).filter(Author.id == id_artist, TypeTranslation.id_language == lang.id).order_by(Music.release_date.desc())

        return [MusicArtist(
            id=m.Music.id,
            poster_img=m.Music.poster_img,
            type=TypeSchema(id=m.TypeTranslation.id_type,
                            name=m.TypeTranslation.name),
            name=m.Music.name,
            release_date=m.Music.release_date) for m in musics]

    def create(self, obj: MusicCreate, poster_img: UploadFile, user: User):
        if user.is_manager:
            blob = bucket.blob(f"music_poster_images/{poster_img.filename}")
            blob.upload_from_file(poster_img.file, content_type="image/png")
            blob.make_public()

            anime = self.db_session.get(Anime, obj.anime_id)
            type = self.db_session.get(Type, obj.type_id)

            list_authors = []

            for id in obj.authors:
                list_authors.append(self.db_session.get(Author, id))

            print(anime, type, list_authors)

            if anime and type and len(list_authors) > 0:
                db_obj: Music = Music(
                    name=obj.name,
                    release_date=obj.release_date,
                    type=type,
                    anime=anime,
                    poster_img=blob.public_url,
                    id_video=obj.id_video,
                    authors=list_authors
                )

                print(f"converted to Music model : ${db_obj}")
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
                    status_code=status.HTTP_404_NOT_FOUND, detail="Anime or Type or Authors not found")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")

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

            print(f"Music {db_obj}")

            return db_obj
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")

    def delete(self, id: int, user: User):
        if user.is_manager:
            db_obj = self.db_session.query(Music).get(id)
            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(status_code=401, detail="Forbidden")


def get_service(db_session: Session = Depends(get_session)) -> MusicService:
    return MusicService(db_session)
