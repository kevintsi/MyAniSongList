from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    UploadFile,
)
from typing import Optional
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


@router.get("/search", response_model=List[Author])
async def search(
    query: str,
    service: AuthorService = Depends(get_service),
):
    if query.strip() == "":
        return []
    else:
        return service.search(query)


@router.post("/add")
async def add(
    author: AuthorCreate = Body(...),
    poster_img: UploadFile = File(...),
    service: AuthorService = Depends(get_service),
):
    return service.create(author, poster_img)


@router.put("/update/{id}")
async def update(
    id: int,
    author: AuthorUpdate = Body(...),
    poster_img: Optional[UploadFile] = File(None),
    service: AuthorService = Depends(get_service),
):
    return service.update(id, author, poster_img)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: AuthorService = Depends(get_service),
):
    return service.delete(id)


@router.get("/{id}", response_model=Author)
async def get(
    id: int,
    service: AuthorService = Depends(get_service),
):
    return service.get(id)
