from app.db.models import User
from app.db.schemas.reviews import Review, ReviewCreate, ReviewUpdate
from app.services.reviews import ReviewService, get_service
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from .users import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/all", response_model=Page[Review])
async def get_all(
    service: ReviewService = Depends(get_service),
):
    return paginate(service.db_session, service.list())


@router.get("/{id}", response_model=Review)
async def get(
    id: int,
    service: ReviewService = Depends(get_service),
):
    return service.get(id)


@router.get("/user/music/{id_music}", response_model=Review | None)
async def get_user_review_by_music(
    id_music: int,
    service: ReviewService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_user_review(id_music, current_user.id)


@router.get("/music/{id_music}", response_model=Page[Review])
async def get_music_reviews(
    id_music: int,
    service: ReviewService = Depends(get_service),
):
    return paginate(service.db_session, service.get_music_review(id_music))


@router.post(
    "/add", status_code=status.HTTP_201_CREATED, response_model=Review
)
async def add(
    review: ReviewCreate,
    service: ReviewService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    return service.create(review, current_user.id)


@router.put("/update/{id}", response_model=Review)
async def update(
    id: int,
    review: ReviewUpdate,
    service: ReviewService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(id, review, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: ReviewService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(id, current_user)
