from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    Form,
    UploadFile,
)
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from db.models import User
from db.schemas.animes import Anime, AnimeCreate, AnimeUpdate
from typing import List, Optional
from routers.users import get_current_user
from services.animes import (
    AnimeService,
    get_service,
)

router = APIRouter(
    prefix='/animes',
    tags=["Animes"]
)


@router.get("/all", response_model=Page[Anime])
async def get_all(
    service: AnimeService = Depends(get_service),
):
    # fake_data = service.list()*100
    # return paginate(fake_data)
    print("Begin get list anime...")
    return paginate(service.list())


@router.get("/search", response_model=Page[Anime])
async def search(
    query: str,
    service: AnimeService = Depends(get_service),
):
    return paginate(service.search(query))


@router.post("/add")
async def add(
    anime: AnimeCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: AnimeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(anime, poster_img, current_user)


@router.put("/update/{id}")
async def update(
    id: int,
    anime: AnimeUpdate = Form(...),
    poster_img: Optional[UploadFile] = File(None),
    service: AnimeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    print("Begin update route")
    return service.update(id, anime, poster_img, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: AnimeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete(id, current_user)


@router.get("/{id}", response_model=Anime)
async def get(
    id: int,
    service: AnimeService = Depends(get_service),
):
    return service.get(id)
