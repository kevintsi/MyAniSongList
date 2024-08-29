from io import BytesIO

from app.db.models import Anime, AnimeTranslation, Language, User
from app.db.schemas.animes import Anime as AnimeSchema
from app.db.schemas.animes import (
    AnimeCreate,
    AnimeTranslationCreate,
    AnimeUpdate,
)
from app.db.session import get_session
from app.firebase import bucket
from fastapi import Depends, UploadFile, status
from PIL import Image
from sqlalchemy import exc, select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from .base import BaseService


class AnimeService(BaseService[Anime, AnimeCreate, AnimeUpdate]):
    def __init__(self, db_session: Session):
        super(AnimeService, self).__init__(Anime, db_session)

    def list(self, lang):
        obj_lang = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()
        if obj_lang:
            return select(AnimeTranslation).where(
                AnimeTranslation.id_language == obj_lang.id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Error language"
            )

    def get(self, id: int, lang: str):
        obj_lang = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()

        anime = self.db_session.get(Anime, id)

        if obj_lang and anime:

            obj: AnimeTranslation | None = self.db_session.scalars(
                select(AnimeTranslation).where(
                    AnimeTranslation.id_language == obj_lang.id,
                    AnimeTranslation.id_anime == anime.id,
                )
            ).first()

            if obj is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Error no translation found for this language",
                )

            return AnimeSchema(
                id=obj.id_anime,
                name=obj.name,
                description=obj.description,
                poster_img=obj.anime.poster_img,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error language or anime id",
            )

    def search(self, term: str, lang: str):
        lang: Language | None = self.db_session.scalars(
            select(Language).filter(Language.code == lang)
        ).first()
        if lang:
            return select(AnimeTranslation).filter(
                AnimeTranslation.name.like(f"%{term}%"),
                AnimeTranslation.id_language == lang.id,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Error language"
            )

    def create(self, obj: AnimeCreate, poster_img: UploadFile, user: User):
        if user.is_manager:
            lang_obj: Language | None = self.db_session.scalars(
                select(Language).filter(Language.code == "fr")
            ).first()

            if lang_obj:
                image = Image.open(BytesIO(poster_img.file.read()))
                webp_buffer = BytesIO()
                image.save(webp_buffer, format="WEBP", quality=100)
                webp_buffer.seek(0)
                filename = poster_img.filename.rsplit(".", 1)[0] + ".webp"
                blob = bucket.blob(f"anime_poster_images/{filename}")
                blob.upload_from_file(webp_buffer, content_type="image/webp")
                blob.make_public()

                try:

                    anime: Anime = Anime(poster_img=blob.public_url)

                    anime_translation: AnimeTranslation = AnimeTranslation(
                        anime=anime,
                        name=obj.name,
                        description=obj.description,
                        language=lang_obj,
                    )

                    print(f"converted to Anime model : {anime_translation}")
                    self.db_session.add(anime_translation)
                    self.db_session.commit()

                    return AnimeSchema(
                        id=anime.id,
                        name=anime_translation.name,
                        description=anime_translation.description,
                        poster_img=anime.poster_img,
                    )

                except exc.IntegrityError as e:
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
                    detail="Error language",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )

    def create_translation(
        self, obj: AnimeTranslationCreate, id: int, lang: str, user: User
    ):
        if user.is_manager:
            lang_obj: Language | None = (
                self.db_session.query(Language)
                .filter(Language.code == lang)
                .first()
            )

            anime: Anime | None = (
                self.db_session.query(Anime).filter(Anime.id == id).first()
            )

            if lang_obj and anime:
                try:
                    anime_translation: AnimeTranslation = AnimeTranslation(
                        anime=anime,
                        name=obj.name,
                        description=obj.description,
                        language=lang_obj,
                    )

                    print(
                        f"converted to AnimeTranslation model : {anime_translation}"
                    )
                    self.db_session.add(anime_translation)
                    self.db_session.commit()
                    return AnimeSchema(
                        id=anime.id,
                        name=anime_translation.name,
                        description=anime_translation.description,
                        poster_img=anime.poster_img,
                    )
                except exc.IntegrityError as e:
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
                    status_code=404, detail="Error language or anime id"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )

    def update(
        self,
        id,
        obj: AnimeUpdate,
        poster_img: UploadFile,
        lang: str,
        user: User,
    ):

        if user.is_manager:

            obj_lang: Language | None = self.db_session.scalars(
                select(Language).filter(Language.code == lang)
            ).first()

            anime: Anime | None = self.db_session.get(Anime, id)

            if anime and obj_lang:
                if poster_img:
                    image = Image.open(BytesIO(poster_img.file.read()))
                    webp_buffer = BytesIO()
                    image.save(webp_buffer, format="WEBP", quality=100)
                    webp_buffer.seek(0)
                    filename = poster_img.filename.rsplit(".", 1)[0] + ".webp"
                    blob = bucket.blob(f"anime_poster_images/{filename}")
                    blob.upload_from_file(
                        webp_buffer, content_type="image/webp"
                    )
                    blob.make_public()

                    anime.poster_img = blob.public_url

                anime_translation: AnimeTranslation = self.db_session.scalars(
                    select(AnimeTranslation).filter(
                        AnimeTranslation.id_anime == anime.id,
                        AnimeTranslation.id_language == obj_lang.id,
                    )
                ).first()

                for col, value in obj.dict(exclude_unset=True).items():
                    setattr(anime_translation, col, value)

                self.db_session.commit()
                return AnimeSchema(
                    id=anime.id,
                    name=anime_translation.name,
                    description=anime_translation.description,
                    poster_img=anime.poster_img,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Error language or anime id",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )

    def delete(self, id: int, user: User):
        if user.is_manager:
            db_obj = self.db_session.get(Anime, id)
            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )


def get_service(db_session: Session = Depends(get_session)) -> AnimeService:
    print("Get service...")
    return AnimeService(db_session)
