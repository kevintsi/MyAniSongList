from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    UploadFile,
)
from typing import Optional

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from db.schemas import *
from routers.users import get_current_user
from services.authors import (
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
    # fake_data = service.list()*100
    # return paginate(fake_data)
    return paginate(service.list())


@router.get("/search", response_model=Page[Author])
async def search(
    query: str,
    service: AuthorService = Depends(get_service),
):
    return paginate(service.search(query))


@router.post("/add")
async def add(
    author: AuthorCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: AuthorService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(author, poster_img, current_user)


@router.put("/update/{id}")
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
