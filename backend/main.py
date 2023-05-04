from db import schemas
from db.session import get_session
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from db.models import User
from datetime import timedelta, datetime
from services.users import UserService, get_user_service
from sqlalchemy.orm import Session
from utils import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user
)


ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def register(user: schemas.UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create(user)


@app.post("/update")
async def update(user: schemas.UserUpdate, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    print(f"Data : {user}")
    print(f"Current user : {current_user.username}")


@app.post('/login', summary="Create access tokens for user", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_session)):
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
