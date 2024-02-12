from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    status
)
from .users import get_current_user
from app.db.models import User
from app.db.schemas.types import Type, TypeCreate, TypeUpdate
from app.services.types import (
    TypeService,
    get_service,
)

router = APIRouter(
    prefix='/types',
    tags=["Types"]
)


@router.get("/all", response_model=list[Type])
async def get_all(
    lang: str,
    service: Annotated[TypeService, Depends(get_service)],
) -> list[Type]:
    """

    **Route to retrieves all types of music**

    **Args:**

        lang (str): Language code
        service (Annotated[TypeService, Depends]): Type service

    **Returns:**

        list[Type]: List of all types by language code
    """
    return service.list(lang)


@router.post("/add", response_model=Type, status_code=status.HTTP_201_CREATED)
async def add(
    type: TypeCreate,
    service: Annotated[TypeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> Type:
    """

    **Route to create a new type of music**

    **Args:**

        type (TypeCreate): Type create schema
        service (Annotated[TypeService, Depends]): Type service 
        current_user (Annotated[User, Depends]): Get user using the token in the header

    **Returns:**

        Type: Created type
    """
    return service.create(type, current_user)


@router.post("/{id}/add_translation", response_model=Type, status_code=status.HTTP_201_CREATED)
async def add_translation(
    id: str,
    type: TypeCreate,
    lang: str,
    service: Annotated[TypeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> Type:
    """

    **Route to add a new translation for a type of music**

    **Args:**

        id (str): Type id
        type (TypeCreate): Type create schema
        lang (str): Language code
        service (Annotated[TypeService, Depends]): Type service
        current_user (Annotated[User, Depends]): Get user using the token in the header

    **Returns:**

        Type: Created type translation 
    """
    return service.add_translation(type, lang, id, current_user)


@router.put("/update/{id}", response_model=Type)
async def update(
    id: int,
    type: TypeUpdate,
    service: Annotated[TypeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> Type:
    """

    **Route to update a music type**

    **Args:**

        id (int): Type id
        type (TypeUpdate): Type update schema
        service (Annotated[TypeService, Depends]): Type service
        current_user (Annotated[User, Depends]): Get user using the token in the header

    **Returns:**

        Type: Updated type
    """
    return service.update(id, type, current_user)


@router.put("/{id}/update_translation", response_model=Type)
async def update_translation(
    lang: str,
    id: int,
    type: TypeUpdate,
    service: Annotated[TypeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> Type:
    """

    **Route to update music type translation**

    **Args:**

        lang (str): Language code
        id (int): Type id
        type (TypeUpdate): Type update schema
        service (Annotated[TypeService, Depends]): Type service
        current_user (Annotated[User, Depends]): Get user using the token in the header

    **Returns:**

        Type: Update type translation
    """
    return service.update_translation(type, lang, id, current_user)


@router.delete("/delete/{id}")
async def delete(
    id: int,
    service: Annotated[TypeService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """

    **Route to delete a type of music**

    **Args:**

        id (int): Type id
        service (Annotated[TypeService, Depends]): Type service
        current_user (Annotated[User, Depends]): Get user using the token in the header
    """
    return service.delete(id, current_user)


@router.get("/{id}", response_model=Type)
async def get(
    lang: str,
    id: int,
    service: Annotated[TypeService, Depends(get_service)],
) -> Type:
    """
    **Route to get type translation by id and language code**

    **Args:**

        lang (str) : Language code
        id (int): Type id
        service (Annotated[TypeService, Depends]): Get user using the token in the header

    **Returns:**

        Type: Retrieved type translation
    """
    return service.get_translation(id, lang)
