from datetime import datetime
from app.db.session import get_session
from fastapi import Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models import Music, Notification, User
from app.db.schemas.notifications import NotificationCreate, Notification as NotificationSchema

from .base import BaseService

class NotificationService(BaseService[Notification, NotificationCreate,None]):
    def __init__(self, db_session: Session):
        super(NotificationService, self).__init__(Notification, db_session)

    def create(self, notification : NotificationCreate):
        music_db : Music | None = self.db_session.get(Music, notification.music_id)
        user_db : User | None = self.db_session.get(User, notification.user_id)

        if music_db is None or user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music or user not found")
        
        try:
            notif_db : Notification = Notification(
                creation_date = datetime.now(),
                is_read = False,
                user = user_db,
                music = music_db,
            )

            self.db_session.add(notif_db)
            self.db_session.commit()

            return NotificationSchema(
                id=notif_db.id,
                music_name=notif_db.music.name,
                music_id=notif_db.music_id,
                creation_date=notif_db.creation_date,
                is_read=notif_db.is_read
            )

        except IntegrityError as e:
            self.db_session.rollback()
            print(f"Error : {e} ")
     
    def list(self, curr_user : User):
        notifs : list[NotificationSchema]= []
        res = self.db_session.scalars(
            select(Notification).
            where(Notification.user_id == curr_user.id).
            order_by(Notification.creation_date.desc())
        ).all()

        for notif in res:
            notifs.append(NotificationSchema(
                id=notif.id,
                music_id=notif.music_id,
                music_name=notif.music.name,
                creation_date=notif.creation_date,
                is_read=notif.is_read
            ))

        return notifs

    def update(self, curr_user : User, id : int):
        notif = self.db_session.get(Notification, id)
        if notif is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

        setattr(notif, "is_read", True)
        
        try:
            self.db_session.commit()

            return NotificationSchema(
                id=notif.id,
                music_id=notif.music_id,
                user_id=notif.user_id,
                creation_date=notif.creation_date,
                is_read=notif.is_read
            )
            
        except IntegrityError as e:
            self.db_session.rollback()
            print(f"Integrity error : {e}")

def get_service(db_session: Session = Depends(get_session)) -> NotificationService:
    print("Get service...")
    return NotificationService(db_session)