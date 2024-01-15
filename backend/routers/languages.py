from fastapi import (
    APIRouter,
    Depends,
)
from db.models import User
from db.schemas.languages import Language, LanguageCreate, LanguageUpdate
from services.languages import LanguageService, get_service
from routers.users import get_current_user

router = APIRouter(
    prefix='/languages',
    tags=["Languages"]
)


@router.get("/all", response_model=list[Language])
async def get_all(
    service: LanguageService = Depends(get_service)
):
    return service.list().all()


@router.get("/{id}", response_model=Language)
async def get(
    id: int,
    service: LanguageService = Depends(get_service)
):
    return service.get(id)


@router.get("/animes/{id}", response_model=list[Language])
async def get_languages_by_anime(
    id: int,
    service: LanguageService = Depends(get_service)
):
    return service.get_languages_by_anime(id)


@router.post("/add")
async def add(
    language: LanguageCreate,
    service: LanguageService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(language, current_user)


@router.put("/update/{id}")
async def update(
    id: int,
    language: LanguageUpdate,
    service: LanguageService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(id, language, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: LanguageService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete(id, current_user)
