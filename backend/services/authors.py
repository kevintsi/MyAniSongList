from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from db.schemas import AuthorCreate, AuthorUpdate
from starlette.exceptions import HTTPException
from db.models import Author
from .base import BaseService
from db.session import get_session
import sqlalchemy
from firebase import bucket


class AuthorService(BaseService[Author, AuthorCreate, AuthorUpdate]):
    def __init__(self, db_session: Session):
        super(AuthorService, self).__init__(Author, db_session)

    def create(self, obj: AuthorCreate, poster_img: UploadFile):
        # if not os.path.exists("static/author_poster_images"):
        #     os.makedirs("static/author_poster_images")

        # with open(f"static/author_poster_images/{poster_img.filename}", "wb") as f:
        #     f.write(poster_img.file.read())

        blob = bucket.blob(f"artist_poster_images/{poster_img.filename}")
        blob.upload_from_file(poster_img.file, content_type="image/png")
        blob.make_public()

        db_obj: Author = Author(
            name=obj.name,
            poster_img=blob.public_url,
        )

        print(f"converted to Author model : ${db_obj}")
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

    def update(self, id, obj: AuthorUpdate, poster_img: UploadFile):
        # if not os.path.exists("static/profile_pictures"):
        #     os.makedirs("static/profile_pictures")

        # with open(f"static/profile_pictures/{pfp.filename}", "wb") as f:
        #     f.write(pfp.file.read())

        blob = bucket.blob(f"artist_poster_images/{poster_img.filename}")
        blob.upload_from_file(poster_img.file, content_type="image/png")
        blob.make_public()

        stmt = (
            sqlalchemy.update(Author)
            .where(Author.id == id)
            .values(
                name=obj.name,
                poster_img=blob.public_url
            )
        )
        print(stmt)

        self.db_session.execute(stmt)
        self.db_session.commit()


def get_service(db_session: Session = Depends(get_session)) -> AuthorService:
    return AuthorService(db_session)
