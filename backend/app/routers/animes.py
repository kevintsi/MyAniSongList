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
from app.db.models import User
from app.db.schemas.animes import Anime, AnimeCreate, AnimeTranslationCreate, AnimeUpdate
from typing import List, Optional
from .users import get_current_user
from app.services.animes import (
    AnimeService,
    get_service,
)

router = APIRouter(
    prefix='/animes',
    tags=["Animes"]
)


@router.get("/all", response_model=Page[Anime])
async def get_all(
    lang: str,
    service: AnimeService = Depends(get_service),
):
    res = service.list(lang)
    return paginate(res,
                    transformer=lambda items: [
                        Anime(
                            id=row.AnimeTranslation.id_anime,
                            description=row.AnimeTranslation.description,
                            poster_img=row.Anime.poster_img,
                            name=row.AnimeTranslation.name).dict() for row in items
                    ])


@router.get("/search", response_model=Page[Anime])
async def search(
    lang: str,
    query: str,
    service: AnimeService = Depends(get_service),
):
    res = service.search(query, lang)
    return paginate(res,
                    transformer=lambda items: [
                        Anime(
                            id=row.AnimeTranslation.id_anime,
                            description=row.AnimeTranslation.description,
                            poster_img=row.Anime.poster_img,
                            name=row.AnimeTranslation.name).dict() for row in items
                    ])


@router.post("/add")
async def add(
    anime: AnimeCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: AnimeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(anime, poster_img, current_user)


@router.post("/{id}/add_translation/")
async def add_translation(
    id: int,
    lang: str,
    anime: AnimeTranslationCreate,
    service: AnimeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create_translation(anime, id, lang, current_user)


@router.put("/update/{id}")
async def update(
    lang: str,
    id: int,
    anime: AnimeUpdate = Form(...),
    poster_img: Optional[UploadFile] = File(None),
    service: AnimeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    print("Begin update route")
    return service.update(id, anime, poster_img, lang, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: AnimeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete(id, current_user)


@router.get("/{id}", response_model=Anime | None)
async def get(
    lang: str,
    id: int,
    service: AnimeService = Depends(get_service),
):
    return service.get(id, lang)
