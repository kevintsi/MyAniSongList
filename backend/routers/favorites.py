from fastapi import APIRouter
from fastapi.params import Depends
from db.schemas.musics import MusicShort
from db.models import User
from routers.users import get_current_user
from db.schemas.musics import Music

from services.musics import MusicService, get_service


router = APIRouter(
    prefix='/favorites',
    tags=["Favorites"]
)


@router.get("/all", response_model=list[Music])
async def get_all(
    service: MusicService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_favorites(current_user)


@router.get("/users/{id_user}", response_model=list[MusicShort])
async def get_all(
    id_user: int,
    service: MusicService = Depends(get_service),
):
    return service.get_user_favorites(id_user)


@router.post("/{id_music}")
async def add(
    id_music: str,
    service: MusicService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.add_to_favorite(id_music, current_user)


@router.delete("/{id_music}")
async def delete(
    id_music: str,
    service: MusicService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.remove_from_favorite(id_music, current_user)
