from fastapi import (
    APIRouter,
    Depends,
)
from db.schemas.languages import Language, LanguageCreate, LanguageUpdate
from services.languages import LanguageService, get_service

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


@router.post("/add")
async def add(
    language: LanguageCreate,
    service: LanguageService = Depends(get_service)
):
    return service.create(language)


@router.put("/update/{id}")
async def update(
    id: int,
    language: LanguageUpdate,
    service: LanguageService = Depends(get_service),
):
    return service.update(id, language)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: LanguageService = Depends(get_service),
):
    return service.delete(id)
