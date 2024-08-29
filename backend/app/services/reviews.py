from datetime import datetime

import sqlalchemy
from app.db.models import Music, Review, User
from app.db.schemas.reviews import ReviewCreate, ReviewUpdate
from app.db.session import get_session
from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from .base import BaseService


class ReviewService(BaseService[Review, ReviewCreate, ReviewUpdate]):
    def __init__(self, db_session: Session):
        super(ReviewService, self).__init__(Review, db_session)

    def list(self):
        return select(Review)

    def get_user_review(self, id_music, id_user):
        review = self.db_session.scalars(
            select(Review).filter(
                Review.music_id == id_music, Review.user_id == id_user
            )
        ).first()
        return review

    def create(self, obj: ReviewCreate, id_user):

        user: User | None = self.db_session.get(User, id_user)
        music: Music | None = self.db_session.get(Music, obj.music_id)

        if not user or not music:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User or Music not found",
            )

        db_obj: Review = Review(
            note_visual=obj.note_visual,
            note_music=obj.note_music,
            creation_date=datetime.now(),
            music=music,
            user=user,
            description=obj.description,
        )

        user_review: Review | None = self.db_session.scalars(
            select(Review).filter(
                Review.user_id == id_user, Review.music_id == obj.music_id
            )
        ).first()
        try:
            if user_review:
                user_review.note_visual = obj.note_visual
                user_review.note_music = obj.note_music
                user_review.description = obj.description
                self.db_session.commit()
                self.calculate_note(user_review)
                db_obj = user_review
            else:
                print(f"converted to Review model : {db_obj}")
                self.db_session.add(db_obj)
                self.db_session.commit()
                self.calculate_note(db_obj)

            self.db_session.commit()
            print("NEW REVIEW MUSIC UPDATED : ", db_obj.music)
            print("End create or update review successfully")
            print(db_obj)
            return db_obj
        except sqlalchemy.exc.IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conflict Error",
                )
            else:
                raise e

    def calculate_note(self, obj: Review):
        music: Music = self.db_session.scalars(
            select(Music).filter(Music.id == obj.music_id)
        ).first()

        total_sum = self.db_session.scalars(
            select(
                sqlalchemy.func.sum(Review.note_visual + Review.note_music)
            ).filter(Review.music_id == music.id)
        ).first()

        reviews_count = self.db_session.scalars(
            select(sqlalchemy.func.count(Review.id)).filter(
                Review.music_id == music.id
            )
        ).first()

        print(f"Count : {reviews_count}")
        print(f"Music avg note empy ? {total_sum is None}")
        print(f"Total sum = {total_sum}")

        new_avg_note = total_sum / (reviews_count * 2)

        print(f"New avg_note : {new_avg_note}")

        music.avg_note = new_avg_note

    def get_music_review(self, id_music: int):
        return select(Review).filter(
            Review.music_id == id_music, Review.description != ""
        )

    def update(self, id, obj: ReviewUpdate, user: User):

        db_obj: Review = self.db_session.get(Review, id)

        if db_obj.user.id == user.id or user.is_manager:
            music: Music = self.db_session.get(Music, obj.music_id)

            if music.avg_note is not None:
                new_avg_note = (
                    music.avg_note + (obj.note_visual + obj.note_music)
                ) / 2

                music.avg_note = new_avg_note

            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)
            self.db_session.commit()
            return db_obj
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )

    def delete(self, id: int, user: User) -> None:
        db_obj: Review = self.db_session.get(Review, id)

        if db_obj.user.id == user.id or user.is_manager:
            self.db_session.delete(db_obj)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )


def get_service(db_session: Session = Depends(get_session)) -> ReviewService:
    return ReviewService(db_session)
