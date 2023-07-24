from datetime import datetime, timedelta, timezone
from os import getenv
import os
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
    File,
    Body,
    UploadFile
)
from fastapi_pagination import Page
import jwt
import redis
from db.schemas.users import *
from utils import (
    authenticate_user,
    create_access_token,
)
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from services.users import (
    UserService,
    UserCreate,
    UserUpdate,
    get_service,
    get_session,
)
from fastapi.security import HTTPBearer

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


async def get_current_user(token: str = Depends(HTTPBearer()), user_service: UserService = Depends(get_service)):
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


@router.get("/search", response_model=Page[UserPublic])
async def search(
    query: str,
    service: UserService = Depends(get_service)
):
    return paginate(service.search(query))


@router.post("/register")
async def register(
    user: UserCreate,
    service: UserService = Depends(get_service)
):
    return service.create(user)


@router.put("/update")
async def update(
    profile_picture: UploadFile = File(...),
    service: UserService = Depends(get_service),
    user: UserUpdate = Body(...),
    current_user: User = Depends(get_current_user)
):
    print(f"Current user : {current_user}")
    return service.update(current_user.id, user, profile_picture)


@router.post('/login', summary="Create access tokens for user")
async def login(
    response: Response,
    form_data: UserLogin,
    db_session: Session = Depends(get_session),
):
    user = authenticate_user(
        db_session, form_data.email, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")
    print(user)
    access_token_expires = timedelta(minutes=15)
    print(access_token_expires)
    access_token = create_access_token(
        data={"sub": {"id": user.id, "username": user.username, "is_manager": user.is_manager, 'profile_picture': user.profile_picture}}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(days=7)
    refresh_token = create_access_token(
        data={"sub": {"id": user.id, "username": user.username, "is_manager": user.is_manager, 'profile_picture': user.profile_picture}}, expires_delta=refresh_token_expires)

    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        samesite="none",
                        secure=True,
                        httponly=True,
                        domain=os.getenv("DOMAIN"),
                        expires=datetime.now(
                            timezone.utc)+refresh_token_expires
                        )

    # Générez également un refresh token et stockez-le dans votre système de stockage
    # Vous pouvez utiliser votre propre logique de génération et de stockage du refresh token ici
    return {"access_token": access_token}


@router.post("/refresh_token")
def refresh_access_token(response: Response, refresh_token: str = Cookie(None)):
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
                    data={"sub": {"id": user['id'], "username": user["username"], "is_manager": user['is_manager'], 'profile_picture': user['profile_picture']}}, expires_delta=access_token_expires
                )

                refresh_token_expires = timedelta(days=7)
                new_refresh_token = create_access_token(
                    data={"sub": {"id": user['id'], "username": user["username"], "is_manager": user['is_manager'], 'profile_picture': user['profile_picture']}}, expires_delta=refresh_token_expires)

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
                return {"access_token": new_access_token}
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
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_service)

):
    print(f"User : {current_user.id} {type(current_user)}")
    return service.get(current_user.id)


@router.get("/{id}", response_model=UserPublic)
async def get_user(
    id: int,
    service: UserService = Depends(get_service)

):
    return service.get(id)


@router.delete("/delete")
async def delete(
    service: UserService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete(current_user.id)
