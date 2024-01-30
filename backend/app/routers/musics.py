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
from app.db.models import Music, User
from app.services.musics import OrderMusicBy
from app.db.schemas.musics import MusicAnime, MusicArtist, MusicCreate, MusicShort, MusicUpdate, Music
from typing import Optional
from .users import get_current_user
from app.services.musics import (
    MusicService,
    get_service,
)

router = APIRouter(
    prefix='/musics',
    tags=["Musics"]
)


@router.get("/all", response_model=Page[MusicShort])
async def get_all(
    service: MusicService = Depends(get_service),
    order_by: OrderMusicBy = Query(None, description="Order items by")
):
    return paginate(service.db_session, service.list(order_by))


@router.get("/latest", response_model=list[MusicShort])
async def get_latest(
    service: MusicService = Depends(get_service)
):
    return service.get_latest()


@router.get("/popular", response_model=list[MusicShort])
async def get_most_popular(
    service: MusicService = Depends(get_service)
):
    return service.get_most_popular()


@router.get("/search", response_model=Page[MusicShort])
async def search(
    query: str,
    service: MusicService = Depends(get_service),
):
    return paginate(service.search(query))


@router.get("/anime/{id_anime}", response_model=list[MusicAnime])
async def get_musics_by_id_anime(
    lang: str,
    id_anime: int,
    service: MusicService = Depends(get_service),
):
    return service.get_musics_anime(id_anime, lang)


@router.get("/artist/{id_artist}", response_model=list[MusicArtist])
async def get_musics_by_id_artist(
    lang: str,
    id_artist: int,
    service: MusicService = Depends(get_service),
):
    return service.get_musics_artist(id_artist, lang)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=Music)
async def add(
    music: MusicCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: MusicService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(music, poster_img, current_user)


@router.put("/update/{id}", response_model=Music)
async def update(
    id: int,
    music: MusicUpdate = Body(...),
    poster_img: Optional[UploadFile] = File(None),
    service: MusicService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(id, music, poster_img, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: MusicService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete(id, current_user)


@router.get("/{id}", response_model=Music)
async def get(
    lang: str,
    id: int,
    service: MusicService = Depends(get_service),
):
    return service.get(id, lang)
