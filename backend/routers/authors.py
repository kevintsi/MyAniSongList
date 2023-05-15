from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    UploadFile,
)
from db.schemas import *
from typing import List
from services.authors import (
    AuthorService,
    get_service,
)

router = APIRouter(
    prefix='/authors',
    tags=["Authors"]
)


@router.get("/all", response_model=List[Author])
async def get_all(
    service: AuthorService = Depends(get_service),
):
    return service.list()


@router.post("/add", response_model=Author)
async def add(
    author: AuthorCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: AuthorService = Depends(get_service),
):
    return service.create(author, poster_img)


@router.put("/update/{id}", response_model=Author)
async def update(
    id: int,
    author: AuthorUpdate = Body(...),
    poster_img: UploadFile = File(...),
    service: AuthorService = Depends(get_service),
):
    author.poster_img = poster_img.filename
    return service.update(id, author)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: AuthorService = Depends(get_service),
):
    return service.delete(id)


@router.get("/{id}")
async def get(
    id: int,
    service: AuthorService = Depends(get_service),
):
    return service.get(id)
