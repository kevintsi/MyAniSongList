from fastapi import (
    APIRouter,
    Depends,
)
from fastapi_pagination import Page
from app.db.models import User
from fastapi_pagination.ext.sqlalchemy import paginate
from app.db.schemas.reviews import *
from .users import get_current_user
from app.services.reviews import (
    ReviewService,
    get_service,
)

router = APIRouter(
    prefix='/reviews',
    tags=["Reviews"]
)


@router.get("/all", response_model=Page[Review])
async def get_all(
    service: ReviewService = Depends(get_service),
):
    # fake_data = service.list()*100
    # return paginate(fake_data)
    return paginate(service.list())


@router.get("/{id}", response_model=Review)
async def get(
    id: int,
    service: ReviewService = Depends(get_service),
):
    return service.get(id)


@router.get("/user/music/{id_music}", response_model=Review | None)
async def get(
    id_music: int,
    service: ReviewService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_user_review(id_music, current_user.id)


@router.get("/music/{id_music}", response_model=Page[Review])
async def get_music_reviews(
    id_music: int,
    service: ReviewService = Depends(get_service),
):
    # fake_data = service.get_music_review(id_music)*100
    # return paginate(fake_data)
    return paginate(service.get_music_review(id_music))


@router.post("/add")
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
