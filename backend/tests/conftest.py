import os
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session, sessionmaker
from app.main import app
from app.db.session import engine
from app.db.models import Base, User
from app.utils import get_password_hash
from app.db.schemas.users import UserLogin


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
    session.add(User(username="test_manager", email="test_manager@gmail.com",
                password=get_password_hash("motdepasse"), is_manager=True))
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
