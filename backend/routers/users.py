from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    File,
    Body,
    UploadFile
)
from fastapi.security import OAuth2PasswordRequestForm
from db.schemas import *
from utils import (
    get_current_user,
    authenticate_user,
    create_access_token
)
from sqlalchemy.orm import Session
from datetime import timedelta
from services.users import (
    UserService,
    UserCreate,
    UserUpdate,
    get_service,
    get_session,
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


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
    current_user: User = Depends(get_current_user),
    user: UserUpdate = Body(...)
):
    print(f"Data : {user} , {profile_picture.filename}")
    print(f"Current user : {current_user.id} , {current_user.username}")
    return service.update(current_user.id, user, profile_picture)


@router.post('/login', summary="Create access tokens for user", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_session)
):
    print(form_data)
    user: User | None = authenticate_user(
        db_session,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=User)
async def profile(
    service: UserService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    return service.get(current_user.id)


@router.delete("/delete")
async def delete(
        service: UserService = Depends(get_service),
        current_user: User = Depends(get_current_user)
):
    return service.delete(current_user.id)
