from datetime import datetime
import json
from fastapi import Depends, HTTPException
from app.db.schemas.music_requests import (
    CreateMusicRequest,
    MusicRequest
)
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from app.db.models import User, Type
from app.db.schemas.users import User as UserSchema
from app.db.session import get_session
from app.db.models import RequestMusic
from app.services.base import BaseService
from sqlalchemy.orm import Session
from fastapi import status

class MusicRequestService(BaseService[RequestMusic, CreateMusicRequest, None]):
    def __init__(self, db_session: Session):
        super(MusicRequestService, self).__init__(RequestMusic, db_session)

    def get_all(self):
        return self.db_session.scalars(select(RequestMusic)).all()
    
    def create_request(self, music_req : MusicRequest, curr_user : UserSchema):
        type : Type | None = self.db_session.get(Type, music_req.type_id)
        user : User = self.db_session.get(User, curr_user.id)
        
        if type is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Type not found")
        
        music_req_db = RequestMusic(
            creation_date=datetime.now(),
            is_done=False,
            video_id=music_req.video_id,
            music_name=music_req.music_name,
            anime_name=music_req.anime_name,
            artists=json.dumps(music_req.artists),
            user=user,
            type=type
            )
        
        self.db_session.add(music_req_db)
        try:
            self.db_session.commit()
            
            return MusicRequest(
            id=music_req_db.id,
            creation_date=datetime.now(),
            is_done=music_req_db.is_done,
            video_id=music_req_db.video_id,
            music_name=music_req_db.music_name,
            anime_name=music_req_db.anime_name,
            artists=json.loads(music_req_db.artists),
            type_id=music_req_db.type_id
            )
        except IntegrityError as e:
            self.db_session.rollback()
            print(f"Error : {e}")
    
    def update_request(self, id : int):
        req_music : RequestMusic | None = self.db_session.get(RequestMusic, id)
        
        if req_music is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Request music with this id not found")
        
        try:
            stmt = (
                update(RequestMusic).
            where(RequestMusic.id == id).
            values(is_done=True)
            )

            self.db_session.execute(stmt)

            return req_music
        except IntegrityError as e:
            self.db_session.rollback()
            print(f"Error : {e}")

    def delete(self, id : int):
        req_music : RequestMusic | None = self.db_session.get(RequestMusic, id)
        
        if req_music is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Request music with this id not found")
        
        try:
            self.db_session.delete(req_music)
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            print(f"Error : {e}")

def get_service(db_session: Session = Depends(get_session)) -> MusicRequestService:
    return MusicRequestService(db_session)
