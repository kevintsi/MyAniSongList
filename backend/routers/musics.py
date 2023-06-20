from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    UploadFile,
)
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from db.schemas import *
from typing import Optional
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
):
    return paginate(service.list())


@router.get("/search", response_model=list[Music])
async def search(
    query: str,
    service: MusicService = Depends(get_service),
):
    if query.strip() == "":
        return []
    else:
        return service.search(query)


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
):
    return service.create(music, poster_img)


@router.put("/update/{id}")
async def update(
    id: int,
    music: MusicUpdate = Body(...),
    poster_img: Optional[UploadFile] = File(None),
    service: MusicService = Depends(get_service),
):
    return service.update(id, music, poster_img)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: MusicService = Depends(get_service),
):
    return service.delete(id)


@router.get("/{id}", response_model=Music)
async def get(
    id: int,
    service: MusicService = Depends(get_service),
):
    return service.get(id)
