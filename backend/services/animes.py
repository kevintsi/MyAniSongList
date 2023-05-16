from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from db.schemas import AnimeCreate, AnimeUpdate, UserUpdate
from starlette.exceptions import HTTPException
from db.models import Anime
from .base import BaseService
from db.session import get_session
import sqlalchemy
from firebase import bucket


class AnimeService(BaseService[Anime, AnimeCreate, AnimeUpdate]):
    def __init__(self, db_session: Session):
        super(AnimeService, self).__init__(Anime, db_session)

    def create(self, obj: AnimeCreate, poster_img: UploadFile):
        # if not os.path.exists("static/poster_images"):
        #     os.makedirs("static/poster_images")

        # with open(f"static/poster_images/{poster_img.filename}", "wb") as f:
        #     f.write(poster_img.file.read())

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
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        print("End create")
        return db_obj

    def update(self, id, obj: AnimeUpdate, poster_img: UploadFile):
        # if not os.path.exists("static/profile_pictures"):
        #     os.makedirs("static/profile_pictures")

        # with open(f"static/profile_pictures/{pfp.filename}", "wb") as f:
        #     f.write(pfp.file.read())

        blob = bucket.blob(f"anime_poster_images/{poster_img.filename}")
        blob.upload_from_file(poster_img.file, content_type="image/png")
        blob.make_public()

        stmt = (
            sqlalchemy.update(Anime)
            .where(Anime.id == id)
            .values(
                name=obj.name,
                description=obj.description,
                poster_img=blob.public_url
            )
        )
        print(stmt)

        self.db_session.execute(stmt)
        self.db_session.commit()


def get_service(db_session: Session = Depends(get_session)) -> AnimeService:
    return AnimeService(db_session)
