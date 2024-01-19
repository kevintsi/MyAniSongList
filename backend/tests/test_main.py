from app.db.schemas.users import UserCreate


def test_read_main(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Works fine"}


def test_create_user(test_app_with_db):
    user = UserCreate(
        email="test@gmail.com",
        username="test",
        password="motdepasse"
    )
    response = test_app_with_db.post("/users/register", json=user.dict())
    assert response.status_code == 201
    assert response.json()["username"] == user.username
    assert response.json()["email"] == user.email
    assert response.json()["profile_picture"] == None
