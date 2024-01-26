from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile, status
from app.db.schemas.animes import AnimeCreate,  AnimeUpdate, Anime as AnimeSchema, AnimeTranslationCreate
from starlette.exceptions import HTTPException
from app.db.models import Anime, AnimeTranslation, Language, User
from .base import BaseService
from app.db.session import get_session
from sqlalchemy import select, exc
from app.firebase import bucket


class AnimeService(BaseService[Anime, AnimeCreate, AnimeUpdate]):
    def __init__(self, db_session: Session):
        super(AnimeService, self).__init__(Anime, db_session)

    def list(self, lang):
        obj_lang = self.db_session.query(Language).filter(
            Language.code == lang).first()
        if obj_lang:
            return self.db_session.query(AnimeTranslation, Anime).join(Anime.anime_translations).where(AnimeTranslation.id_language == obj_lang.id)
        else:
            raise HTTPException(
                status_code=404, detail="Error language")

    def get(self, id: int, lang: str):
        obj_lang = self.db_session.query(Language).filter(
            Language.code == lang).first()

        anime = self.db_session.query(Anime).where(Anime.id == id).first()
        if obj_lang and anime:
            obj = self.db_session.query(AnimeTranslation, Anime).join(
                Anime.anime_translations).where(AnimeTranslation.id_language == obj_lang.id, AnimeTranslation.id_anime == anime.id).first()
            if obj is None:
                return None
            return AnimeSchema(id=obj.AnimeTranslation.id_anime, name=obj.AnimeTranslation.name, description=obj.AnimeTranslation.description, poster_img=obj.Anime.poster_img)
        else:
            raise HTTPException(
                status_code=404, detail="Error language or anime id")

    def search(self, term: str, lang: str):
        lang: Language = self.db_session.query(
            Language).filter(Language.code == lang).first()
        if lang:
            return self.db_session.query(AnimeTranslation, Anime).join(Anime.anime_translations).filter(AnimeTranslation.name.like(f"%{term}%"), AnimeTranslation.id_language == lang.id)
        else:
            raise HTTPException(
                status_code=404, detail="Error language")

    def create(self, obj: AnimeCreate, poster_img: UploadFile, user: User):
        if user.is_manager:
            lang_obj: Language = self.db_session.scalars(
                select(Language).filter(Language.code == "fr")).first()

            if lang_obj:
                blob = bucket.blob(
                    f"anime_poster_images/{poster_img.filename}")
                blob.upload_from_file(
                    poster_img.file, content_type="image/png")
                blob.make_public()
                try:
                    anime: Anime = self.db_session.scalars(select(Anime).filter(
                        Anime.poster_img == blob.public_url)).first()

                    if not anime:
                        anime: Anime = Anime(poster_img=blob.public_url)

                    anime_translation: AnimeTranslation = AnimeTranslation(
                        anime=anime,
                        name=obj.name,
                        description=obj.description,
                        language=lang_obj
                    )

                    print(f"converted to Anime model : {anime_translation}")
                    self.db_session.add(anime_translation)
                    self.db_session.commit()
                    return AnimeSchema(id=anime.id, name=anime_translation.name, description=anime_translation.description, poster_img=anime.poster_img)
                except exc.IntegrityError as e:
                    self.db_session.rollback()
                    if "Duplicate entry" in str(e):
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT, detail="Conflict Error")
                    else:
                        raise e
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Error language")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")

    def create_translation(self, obj: AnimeTranslationCreate, id: int,  lang: str, user: User):
        if user.is_manager:
            lang_obj: Language = self.db_session.query(
                Language).filter(Language.code == lang).first()

            anime: Anime = self.db_session.query(Anime).filter(
                Anime.id == id).first()

            if lang_obj and anime:
                try:
                    anime_translation: AnimeTranslation = AnimeTranslation(
                        anime=anime,
                        name=obj.name,
                        description=obj.description,
                        language=lang_obj
                    )

                    print(
                        f"converted to AnimeTranslation model : {anime_translation}")
                    self.db_session.add(anime_translation)
                    self.db_session.commit()
                except exc.IntegrityError as e:
                    self.db_session.rollback()
                    if "Duplicate entry" in str(e):
                        raise HTTPException(
                            status_code=409, detail="Conflict Error")
                    else:
                        raise e
            else:
                raise HTTPException(
                    status_code=404, detail="Error language or anime id")
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def update(self, id, obj: AnimeUpdate, poster_img: UploadFile, lang: str, user: User):

        if user.is_manager:

            obj_lang: Language = self.db_session.query(
                Language).filter(Language.code == lang).first()

            anime: Anime = self.db_session.get(Anime, id)

            if anime and obj_lang:
                if poster_img:
                    blob = bucket.blob(
                        f"anime_poster_images/{poster_img.filename}")
                    blob.upload_from_file(
                        poster_img.file, content_type="image/png")
                    blob.make_public()

                    anime.poster_img = blob.public_url

                anime_translation: AnimeTranslation = self.db_session.query(AnimeTranslation).filter(
                    AnimeTranslation.id_anime == anime.id, AnimeTranslation.id_language == obj_lang.id).first()

                for col, value in obj.dict(exclude_unset=True).items():
                    setattr(anime_translation, col, value)

                self.db_session.commit()
            else:
                raise HTTPException(404, "Error language or anime id")
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
    print("Get service...")
    return AnimeService(db_session)
