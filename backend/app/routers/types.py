from fastapi import (
    APIRouter,
    Depends,
    status
)
from .users import get_current_user
from app.db.models import User
from app.db.schemas.types import *
from app.services.types import (
    TypeService,
    get_service,
)

router = APIRouter(
    prefix='/types',
    tags=["Types"]
)


@router.get("/all", response_model=list[Type])
async def get_all(
    lang: str,
    service: TypeService = Depends(get_service),
):
    return service.list(lang)


@router.post("/add", response_model=Type, status_code=status.HTTP_201_CREATED)
async def add(
    type: TypeCreate,
    service: TypeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(type, current_user)


@router.post("/{id}/add_translation", status_code=status.HTTP_201_CREATED)
async def add_translation(
    id: str,
    type: TypeCreate,
    lang: str,
    service: TypeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.add_translation(type, lang, id, current_user)


@router.put("/update/{id}", response_model=Type)
async def update(
    id: int,
    type: TypeUpdate,
    service: TypeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(id, type, current_user)


@router.put("/{id}/update_translation")
async def update_translation(
    lang: str,
    id: int,
    type: TypeUpdate,
    service: TypeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.update_translation(type, lang, id, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: TypeService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete(id, current_user)


@router.get("/{id}", response_model=Type)
async def get(
    id: int,
    service: TypeService = Depends(get_service),
):
    return service.get(id)


@router.get("/{id}", response_model=Type)
async def get(
    lang: str,
    id: int,
    service: TypeService = Depends(get_service),
):
    return service.get_translation(id, lang)
