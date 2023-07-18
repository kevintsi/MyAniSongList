from fastapi import APIRouter
from fastapi.params import Depends
from db.models import User
from routers.users import get_current_user

from services.musics import MusicService, get_service


router = APIRouter(
    prefix='/favorites',
    tags=["Favorites"]
)


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
