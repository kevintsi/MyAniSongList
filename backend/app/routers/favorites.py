from typing import Annotated
from fastapi import APIRouter, status
from fastapi.params import Depends
from app.db.schemas.musics import MusicShort
from app.db.models import User
from .users import get_current_user
from app.db.schemas.musics import Music

from app.services.musics import MusicService, get_service


router = APIRouter(
    prefix='/favorites',
    tags=["Favorites"]
)


@router.get("/all", response_model=list[Music])
async def get_all(
    service: Annotated[MusicService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[Music]:
    """

    **Route to get favorites musics of the current user logged in**

    **Args:**

        service (Annotated[MusicService , Depends]): Music service
        current_user (Annotated[User , Depends]): Get user using the token in the header

    **Returns:**

        list[Music]: List of user's favorites musics
    """
    return service.get_favorites(current_user)


@router.get("/users/{id_user}", response_model=list[MusicShort])
async def get_user_all(
    id_user: int,
    service: Annotated[MusicService, Depends(get_service)],
) -> list[MusicShort]:
    """

    **Route to get a given user's favorites musics**

    **Args:**

        id_user (int): User id
        service (Annotated[MusicService, Depends]): Music service

    **Returns:**

        list[MusicShort]: List of a given user's favorites musics
    """
    return service.get_user_favorites(id_user)


@router.post("/{id_music}", status_code=status.HTTP_201_CREATED)
async def add(
    id_music: str,
    service: Annotated[MusicService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """

    **Route to add a given music to current user's favorites musics**

    **Args:**

        id_music (str): Music id
        service (Annotated[MusicService, Depends]): Music service
        current_user (Annotated[User, Depends]): Get user using the token in the header
    """
    service.add_to_favorite(id_music, current_user)


@router.delete("/{id_music}")
async def delete(
    id_music: str,
    service: Annotated[MusicService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """

    **Route remove a given music to user's favorites musics**

    **Args:**

        id_music (str): Music id
        service (Annotated[MusicService ,Depends]): Music service
        current_user (Annotated[User , Depends]): Get user using the token in the header
    """
    service.remove_from_favorite(id_music, current_user)
