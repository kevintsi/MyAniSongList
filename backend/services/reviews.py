from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends
from db.schemas.reviews import ReviewCreate, ReviewUpdate
from starlette.exceptions import HTTPException
from db.models import Music, Review, User
from .base import BaseService
from db.session import get_session
import sqlalchemy


class ReviewService(BaseService[Review, ReviewCreate, ReviewUpdate]):
    def __init__(self, db_session: Session):
        super(ReviewService, self).__init__(Review, db_session)

    def get_user_review(self, id_music, id_user):
        review = self.db_session.query(Review).filter(
            Review.music_id == id_music, Review.user_id == id_user).first()
        return review

    def create(self, obj: ReviewCreate, id_user):
        db_obj: Review = Review(
            note_visual=obj.note_visual,
            note_music=obj.note_music,
            creation_date=datetime.now(),
            music_id=obj.music_id,
            user_id=id_user,
            description=obj.description
        )

        user_review = self.db_session.query(Review).filter(
            Review.user_id == id_user, Review.music_id == obj.music_id).first()
        try:
            if user_review:
                user_review.note_visual = obj.note_visual
                user_review.note_music = obj.note_music
                user_review.description = obj.description
                self.db_session.commit()
                self.calculate_note(user_review)
            else:
                print(f"converted to Review model : {db_obj}")
                self.db_session.add(db_obj)
                self.db_session.commit()
                self.calculate_note(db_obj)

            print("NEW REVIEW MUSIC UPDATED : ", db_obj.music)
            print("End create or update review successfully")

        except sqlalchemy.exc.IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=409, detail="Conflict Error")
            else:
                raise e

    def calculate_note(self, obj: Review):
        music: Music = self.db_session.query(
            Music).filter(Music.id == obj.music_id).first()

        total_sum = self.db_session.query(sqlalchemy.func.sum(
            Review.note_visual+Review.note_music)).filter(Review.music_id == music.id).scalar()

        reviews_count = self.db_session.query(Review).filter(
            Review.music_id == music.id).count()

        print(f"Count : {reviews_count}")
        print(f"Music avg note empy ? {total_sum is None}")
        print(f"Total sum = {total_sum}")

        new_avg_note = total_sum/(reviews_count * 2)

        print(f"New avg_note : {new_avg_note}")

        music.avg_note = new_avg_note

    def get_music_review(self, id_music: int):
        return self.db_session.query(Review).filter(Review.music_id == id_music, Review.description != "")

    def update(self, id, obj: ReviewUpdate, user: User):

        db_obj: Review = self.db_session.get(Review, id)

        if db_obj.user.id == user.id or user.is_manager:
            music: Music = self.db_session.query(Music).get(obj.music_id)

            if music.avg_note is not None:
                new_avg_note = (music.avg_note +
                                (obj.note_visual + obj.note_music)) / 2

                music.avg_note = new_avg_note

            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            self.db_session.commit()
        else:
            raise HTTPException(status_code=401, detail="Forbidden")

    def delete(self, id: int,  user: User) -> None:
        db_obj: Review = self.db_session.query(Review).get(id)

        if db_obj.user.id == user.id or user.is_manager:
            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(status_code=401, detail="Forbidden")


def get_service(db_session: Session = Depends(get_session)) -> ReviewService:
    return ReviewService(db_session)
