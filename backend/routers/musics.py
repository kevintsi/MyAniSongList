from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    UploadFile,
)
from db.schemas import *
from typing import List
from services.musics import (
    MusicService,
    get_service,
)

router = APIRouter(
    prefix='/musics',
    tags=["Musics"]
)


@router.get("/all", response_model=List[Music])
async def get_all(
    service: MusicService = Depends(get_service),
):
    return service.list()


@router.post("/add", response_model=Music)
async def add(
    music: MusicCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: MusicService = Depends(get_service),
):
    return service.create(music, poster_img)


@router.put("/update/{id}", response_model=Music)
async def update(
    id: int,
    music: MusicUpdate = Body(...),
    poster_img: UploadFile = File(...),
    service: MusicService = Depends(get_service),
):
    music.poster_img = poster_img.filename
    return service.update(id, music)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: MusicService = Depends(get_service),
):
    return service.delete(id)


@router.get("/{id}")
async def get(
    id: int,
    service: MusicService = Depends(get_service),
):
    return service.get(id)
