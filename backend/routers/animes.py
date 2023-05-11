from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
)
from db.schemas import *
from typing import List
from services.animes import (
    AnimeService,
    get_service,
)

router = APIRouter(
    prefix='/animes',
    tags=["Animes"]
)


@router.get("/all", response_model=List[Anime])
async def get_all(
    service: AnimeService = Depends(get_service),
):
    return service.list()


@router.post("/add", response_model=Anime)
async def add(
    anime: AnimeCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: AnimeService = Depends(get_service),
):
    return service.create(anime, poster_img)


@router.put("/update/{id}", response_model=Anime)
async def update(
    id: int,
    anime: AnimeUpdate = Body(...),
    poster_img: UploadFile = File(...),
    service: AnimeService = Depends(get_service),
):
    anime.poster_img = poster_img.filename
    return service.update(id, anime)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: AnimeService = Depends(get_service),
):
    return service.delete(id)


@router.get("/{id}")
async def get(
    id: int,
    service: AnimeService = Depends(get_service),
):
    anime: Anime = service.get(id)
    print(str(anime.music[0]))
    return service.get(id)
