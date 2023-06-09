from fastapi import (
    APIRouter,
    Depends,
)
from db.schemas import *
from services.reviews import (
    ReviewService,
    get_service,
)

from fastapi_jwt_auth import AuthJWT

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
    # authorize: AuthJWT = Depends(),
    service: ReviewService = Depends(get_service),
):
    # authorize.jwt_refresh_token_required()
    # current_user = authorize.get_jwt_subject()
    # return service.create(review, current_user)
    id_user = 1
    return service.create(review, id_user)


@router.put("/update/{id}")
async def update(
    id: int,
    review: ReviewUpdate,
    # authorize: AuthJWT = Depends(),
    service: ReviewService = Depends(get_service),
):
    # authorize.jwt_refresh_token_required()
    # current_user = authorize.get_jwt_subject()
    # return service.update(id, current_user, review)
    id_user = 1
    return service.update(id, review, id_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    # authorize: AuthJWT = Depends(),
    service: ReviewService = Depends(get_service),
):
    # authorize.jwt_refresh_token_required()
    # current_user = authorize.get_jwt_subject()
    # return service.delete(id, current_user)
    id_user = 1
    return service.delete(id, id_user)
