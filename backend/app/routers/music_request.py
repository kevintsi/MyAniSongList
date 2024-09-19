from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.music_request import MusicRequestService, get_service
from .users import get_current_user
from app.services.users import User
from app.db.schemas.music_requests import (
    MusicRequest,
    CreateMusicRequest
)

router = APIRouter(prefix="/request_music", tags=["Request Musics"])

@router.get("/all")
async def get_all(
    service : Annotated[MusicRequestService, Depends(get_service)], 
    current_user : Annotated[User, Depends(get_current_user)]
    ):
    if current_user.is_manager:
        return service.get_all()
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
@router.post("/", response_model=MusicRequest)
async def request_music(
    music_request : CreateMusicRequest,
    service: Annotated[MusicRequestService, Depends(get_service)],
    current_user : Annotated[User, Depends(get_current_user)]
):
    """

    **Route for requesting a new music**

    **Args:**

        music_request (CreateMusicRequest): Schema for requesting new music
        service (Annotated[MusicService, Depends]): Music id
        current_user (Annotated[User, Depends]): Get user using the token in the header

    **Returns:**

        MusicRequest: request music
    """
    return service.create_request(music_request, current_user)

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_music_request(
    id: int,
    service: Annotated[MusicRequestService, Depends(get_service)],
    current_user : Annotated[User, Depends(get_current_user)]
):
    """

    **Route for updating a music request**

    **Args:**

        id (str): Id request music
        service (Annotated[MusicRequestService, Depends]): Music request service
        current_user (Annotated[User, Depends]): Get user using the token in the header

    **Returns:**

        MusicRequest: request music
    """
    if current_user.is_manager:
        return service.update_request(id)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized, not manager")
    

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_music_request(
    id: int,
    service: Annotated[MusicRequestService, Depends(get_service)],
    current_user : Annotated[User, Depends(get_current_user)]
):
    """

    **Route for delete a given music request**

    **Args:**

        id (str): Id request music
        service (Annotated[MusicRequestService, Depends]): Music request service
        current_user (Annotated[User, Depends]): Get user using the token in the header
    """
    if current_user.is_manager:
        service.delete(id)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized, not manager")