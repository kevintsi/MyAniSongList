
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

app.include_router(users.router)
app.include_router(animes.router)
app.include_router(musics.router)
app.include_router(authors.router)
app.include_router(types.router)
app.include_router(reviews.router)
