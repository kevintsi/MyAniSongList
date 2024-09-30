from datetime import datetime
from pydantic import BaseModel


class NotificationBase(BaseModel):
    music_id : int
    user_id : int

class NotificationCreate(NotificationBase):
    pass

class Notification(BaseModel):
    id : int
    music_id : int
    music_name : str
    creation_date : datetime
    is_read : bool