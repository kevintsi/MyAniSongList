from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from db.schemas import MusicCreate, MusicUpdate
from starlette.exceptions import HTTPException
from db.models import Music, Author
from .base import BaseService
from db.session import get_session
import sqlalchemy
from firebase import bucket


class MusicService(BaseService[Music, MusicCreate, MusicUpdate]):
    def __init__(self, db_session: Session):
        super(MusicService, self).__init__(Music, db_session)

    def create(self, obj: MusicCreate, poster_img: UploadFile):
        # if not os.path.exists("static/music_poster_images"):
        #     os.makedirs("static/music_poster_images")

        # with open(f"static/music_poster_images/{poster_img.filename}", "wb") as f:
        #     f.write(poster_img.file.read())

        blob = bucket.blob(f"music_poster_images/{poster_img.filename}")
        blob.upload_from_file(poster_img.file, content_type="image/png")
        blob.make_public()

        author: Author = self.db_session.get(Author, obj.author_id)

        db_obj: Music = Music(
            name=obj.name,
            release_date=obj.release_date,
            anime_id=obj.anime_id,
            type_id=obj.type_id,
            poster_img=blob.public_url,
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

    def update(self, id, obj: MusicUpdate, poster_img: UploadFile):
        # if not os.path.exists("static/profile_pictures"):
        #     os.makedirs("static/profile_pictures")

        # with open(f"static/profile_pictures/{pfp.filename}", "wb") as f:
        #     f.write(pfp.file.read())

        blob = bucket.blob(f"music_poster_images/{poster_img.filename}")
        blob.upload_from_file(poster_img.file, content_type="image/png")
        blob.make_public()

        stmt = (
            sqlalchemy.update(Music)
            .where(Music.id == id)
            .values(
                name=obj.name,
                release_date=obj.release_date,
                anime_id=obj.anime_id,
                type_id=obj.type_id,
                poster_img=blob.public_url
            )
        )
        print(stmt)

        self.db_session.execute(stmt)
        self.db_session.commit()


def get_service(db_session: Session = Depends(get_session)) -> MusicService:
    return MusicService(db_session)