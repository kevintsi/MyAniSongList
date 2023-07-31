from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    Query,
    UploadFile,
)
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from db.models import User
from services.musics import OrderMusicBy
from db.schemas.musics import *
from typing import Optional
from routers.users import get_current_user
from services.musics import (
    MusicService,
    get_service,
)

router = APIRouter(
    prefix='/musics',
    tags=["Musics"]
)


@router.get("/all", response_model=Page[Music])
async def get_all(
    service: MusicService = Depends(get_service),
    order_by: OrderMusicBy = Query(None, description="Order items by")
):
    # fake_data = service.list()*100
    # return paginate(fake_data)
    return paginate(service.list(order_by))


@router.get("/latest", response_model=List[Music])
async def get_all(
    service: MusicService = Depends(get_service)
):
    return service.get_latest()


@router.get("/popular", response_model=List[Music])
async def get_most_popular(
    service: MusicService = Depends(get_service)
):
    return service.get_most_popular()


@router.get("/search", response_model=Page[Music])
async def search(
    query: str,
    service: MusicService = Depends(get_service),
):
    return paginate(service.search(query))


@router.get("/anime/{id_anime}", response_model=list[Music])
async def get_musics_by_id_anime(
    id_anime: int,
    service: MusicService = Depends(get_service),
):
    return service.get_musics_anime(id_anime)


@router.get("/artist/{id_artist}", response_model=list[MusicArtist])
async def get_musics_by_id_artist(
    id_artist: int,
    service: MusicService = Depends(get_service),
):
    return service.get_musics_artist(id_artist)


@router.post("/add")
async def add(
    music: MusicCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: MusicService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(music, poster_img, current_user)


@router.put("/update/{id}")
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
    id: int,
    service: MusicService = Depends(get_service),
):
    return service.get(id)
