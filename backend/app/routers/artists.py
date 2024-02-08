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
from app.db.schemas.artists import ArtistCreate, ArtistUpdate, Artist
from .users import get_current_user
from app.services.artists import (
    ArtistService,
    get_service,
)

router = APIRouter(
    prefix='/artists',
    tags=["artists"]
)


@router.get("/all", response_model=Page[Artist])
async def get_all(
    service: Annotated[ArtistService, Depends(get_service)],
) -> Page[Artist]:
    """

    **Route to get all artists with pages**

    **Args:**

        service (artistService, Depends): Artist service

    **Returns:**

        Page[artist]: Artists with pages
    """
    return paginate(service.db_session, service.list())


@router.get("/search", response_model=Page[Artist])
async def search(
    query: str,
    service: Annotated[ArtistService, Depends(get_service)],
) -> Page[Artist]:
    """

    **Route to retrieve artists containing query parameter

    **Args:**

        query (str): Artist searched
        service (Annotated[artistService, Depends): Artist service

    **Returns:**

        Page[artist]: Artists matching criteria with pages
    """
    return paginate(service.db_session, service.search(query))


@router.post("/add", response_model=Artist, status_code=status.HTTP_201_CREATED)
async def add(
    artist: Annotated[ArtistCreate, Body(embed=True)],
    poster_img: UploadFile,
    service: Annotated[ArtistService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Artist:
    """

    **Route to create a new artist**

    **Args:**

        service (Annotated[ArtistService, Depends): Artist service
        current_user (Annotated[User, Depends): Get user using the token in the header
        artist (Annotated[ArtistCreate, Body]): Artist create schema
        poster_img (UploadFile): Poster image

    **Returns:**

        artist: Created artist
    """
    return service.create(artist, poster_img, current_user)


@router.put("/update/{id}", response_model=Artist)
async def update(
    id: int,
    artist: Annotated[ArtistUpdate, Body(embed=True)],
    service: Annotated[ArtistService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    poster_img: UploadFile | None = None,
) -> Artist:
    """

    **Route to update an artist**

    **Args:**

        id (int): Artist id
        service (Annotated[ArtistService, Depends): Artist service
        current_user (Annotated[User, Depends): Get user using the token in the header
        artist (Annotated[ArtistUpdate, Body): Artist update schema.
        poster_img (UploadFile | None, optional): Optional poster image

    **Returns:**

        artist: Updated artist
    """
    return service.update(id, artist, poster_img, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: Annotated[ArtistService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """

    **Route to delete an artist**

    **Args:**

        id (int): Artist id
        service (Annotated[ArtistService, Depends): Artist service
        current_user (Annotated[User, Depends): Get user using the token in the header
    """
    return service.delete(id, current_user)


@router.get("/{id}", response_model=Artist)
async def get(
    id: int,
    service: Annotated[ArtistService, Depends(get_service)],
) -> Artist:
    """

    **Route to get artist by id**

    **Args:**

        id (int): Artist id
        service (Annotated[ArtistService, Depends): Artist service

    **Returns:**

        artist: Artist retrieved
    """
    return service.get(id)
