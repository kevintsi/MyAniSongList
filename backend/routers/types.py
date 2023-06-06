from fastapi import (
    APIRouter,
    Depends,
)
from db.schemas import *
from services.types import (
    TypeService,
    get_service,
)

router = APIRouter(
    prefix='/types',
    tags=["Types"]
)


@router.get("/all", response_model=list[Type])
async def get_all(
    service: TypeService = Depends(get_service),
):
    return service.list()


@router.post("/add", response_model=Type)
async def add(
    type: TypeCreate,
    service: TypeService = Depends(get_service),
):
    return service.create(type)


@router.put("/update/{id}", response_model=Type)
async def update(
    id: int,
    type: TypeUpdate,
    service: TypeService = Depends(get_service),
):
    return service.update(id, type)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: TypeService = Depends(get_service),
):
    return service.delete(id)


@router.get("/{id}", response_model=Type)
async def get(
    id: int,
    service: TypeService = Depends(get_service),
):
    return service.get(id)
