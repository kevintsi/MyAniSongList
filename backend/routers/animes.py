from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
)
from db.schemas import *
from typing import List
from sqlalchemy.orm import Session
from datetime import timedelta
from services.animes import (
    AnimeService,
    get_anime_service,
)

router = APIRouter(
    prefix='/animes',
    tags=["Animes"]
)


@router.get("/all", response_model=List[Anime])
async def get_all(
    anime_service: AnimeService = Depends(get_anime_service),
):
    return anime_service.list()


@router.post("/add", response_model=Anime)
async def add(
    anime: AnimeCreate = Body(...),
    poster_img: UploadFile = File(...),
    anime_service: AnimeService = Depends(get_anime_service),
):
    return anime_service.create(anime, poster_img)


@router.put("/update/{id}", response_model=Anime)
async def update(
    id: int,
    anime: AnimeUpdate = Body(...),
    poster_img: UploadFile = File(...),
    anime_service: AnimeService = Depends(get_anime_service),
):
    anime.poster_img = poster_img.filename
    return anime_service.update(id, anime)


@router.delete("/delete/{id}")
async def update(
    id: int,
    anime_service: AnimeService = Depends(get_anime_service),
):
    return anime_service.delete(id)


@router.get("/{id}")
async def update(
    id: int,
    anime_service: AnimeService = Depends(get_anime_service),
):
    return anime_service.get(id)
