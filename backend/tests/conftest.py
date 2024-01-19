from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.db.session import engine
from app.db.models import Base


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as test_client:
        # testing
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db():
    # Create table in database following the models
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        # testing
        yield test_client
