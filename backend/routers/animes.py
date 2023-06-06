from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    Form,
    UploadFile,
)
from db.schemas import Anime, AnimeCreate, AnimeUpdate
from typing import Optional
from services.animes import (
    AnimeService,
    get_service,
)

router = APIRouter(
    prefix='/animes',
    tags=["Animes"]
)


@router.get("/all", response_model=list[Anime])
async def get_all(
    service: AnimeService = Depends(get_service),
):
    return service.list()


@router.get("/search", response_model=list[Anime])
async def search(
    query: str,
    service: AnimeService = Depends(get_service),
):
    if query.strip() == "":
        return []
    else:
        return service.search(query)


@router.post("/add")
async def add(
    anime: AnimeCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: AnimeService = Depends(get_service),
):
    return service.create(anime, poster_img)


@router.put("/update/{id}")
async def update(
    id: int,
    anime: AnimeUpdate = Form(...),
    poster_img: Optional[UploadFile] = File(None),
    service: AnimeService = Depends(get_service),
):
    print("Begin update route")
    return service.update(id, anime, poster_img)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: AnimeService = Depends(get_service),
):
    return service.delete(id)


@router.get("/{id}", response_model=Anime)
async def get(
    id: int,
    service: AnimeService = Depends(get_service),
):
    return service.get(id)
