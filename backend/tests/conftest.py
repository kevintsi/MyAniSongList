from datetime import datetime
import os
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import engine
from app.db.models import Base, User
from app.utils import get_password_hash
from app.db.schemas.users import UserLogin
from app.db.schemas.animes import AnimeCreate
from app.db.schemas.artists import ArtistCreate
from app.db.schemas.languages import LanguageCreate
from app.db.schemas.musics import MusicCreate
from app.db.schemas.types import TypeCreate


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as test_client:
        # testing
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db():
    # Create table in database following the models
    print("Create database for test...")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(
        User(
            username="test_manager",
            email="test_manager@gmail.com",
            password=get_password_hash("motdepasse"),
            is_manager=True,
        )
    )
    session.add(
        User(
            username="test",
            email="test@gmail.com",
            password=get_password_hash("motdepasse"),
            is_manager=False,
        )
    )
    session.commit()
    yield TestClient(app)
    print("Delete tables when done with")
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def get_token_not_manager(test_app_with_db):
    user = UserLogin(email="test@gmail.com", password="motdepasse")
    response = test_app_with_db.post("/users/login", json=user.dict())
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def get_token_manager(test_app_with_db):
    user = UserLogin(email="test_manager@gmail.com", password="motdepasse")
    response = test_app_with_db.post("/users/login", json=user.dict())
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def setUp(test_app_with_db, get_token_manager):
    """
    Create a music example for the test

    Args:
        test_app_with_db (TestClient): TestClient to test API
        get_token_manager (str): Token generated
    """
    lang = LanguageCreate(code="fr")
    type = TypeCreate(name="Opening")
    anime = AnimeCreate(name="Kimetsu no Yaiba", description="description fr")
    artist = ArtistCreate(name="LiSA", creation_year="2005")
    music = MusicCreate(
        name="Gurenge",
        release_date=datetime(2018, 10, 1),
        artists=[1],
        type_id=1,
        id_video="x45dsF",
        anime_id=1,
    )

    response_post_lang = test_app_with_db.post(
        "/languages/add",
        json=lang.dict(),
        headers={"Authorization": f"Bearer {get_token_manager}"},
    )

    assert response_post_lang.status_code == 201

    response_post_type = test_app_with_db.post(
        "/types/add",
        json=type.dict(),
        headers={"Authorization": f"Bearer {get_token_manager}"},
    )

    assert response_post_type.status_code == 201

    file_anime = open(
        "/usr/src/app/tests/images_test/demon_slayer.jpg", mode="rb"
    )

    response_post_anime = test_app_with_db.post(
        "/animes/add",
        data={"anime": anime.json()},
        headers={"Authorization": f"Bearer {get_token_manager}"},
        files={
            "poster_img": (
                os.path.basename(file_anime.name),
                file_anime,
                "image/jpeg",
            )
        },
    )

    response_post_anime.status_code == 201

    file_artist = open("/usr/src/app/tests/images_test/LiSA.jpg", mode="rb")
    response_post_artist = test_app_with_db.post(
        "/artists/add",
        data={"artist": artist.json()},
        headers={"Authorization": f"Bearer {get_token_manager}"},
        files={
            "poster_img": (
                os.path.basename(file_artist.name),
                file_artist,
                "image/jpeg",
            )
        },
    )

    assert response_post_artist.status_code == 201

    file_music = open("/usr/src/app/tests/images_test/Gurenge.jpg", mode="rb")
    response_post_music = test_app_with_db.post(
        "musics/add",
        data={"music": music.json()},
        headers={"Authorization": f"Bearer {get_token_manager}"},
        files={
            "poster_img": (
                os.path.basename(file_music.name),
                file_music,
                "image/jpeg",
            )
        },
    )

    assert response_post_music.status_code == 201
