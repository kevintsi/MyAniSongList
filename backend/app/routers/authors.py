from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    UploadFile,
    status
)
from typing import Optional

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.db.models import User
from app.db.schemas.authors import *
from .users import get_current_user
from app.services.authors import (
    AuthorService,
    get_service,
)

router = APIRouter(
    prefix='/authors',
    tags=["Authors"]
)


@router.get("/all", response_model=Page[Author])
async def get_all(
    service: AuthorService = Depends(get_service),
):
    return paginate(service.db_session, service.list())


@router.get("/search", response_model=Page[Author])
async def search(
    query: str,
    service: AuthorService = Depends(get_service),
):
    return paginate(service.db_session, service.search(query))


@router.post("/add", response_model=Author, status_code=status.HTTP_201_CREATED)
async def add(
    author: AuthorCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: AuthorService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(author, poster_img, current_user)


@router.put("/update/{id}", response_model=Author)
async def update(
    id: int,
    author: AuthorUpdate = Body(...),
    poster_img: Optional[UploadFile] = File(None),
    service: AuthorService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(id, author, poster_img, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: AuthorService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete(id, current_user)


@router.get("/{id}", response_model=Author)
async def get(
    id: int,
    service: AuthorService = Depends(get_service),
):
    return service.get(id)
