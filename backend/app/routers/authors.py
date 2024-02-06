from fastapi import (
    APIRouter,
    Depends,
    File,
    Body,
    UploadFile,
    status
)
from typing import Annotated

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
    service: Annotated[AuthorService, Depends(get_service)],
) -> Page[Author]:
    """

    **Route to get all authors with pages**

    **Args:**

        service (AuthorService, Depends): Author service

    **Returns:**

        Page[Author]: Authors with pages
    """
    return paginate(service.db_session, service.list())


@router.get("/search", response_model=Page[Author])
async def search(
    query: str,
    service: Annotated[AuthorService, Depends(get_service)],
) -> Page[Author]:
    """

    **Route to retrieve authors containing query parameter

    **Args:**

        query (str): Author searched_
        service (Annotated[AuthorService, Depends): Author service

    **Returns:**

        Page[Author]: Authors matching criteria with pages
    """
    return paginate(service.db_session, service.search(query))


@router.post("/add", response_model=Author, status_code=status.HTTP_201_CREATED)
async def add(
    author: Annotated[AuthorCreate, Body(embed=True)],
    poster_img: UploadFile,
    service: Annotated[AuthorService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Author:
    """

    **Route to create a new author**

    **Args:**

        service (Annotated[AuthorService, Depends): Author service
        current_user (Annotated[User, Depends): Get user using the token in the header
        author (Annotated[AuthorCreate, Body]): Author create schema
        poster_img (UploadFile): Poster image

    **Returns:**

        Author: Created author
    """
    return service.create(author, poster_img, current_user)


@router.put("/update/{id}", response_model=Author)
async def update(
    id: int,
    author: Annotated[AuthorUpdate, Body(embed=True)],
    service: Annotated[AuthorService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    poster_img: UploadFile | None = None,
) -> Author:
    """

    **Route to update an author**

    **Args:**

        id (int): Author id
        service (Annotated[AuthorService, Depends): Author service
        current_user (Annotated[User, Depends): Get user using the token in the header
        author (Annotated[AuthorUpdate, Body): Author update schema.
        poster_img (UploadFile | None, optional): Optional poster image

    **Returns:**

        Author: Updated author
    """
    return service.update(id, author, poster_img, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: Annotated[AuthorService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """

    **Route to delete an author**

    **Args:**

        id (int): Author id
        service (Annotated[AuthorService, Depends): Author service
        current_user (Annotated[User, Depends): Get user using the token in the header
    """
    return service.delete(id, current_user)


@router.get("/{id}", response_model=Author)
async def get(
    id: int,
    service: Annotated[AuthorService, Depends(get_service)],
) -> Author:
    """

    **Route to get author by id**

    **Args:**

        id (int): Author id
        service (Annotated[AuthorService, Depends): Author service

    **Returns:**

        Author: Author retrieved
    """
    return service.get(id)
