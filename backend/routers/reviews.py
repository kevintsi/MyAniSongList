from fastapi import (
    APIRouter,
    Depends,
)
from db.schemas import *
from routers.users import get_current_user
from services.reviews import (
    ReviewService,
    get_service,
)

router = APIRouter(
    prefix='/reviews',
    tags=["Reviews"]
)


@router.get("/all", response_model=list[Review])
async def get_all(
    service: ReviewService = Depends(get_service),
):
    return service.list()


@router.get("/{id}", response_model=Review)
async def get(
    id: int,
    service: ReviewService = Depends(get_service),
):
    return service.get(id)


@router.post("/add", response_model=Review)
async def add(
    review: ReviewCreate,
    service: ReviewService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(review, current_user.id)


@router.put("/update/{id}")
async def update(
    id: int,
    review: ReviewUpdate,
    service: ReviewService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(id, review, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: ReviewService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete(id, current_user)
