import os
from app.db.schemas.users import User, UserCreate, UserLogin, UserUpdate
from app.firebase import bucket
from app.db.schemas.users import UserLogin


class TestUsers():
    ENDPOINT_BASE = "/users"

    def test_create_user(self, test_app_with_db):
        user = UserCreate(
            email="test2@gmail.com",
            username="test2",
            password="motdepasse"
        )
        response = test_app_with_db.post(
            f"{self.ENDPOINT_BASE}/register", json=user.dict())
        assert response.status_code == 201
        assert response.json()["username"] == user.username
        assert response.json()["email"] == user.email
        assert response.json()["profile_picture"] == None

    def test_update_profile(self, test_app_with_db):

        user = UserLogin(email="test2@gmail.com", password="motdepasse")
        token = test_app_with_db.post(
            f"{self.ENDPOINT_BASE}/login", json=user.dict()).json()["access_token"]

        user_update = UserUpdate(email="test2Update@gmail.com",
                                 username="test2Update", password="motdepasseUpdate")
        response_update = None
        with open("/usr/src/app/tests/images_test/naruto.jpg", "rb") as f:
            response_update = test_app_with_db.put(f"{self.ENDPOINT_BASE}/update", data={"user": user_update.json()}, headers={
                "Authorization": f"Bearer {token}",
            }, files={"profile_picture": (f"{os.path.basename(f.name)}", f, "image/jpeg")})

        blob = bucket.blob(
            "profile_pictures/naruto.jpg")
        blob.make_public()

        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/me", headers={
            "Authorization": f"Bearer {token}"})

        assert response_get.status_code == 200
        assert response_update.status_code == 200
        assert response_update.json() == User(id=response_get.json()["id"],
                                              email=response_get.json()[
            "email"],
            username=response_get.json()[
            "username"],
            profile_picture=blob.public_url)

    def test_search_user(self, test_app_with_db):
        new_users = [
            UserCreate(email="john.doe@gmail.com",
                       username="johndoe", password="motdepasse"),
            UserCreate(email="marie.doe@gmail.com",
                       username="mariedoe", password="motdepasse"),
            UserCreate(email="arthur.johns@gmail.com",
                       username="arthurjohns", password="motdepasse")
        ]

        for user in new_users:
            test_app_with_db.post(
                f"{self.ENDPOINT_BASE}/register", json=user.dict())

        response = test_app_with_db.get("/users/search?query=doe")
        assert response.status_code == 200
        assert response.json()["total"] == 2

    def test_get_user(self, test_app_with_db):
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/3")
        blob = bucket.blob(
            "profile_pictures/naruto.jpg")
        blob.make_public()
        assert response.status_code == 200
        assert response.json() == User(
            id=3,
            email="test2Update@gmail.com",
            username="test2Update",
            profile_picture=blob.public_url
        )

    def test_get_my_profile(self, test_app_with_db):
        user = UserLogin(email="marie.doe@gmail.com", password="motdepasse")
        response_login = test_app_with_db.post(
            f"{self.ENDPOINT_BASE}/login", json=user.dict())
        assert response_login.status_code == 200
        response_me = test_app_with_db.get(f"{self.ENDPOINT_BASE}/me", headers={
            "Authorization": f"Bearer {response_login.json()['access_token']}"
        })
        assert response_me.status_code == 200
        assert response_me.json()["email"] == user.email

    def test_delete_user(self, test_app_with_db):
        user = UserLogin(email="arthur.johns@gmail.com", password="motdepasse")
        response_login = test_app_with_db.post(
            f"{self.ENDPOINT_BASE}/login", json=user.dict())
        assert response_login.status_code == 200

        response = test_app_with_db.delete("/users/delete", headers={
            "Authorization": f"Bearer {response_login.json()['access_token']}"
        })

        assert response.status_code == 200

        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/6")
        assert response_get.status_code == 404
