from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    Query,
    UploadFile,
    status
)
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.db.models import User
from app.services.musics import OrderMusicBy
from app.db.schemas.musics import (
    MusicAnime,
    MusicArtist,
    MusicCreate,
    MusicSearch,
    MusicShort,
    MusicUpdate,
    Music
)
from typing import Annotated

from app.db.schemas.types import Type
from .users import get_current_user
from app.services.musics import (
    MusicService,
    get_service,
)

router = APIRouter(
    prefix='/musics',
    tags=["Musics"]
)


@router.get("/all", response_model=Page[MusicSearch])
async def get_all(
    service: Annotated[MusicService, Depends(get_service)],
    order_by: OrderMusicBy = Query(None, description="Order items by")
) -> Page[MusicSearch]:
    """

    **Route to get all musics with page format**

    **Args:**
        service (Annotated[MusicService, Depends]): Music service
        order_by (OrderMusicBy, optional): Order items by

    **Returns:**

        Page[MusicSearch]: List of musics with page format
    """
    return paginate(service.db_session, service.list(order_by))


@router.get("/latest", response_model=list[MusicShort])
async def get_latest(
    service: Annotated[MusicService, Depends(get_service)]
) -> list[MusicShort]:
    """

    **Route to get the 5 latest musics**

    **Args:**

        service (Annotated[MusicService, Depends]): Music service

    **Returns:**

        list[MusicShort]: List of the 5 latest musics
    """
    return service.get_latest()


@router.get("/popular", response_model=list[MusicShort])
async def get_most_popular(
    service: Annotated[MusicService, Depends(get_service)]
) -> list[MusicShort]:
    """

    **Route to get the 5 most popular musics** 

    **Args:**

        service (Annotated[MusicService, Depends]): Music service

    **Returns:**

        list[MusicShort]: List of the 5 most popular musics
    """
    return service.get_most_popular()


@router.get("/search", response_model=Page[MusicSearch])
async def search(
    query: str,
    service: Annotated[MusicService, Depends(get_service)],
) -> Page[MusicSearch]:
    """

    **Route to search for musics matching query parameter**

    **Args:**

        query (str): Music searched
        service (Annotated[MusicService, Depends]): Music service

    **Returns:**

        Page[MusicSearch]: List of musics matching the query parameter with page format
    """
    return paginate(service.db_session, service.search(query))


@router.get("/anime/{id_anime}", response_model=list[MusicAnime])
async def get_musics_by_id_anime(
    lang: str,
    id_anime: int,
    service: Annotated[MusicService, Depends(get_service)],
) -> list[MusicAnime]:
    """

    **Route to get all musics for a given anime and a given language**

    **Args:**

        lang (str): Language code
        id_anime (int): Anime id
        service (Annotated[MusicService, Depends]): Music service

    **Returns:**

        list[MusicAnime]: List of all musics for the given anime and given language
    """
    return service.get_musics_anime(id_anime, lang)


@router.get("/artist/{id_artist}", response_model=list[MusicArtist])
async def get_musics_by_id_artist(
    lang: str,
    id_artist: int,
    service: Annotated[MusicService, Depends(get_service)],
) -> list[MusicArtist]:
    """

    **Route to get all musics for a given artist and a given language**

    **Args:**

        lang (str): Language code
        id_artist (int): Artist id
        service (Annotated[MusicService ,Depends]): Music service

    **Returns:**

        list[MusicArtist]: List of all musics for the given artist and given language
    """
    return service.get_musics_artist(id_artist, lang)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=Music)
async def add(
    music: Annotated[MusicCreate, Body(embed=True)],
    poster_img: UploadFile,
    service: Annotated[MusicService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """

    **Route to add a new music**

    **Args:**

        poster_img (UploadFile): Poster image
        service (Annotated[MusicService, Depends]): Music service
        current_user (Annotated[User, Depends]): Get user using the token in the header
        music (Annotated[MusicCreate, Body): Music create schema

    **Returns:**

        Music: Created music
    """
    return service.create(music, poster_img, current_user)


@router.put("/update/{id}", response_model=Music)
async def update(
    id: int,
    music: Annotated[MusicUpdate, Body(embed=True)],
    service: Annotated[MusicService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    poster_img: UploadFile | None = None,
) -> Music:
    """

    **Route to update a given music**

    **Args:**

        id (int): Music id
        music (MusicUpdate, Body): Music update schema
        service (Annotated[MusicService, Depends): Music service
        current_user (Annotated[User, Depends): Get user using the token in the header
        poster_img (UploadFile | None, optional): Optional poster image

    **Returns:**

        Music: Updated music
    """
    return service.update(id, music, poster_img, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: Annotated[MusicService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """

    **Route to delete a given music**

    **Args:**

        id (int): Music id
        service (Annotated[MusicService, Depends]): Music id
        current_user (Annotated[User, Depends]): Get user using the token in the header
    """
    service.delete(id, current_user)


@router.get("/{id}", response_model=Music)
async def get(
    lang: str,
    id: int,
    service: Annotated[MusicService, Depends(get_service)],
) -> Music:
    """

    **Route to get a given music with a given language**

    **Args:**

        lang (str): Language code
        id (int): Music id
        service (Annotated[MusicService, Depends]): Music service

    **Returns:**

        Music: Retrieved music
    """
    return service.get(id, lang)
