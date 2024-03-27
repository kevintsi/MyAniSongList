from datetime import datetime, timedelta, timezone
from os import getenv
import os
from typing import Annotated
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
    Body,
    UploadFile
)
from fastapi_pagination import Page
import jwt
import redis
from app.db.schemas.users import User, UserLogin
from app.utils import (
    authenticate_user,
    create_access_token,
)
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from app.services.users import (
    UserService,
    UserCreate,
    UserUpdate,
    get_service,
    get_session,
)
from fastapi.security import HTTPBearer

from app.db.schemas.token import Token

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


async def get_current_user(
        token: Annotated[str, Depends(HTTPBearer())],
        user_service: Annotated[UserService, Depends(get_service)]
) -> User:
    """

    **Function to get current user logged in with the token given in the header**

    **Args:**

        token (Annotated[str, Depends]): token retrieved from the header
        user_service (Annotated[UserService, Depends]): User service

    **Raises:**

        credentials_exception: Raised when token has expired

    **Returns:**

        User: User retrieved with token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, getenv("SECRET_KEY"),
                             algorithms=getenv("ALGORITHM"))
        user = payload.get("sub")
        print(f"Value in access token : {user} {type(user)}")
        if user is None:
            raise credentials_exception

        return user_service.get(user["id"])
    except jwt.InvalidTokenError:
        raise credentials_exception


@router.get("/search", response_model=Page[User])
async def search(
    query: str,
    service: Annotated[UserService, Depends(get_service)]
) -> Page[User]:
    """

    **Route to search for an user matching query parameter**

    **Args:**

        query (str): User searched 
        service (Annotated[UserService, Depends]): User service

    **Returns:**

        Page[User]: List of users matching the query parameter using pages format 
    """
    return paginate(service.db_session, service.search(query))


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_service)]
) -> User:
    """

    **Route to create a new user**

    **Args:**

        user (UserCreate): User create schema
        service (Annotated[UserService, Depends]): User service

    **Returns:**

        User: Created user
    """
    return service.create(user)


@router.put("/update", response_model=User, status_code=status.HTTP_200_OK)
async def update(
    service: Annotated[UserService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    user: Annotated[UserUpdate, Body(embed=True)] = None,
    profile_picture: UploadFile | None = None,
) -> User:
    """

    **Route to update a given user**

    **Args:**

        service (Annotated[UserService, Depends): User service
        current_user (Annotated[User, Depends): Get user using the token in the header
        user (Annotated[UserUpdate, Body]): Optional User update schema
        profile_picture (UploadFile): Optional Profile picture

    **Returns:**

        User: Updated user
    """
    print(f"Current user : {current_user}")
    return service.update(current_user.id, user, profile_picture)


@router.post('/login', summary="Create access tokens for user", response_model=Token)
async def login(
    response: Response,
    form_data: UserLogin,
    db_session: Annotated[Session, Depends(get_session)],
) -> Token:
    """

    **Route to log in an user**

    **Args:**

        response (Response): Response to add refresh token to cookie
        form_data (UserLogin): User login schema
        db_session (Annotated[Session, Depends): Session 

    **Raises:**

        HTTPException: Raised when credentials incorrect

    **Returns:**

        Token: Created access token
    """
    user = authenticate_user(
        db_session, form_data.email, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")
    print(user)
    access_token_expires = timedelta(minutes=15)
    print(access_token_expires)
    access_token = create_access_token(
        data={"sub": {"id": user.id, "is_manager": user.is_manager}}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(days=7)
    refresh_token = create_access_token(
        data={"sub": {"id": user.id, "is_manager": user.is_manager}}, expires_delta=refresh_token_expires)

    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        samesite="none",
                        secure=True,
                        httponly=True,
                        domain=os.getenv("DOMAIN"),
                        expires=datetime.now(
                            timezone.utc)+refresh_token_expires
                        )

    return Token(access_token=access_token)


@router.post("/refresh_token", response_model=Token)
def refresh_access_token(
        response: Response,
        refresh_token: str = Cookie(None)
) -> Token:
    """
    **Route to refresh access token**

    **Args:**

        response (Response): Response to add new cookie with new refresh token
        refresh_token (str, optional): Refresh token Defaults to Cookie(None).

    **Raises:**

        HTTPException: Raised when given refresh token is blacklisted
        HTTPException: Raised when given refresh token is missing

    **Returns:**

        Token: New access token
    """
    try:
        r = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD")
        )
        if refresh_token:
            if r.sismember('token_blacklist', refresh_token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid refresh token has already been revoked",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                # Verify and decode the refresh token
                decoded_token = jwt.decode(refresh_token, getenv(
                    "SECRET_KEY"), algorithms=getenv("ALGORITHM"))
                user = decoded_token.get("sub")
                print(user)
                # Generate a new access token
                access_token_expires = timedelta(minutes=15)
                new_access_token = create_access_token(
                    data={"sub": {"id": user['id'], "is_manager": user['is_manager']}}, expires_delta=access_token_expires
                )

                refresh_token_expires = timedelta(days=7)
                new_refresh_token = create_access_token(
                    data={"sub": {"id": user['id'], "is_manager": user['is_manager']}}, expires_delta=refresh_token_expires)

                response.set_cookie("refresh_token",
                                    value=new_refresh_token,
                                    samesite="none",
                                    secure=True,
                                    httponly=True,
                                    domain=os.getenv("DOMAIN"),
                                    expires=datetime.now(
                                        timezone.utc)+refresh_token_expires
                                    )

                r.sadd("token_blacklist", refresh_token)
                # Return the new access token
                return Token(access_token=new_access_token)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as e:
        raise e


@router.post('/logout')
def logout(response: Response, refresh_token: str = Cookie(default=None)):
    """

    **Route to logout**

    **Args:**

        response (Response): Response to delete cookie
        refresh_token (str, optional): Refresh token in cookie Defaults to Cookie(default=None).

    Returns:
        JSON: Success message
    """
    r = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        password=os.getenv("REDIS_PASSWORD")
    )

    r.sadd("token_blacklist", refresh_token)

    response.delete_cookie("refresh_token")

    return {"msg": "Successfully logout"}


@router.get("/me", response_model=User)
async def profile(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UserService, Depends(get_service)]

) -> User:
    """

    **Route to get current user logged in profile**

    **Args:**

        current_user (Annotated[User, Depends]): Get user using the token in the header
        service (Annotated[UserService, Depends]): User service

    **Returns:**

        User: User profile
    """
    print(f"User : {current_user.id} {type(current_user)}")
    return service.get(current_user.id)


@router.get("/{id}", response_model=User)
async def get_user(
    id: int,
    service: Annotated[UserService, Depends(get_service)]

) -> User:
    """

    **Route to get an user**

    **Args:**

        id (int): User id
        service (Annotated[UserService, Depends]): User service

    **Returns:**

        User: Retrieved user
    """
    return service.get(id)


@router.delete("/delete")
async def delete(
    service: Annotated[UserService, Depends(get_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """

    **Route to delete current logged in user**

    **Args:**

        service (Annotated[UserService, Depends]): User service
        current_user (Annotated[User, Depends]):  Get user using the token in the header
    """
    service.delete(current_user.id)
