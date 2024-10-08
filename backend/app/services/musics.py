from enum import Enum
from io import BytesIO

import sqlalchemy
from app.db.models import (
    Anime,
    AnimeTranslation,
    Artist,
    Language,
    Music,
    Type,
    TypeTranslation,
    User,
)
from app.db.schemas.animes import Anime as AnimeSchema
from app.db.schemas.animes import AnimeShort
from app.db.schemas.artists import Artist as ArtistSchema
from app.db.schemas.musics import Music as MusicSchema
from app.db.schemas.musics import (
    MusicAnime,
    MusicArtist,
    MusicCreate,
    MusicUpdate,
)
from app.db.schemas.types import Type as TypeSchema
from app.db.session import get_session
from app.firebase import bucket
from fastapi import Depends, UploadFile, status
from PIL import Image
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from .base import BaseService


class OrderMusicBy(str, Enum):
    AVG_NOTE = "avg_note"
    NAME = "name"


class MusicService(BaseService[Music, MusicCreate, MusicUpdate]):
    def __init__(self, db_session: Session):
        super(MusicService, self).__init__(Music, db_session)

    def get(self, id, lang):
        lang = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()

        obj = self.db_session.execute(
            select(Music, AnimeTranslation, TypeTranslation)
            .join(Anime, Anime.id == Music.anime_id)
            .join(Type, Type.id == Music.type_id)
            .join(Anime.anime_translations)
            .join(Type.type_translations)
            .filter(
                AnimeTranslation.id_language == lang.id,
                TypeTranslation.id_language == lang.id,
                Music.id == id,
            )
        ).first()
        if lang and obj:
            return MusicSchema(
                name=obj.Music.name,
                release_date=obj.Music.release_date,
                id=obj.Music.id,
                poster_img=obj.Music.poster_img,
                artists=obj.Music.artists,
                avg_note=obj.Music.avg_note,
                anime=AnimeSchema(
                    id=obj.AnimeTranslation.id_anime,
                    description=obj.AnimeTranslation.description,
                    poster_img=obj.AnimeTranslation.anime.poster_img,
                    name=obj.AnimeTranslation.name,
                ),
                type=TypeSchema(
                    id=obj.TypeTranslation.id_type,
                    name=obj.TypeTranslation.name,
                ),
                id_video=obj.Music.id_video,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="language id or music id not found",
            )

    def get_most_popular(self):
        return self.db_session.scalars(
            select(Music).order_by(Music.avg_note.desc()).limit(5)
        ).all()

    def get_latest(self):
        return self.db_session.scalars(
            select(Music).order_by(Music.release_date.desc()).limit(5)
        ).all()

    def list(self, order_by):
        if order_by:
            if order_by == OrderMusicBy.AVG_NOTE:
                return select(Music).order_by(Music.avg_note.desc())

        return select(Music).order_by(Music.name)

    def search(self, term: str):
        return select(Music).filter(Music.name.like(f"%{term}%"))

    def get_musics_anime(self, id_anime: int, lang: str):
        lang: Language | None = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()

        if lang:

            musics = self.db_session.execute(
                select(Music, TypeTranslation)
                .join(
                    TypeTranslation, TypeTranslation.id_type == Music.type_id
                )
                .join(Language, Language.id == TypeTranslation.id_language)
                .filter(
                    Music.anime_id == id_anime,
                    TypeTranslation.id_language == lang.id,
                )
                .order_by(Music.release_date.desc())
            ).all()

            return [
                MusicAnime(
                    id=m.Music.id,
                    poster_img=m.Music.poster_img,
                    artists=m.Music.artists,
                    type=TypeSchema(
                        id=m.TypeTranslation.id_type,
                        name=m.TypeTranslation.name,
                    ),
                    name=m.Music.name,
                    release_date=m.Music.release_date,
                )
                for m in musics
            ]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="language id not found",
            )

    def get_musics_artist(self, id_artist: int, lang: str):
        lang: Language | None = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()

        if lang:
            musics = self.db_session.execute(
                select(Music, TypeTranslation, AnimeTranslation)
                .join(
                    TypeTranslation, TypeTranslation.id_type == Music.type_id
                )
                .join(
                    AnimeTranslation,
                    AnimeTranslation.id_anime == Music.anime_id,
                )
                .join(Music.artists)
                .filter(
                    Artist.id == id_artist,
                    TypeTranslation.id_language == lang.id,
                    AnimeTranslation.id_language == lang.id,
                )
                .order_by(Music.release_date.desc())
            ).all()

            return [
                MusicArtist(
                    id=m.Music.id,
                    poster_img=m.Music.poster_img,
                    type=TypeSchema(
                        id=m.TypeTranslation.id_type,
                        name=m.TypeTranslation.name,
                    ),
                    anime=AnimeShort(
                        name=m.AnimeTranslation.name,
                        poster_img=m.AnimeTranslation.anime.poster_img,
                    ),
                    name=m.Music.name,
                    release_date=m.Music.release_date,
                )
                for m in musics
            ]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="language id not found",
            )

    def create(self, obj: MusicCreate, poster_img: UploadFile, user: User):
        if user.is_manager:
            image = Image.open(BytesIO(poster_img.file.read()))
            webp_buffer = BytesIO()
            image.save(webp_buffer, format="WEBP", quality=100)
            webp_buffer.seek(0)
            filename = poster_img.filename.rsplit(".", 1)[0] + ".webp"
            blob = bucket.blob(f"music_poster_images/{filename}")
            blob.upload_from_file(webp_buffer, content_type="image/webp")
            blob.make_public()

            anime = self.db_session.get(Anime, obj.anime_id)
            type = self.db_session.get(Type, obj.type_id)

            list_artists = []

            for id in obj.artists:
                list_artists.append(self.db_session.get(Artist, id))

            print(anime, type, list_artists)

            if anime and type and len(list_artists) > 0:
                db_obj: Music = Music(
                    name=obj.name,
                    release_date=obj.release_date,
                    type=type,
                    anime=anime,
                    poster_img=blob.public_url,
                    id_video=obj.id_video,
                    artists=list_artists,
                )

                print(f"converted to Music model : ${db_obj}")
                self.db_session.add(db_obj)
                try:
                    self.db_session.commit()

                    list_artists = list(
                        map(
                            lambda obj: ArtistSchema(
                                id=obj.id,
                                name=obj.name,
                                creation_year=obj.creation_year,
                                poster_img=obj.poster_img,
                            ),
                            list_artists,
                        )
                    )

                    return MusicSchema(
                        id=db_obj.id,
                        name=db_obj.name,
                        release_date=db_obj.release_date,
                        poster_img=db_obj.poster_img,
                        id_video=obj.id_video,
                        artists=list_artists,
                    )

                except sqlalchemy.exc.IntegrityError as e:
                    self.db_session.rollback()
                    if "Duplicate entry" in str(e):
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="Conflict Error",
                        )
                    else:
                        raise e
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Anime or Type or Artists not found",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )

    def add_to_favorite(self, id: str, user: User):
        music = self.db_session.get(Music, id)

        if music is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Music not found",
            )

        user.favorites.append(music)

        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error",
                )
            else:
                raise e
        print("End add to favorite")

    def get_favorites(self, user: User):
        return user.favorites

    def get_user_favorites(self, id: int):
        user = self.db_session.get(User, id)
        if user is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user.favorites

    def remove_from_favorite(self, id: str, user: User):
        music = self.db_session.get(Music, id)

        if music is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Music not found",
            )

        user.favorites.remove(music)

        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error",
                )
            else:
                raise e
        print("End remove from favorite")

    def update(self, id, obj: MusicUpdate, poster_img: UploadFile, user: User):
        if user.is_manager:
            db_obj = self.db_session.get(Music, id)

            if db_obj is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Music id not found",
                )

            list_artist = []

            for id in obj.artists:
                list_artist.append(self.db_session.get(Artist, id))

            for column, value in obj.dict(exclude_unset=True).items():
                if column == "artists":
                    db_obj.artists = list_artist
                else:
                    setattr(db_obj, column, value)

            if poster_img is not None:
                image = Image.open(BytesIO(poster_img.file.read()))
                webp_buffer = BytesIO()
                image.save(webp_buffer, format="WEBP", quality=100)
                webp_buffer.seek(0)
                filename = poster_img.filename.rsplit(".", 1)[0] + ".webp"
                blob = bucket.blob(f"music_poster_images/{filename}")
                blob.upload_from_file(webp_buffer, content_type="image/webp")
                blob.make_public()

                setattr(db_obj, "poster_img", blob.public_url)

            self.db_session.commit()

            print(f"Music {db_obj}")

            return MusicSchema(
                id=db_obj.id,
                name=db_obj.name,
                release_date=db_obj.release_date,
                poster_img=db_obj.poster_img,
                id_video=obj.id_video,
                artists=list(
                    map(
                        lambda obj: ArtistSchema(
                            id=obj.id,
                            name=obj.name,
                            creation_year=obj.creation_year,
                            poster_img=obj.poster_img,
                        ),
                        db_obj.artists,
                    )
                ),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )

    def delete(self, id: int, user: User):
        if user.is_manager:
            db_obj = self.db_session.get(Music, id)
            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )


def get_service(db_session: Session = Depends(get_session)) -> MusicService:
    return MusicService(db_session)
