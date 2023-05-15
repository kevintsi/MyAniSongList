from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    File,
    Body,
    UploadFile
)
from db.schemas import *
from utils import (
    authenticate_user,
)
from sqlalchemy.orm import Session
from services.users import (
    UserService,
    UserCreate,
    UserUpdate,
    get_service,
    get_session,
)

from fastapi_jwt_auth import AuthJWT

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
    authorize: AuthJWT = Depends(),
    user: UserUpdate = Body(...)
):

    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()

    print(f"Data : {user} , {profile_picture.filename}")
    print(f"Current user : {current_user}")
    return service.update(current_user, user, profile_picture)


@router.post('/login', summary="Create access tokens for user")
async def login(
    form_data: UserLogin,
    authorize: AuthJWT = Depends(),
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
    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = authorize.create_access_token(subject=user.id)
    refresh_token = authorize.create_refresh_token(subject=user.id)

    # Set the JWT cookies in the response
    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)

    return user


@router.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    # Set the JWT cookies in the response
    authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@router.post('/logout')
def logout(authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    authorize.jwt_required()

    authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@router.get("/", response_model=User)
async def profile(
    authorize: AuthJWT = Depends(),
    service: UserService = Depends(get_service),
):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    return service.get(current_user)


@router.delete("/delete")
async def delete(
    service: UserService = Depends(get_service),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()

    return service.delete(current_user)
