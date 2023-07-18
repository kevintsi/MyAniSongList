
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from routers import (
    users,
    animes,
    musics,
    authors,
    types,
    reviews,
    favorites
)

app = FastAPI()

origins = os.getenv("ORIGINS").split(";")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Set-Cookie"],
)

app.include_router(users.router)
app.include_router(animes.router)
app.include_router(musics.router)
app.include_router(authors.router)
app.include_router(types.router)
app.include_router(reviews.router)
app.include_router(favorites.router)

add_pagination(app)
