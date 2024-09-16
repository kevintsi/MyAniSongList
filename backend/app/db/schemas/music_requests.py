from pydantic import BaseModel


class CreateMusicRequest(BaseModel):
    video_id : str
    music_name : str
    anime_name : str
    artists : list[str]
    type_id : int

class MusicRequest(CreateMusicRequest):
    id : int
