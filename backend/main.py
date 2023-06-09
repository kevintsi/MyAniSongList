import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    users,
    animes,
    musics,
    authors,
    types,
    reviews
)

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from db.schemas import Settings
import os


@AuthJWT.load_config
def get_config():
    return Settings()


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


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(users.router)
app.include_router(animes.router)
app.include_router(musics.router)
app.include_router(authors.router)
app.include_router(types.router)
app.include_router(reviews.router)
