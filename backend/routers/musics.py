from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    UploadFile,
)
from db.schemas import *
from typing import List, Optional
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
