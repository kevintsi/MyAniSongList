from typing import Annotated

from app.db.models import User
from app.db.schemas.animes import (
    Anime,
    AnimeCreate,
    AnimeTranslationCreate,
    AnimeUpdate,
)
from app.services.animes import AnimeService, get_service
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from .users import get_current_user

router = APIRouter(prefix="/animes", tags=["Animes"])


@router.get("/all", response_model=Page[Anime])
async def get_all(
    lang: str,
    service: Annotated[AnimeService, Depends(get_service)],
) -> Page[Anime]:
    """
    **Route to retrieve all animes**

    **Args:**

        lang (str): Language code
        service (Annotated[AnimeService, Depends]) : Anime service

    **Returns:**

        Page[Anime]: Animes with pages
    """
    res = service.list(lang)
    return paginate(
        service.db_session,
        res,
        transformer=lambda items: [
            Anime(
                id=row.id_anime,
                description=row.description,
                poster_img=row.anime.poster_img,
                name=row.name,
            ).dict()
            for row in items
        ],
    )


@router.get("/search", response_model=Page[Anime])
async def search(
    lang: str,
    query: str,
    service: Annotated[AnimeService, Depends(get_service)],
) -> Page[Anime]:
    """
    **Route to retrieves all animes containing the query parameter**

    **Args:**

        lang (str): Language code
        query (str): Anime searched
        service (Annoted[AnimeService, optional]): Anime service

    **Returns:**

        Page[Anime]: Animes with page
    """
    res = service.search(query, lang)
    return paginate(
        service.db_session,
        res,
        transformer=lambda items: [
            Anime(
                id=row.id_anime,
                description=row.description,
                poster_img=row.anime.poster_img,
                name=row.name,
            ).dict()
            for row in items
        ],
    )


@router.post("/add", response_model=Anime, status_code=status.HTTP_201_CREATED)
async def add(
    anime: Annotated[AnimeCreate, Body(embed=True)],
    poster_img: Annotated[UploadFile, File()],
    service: Annotated[AnimeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Anime:
    """
    **Route to create an Anime**

    **Args:**

        poster_img (Annotated[UploadFile, File): Poster image
        service (Annotated[AnimeService, Depends): Anime service
        current_user (Annotated[User, Depends): Get user using the token in the header
        anime (Annotated[AnimeCreate, Body, optional]): Anime schema.

    **Returns:**

        Anime: Created anime
    """
    if current_user.is_manager:
        return service.create(anime, poster_img)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )


@router.post(
    "/{id}/add_translation/",
    response_model=Anime,
    status_code=status.HTTP_201_CREATED,
)
async def add_translation(
    id: int,
    lang: str,
    anime: AnimeTranslationCreate,
    service: Annotated[AnimeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Anime:
    """
    **Route to add translation for an anime**

    **Args:**
        id (int): Anime id
        lang (str): Language code
        anime (AnimeTranslationCreate): Anime translation
        service (Annotated[AnimeService, Depends): Anime service
        current_user (Annotated[User, Depends): Get user using the token in the header

    **Returns:**

        Anime: Created anime translation

    """
    if current_user.is_manager:
        return service.create_translation(anime, id, lang)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )



@router.put("/update/{id}", response_model=Anime)
async def update(
    lang: str,
    id: int,
    anime: Annotated[AnimeUpdate, Body(embed=True)],
    service: Annotated[AnimeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    poster_img: UploadFile | None = None,
) -> Anime:
    """

    **Route to update an anime**

    **Args:**

        lang (str): Language code
        id (int): Anime id
        service (Annotated[AnimeService, Depends): Anime service
        current_user (Annotated[User, Depends): Get user using the token in the header
        anime (Annotated[AnimeUpdate, Body]): Anime update schema
        poster_img (UploadFile | None, optional): Optional poster image. Defaults to None

    **Returns:**

        Anime: Anime updated
    """
    if current_user.is_manager:
        return service.update(id, anime, poster_img, lang)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: Annotated[AnimeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    **Route to delete an anime**

    **Args**:

        id (int): Anime id
        service (Annotated[AnimeService, Depends]): Anime service
        current_user (Annotated[User, Depends]): Get user using the token in the header
    """
    if current_user.is_manager:
        return service.delete(id)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.get("/{id}", response_model=Anime)
async def get(
    lang: str,
    id: int,
    service: Annotated[AnimeService, Depends(get_service)],
) -> Anime:
    """
    **Route to get an anime by id**

    **Args:**

        lang (str): Language code
        id (int): Anime id
        service (Annotated[AnimeService, Depends]): Anime service

    **Returns:**

        Anime : Anime retrieved

    """
    return service.get(id, lang)
