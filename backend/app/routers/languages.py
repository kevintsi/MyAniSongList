from typing import Annotated

from app.db.models import User
from app.db.schemas.languages import Language, LanguageCreate, LanguageUpdate
from app.services.languages import LanguageService, get_service
from fastapi import APIRouter, Depends, status

from .users import get_current_user

router = APIRouter(prefix="/languages", tags=["Languages"])


@router.get("/all", response_model=list[Language])
async def get_all(
    service: Annotated[LanguageService, Depends(get_service)]
) -> list[Language]:
    """
    **Route to get all supported languages**

    **Args:**

        service (Annotated[LanguageService, Depends]): Language service

    **Returns:**

        list[Language]: All supported languages
    """
    return service.list().all()


@router.get("/{id}", response_model=Language)
async def get(
    id: int, service: Annotated[LanguageService, Depends(get_service)]
) -> Language:
    """

    **Route to get language by id**

    **Args:**

        id (int): Language id
        service (Annotated[LanguageService, Depends]): Language service

    **Returns:**

        Language: Language retrieved
    """
    return service.get(id)


@router.get("/animes/{id}", response_model=list[Language])
async def get_languages_by_anime(
    id: int, service: Annotated[LanguageService, Depends(get_service)]
) -> list[Language]:
    """

    **Route to get supported languages by an anime**

    **Args:**

        id (int): Anime id
        service (Annotated[LanguageService, Depends]): Language service

    **Returns:**

        list[Language]: List of supported languages
    """
    return service.get_languages_by_anime(id)


@router.get("/types/{id}", response_model=list[Language])
async def get_languages_by_type(
    id: int, service: Annotated[LanguageService, Depends(get_service)]
) -> list[Language]:
    """

    **Route to get supported languages by type**

    **Args:**

        id (int): Type id
        service (Annotated[LanguageService, Depends]): Language service

    **Returns:**

        list[Language]: List of supported languages
    """
    return service.get_languages_by_type(id)


@router.post(
    "/add", response_model=Language, status_code=status.HTTP_201_CREATED
)
async def add(
    language: LanguageCreate,
    service: Annotated[LanguageService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Language:
    """

    **Route to create a new supported language**

    **Args:**

        language (LanguageCreate): Language create schema
        service (Annotated[LanguageService, Depends): Language service
        current_user (Annotated[User, Depends): Get user using the token in the header

    **Returns:**

        Language: Created language
    """
    return service.create(language, current_user)


@router.put("/update/{id}", response_model=Language)
async def update(
    id: int,
    language: LanguageUpdate,
    service: Annotated[LanguageService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Language:
    """

    **Route to update a supported language**

    **Args:**

        id (int): Language id
        language (LanguageUpdate): Language update schema
        service (Annotated[LanguageService, Depends): Language service
        current_user (Annotated[User,Depends): Get user using the token in the header

    **Returns:**

        Language: Language updated
    """
    return service.update(id, language, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: Annotated[LanguageService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """

    **Route to delete a supported language**

    **Args:**

        id (int): Language id
        service (Annotated[LanguageService, Depends): Language service
        current_user (Annotated[User, Depends): Get user using the token in the header

    """
    return service.delete(id, current_user)
