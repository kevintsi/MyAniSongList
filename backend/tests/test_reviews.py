from datetime import datetime
import os
from app.db.schemas.languages import LanguageCreate
from app.db.schemas.types import TypeCreate
from app.db.schemas.animes import AnimeCreate
from app.db.schemas.authors import AuthorCreate
from app.db.schemas.musics import MusicCreate
from app.db.schemas.reviews import ReviewCreate, ReviewUpdate


class TestReviews():
    ENDPOINT_BASE = "/reviews"

    def setUp(self, test_app_with_db, get_token_manager):
        """
        Create a music example for the test

        Args:
            test_app_with_db (TestClient): TestClient to test API
            get_token_manager (str): Token generated 
        """
        lang = LanguageCreate(code="fr")
        type = TypeCreate(name="Opening")
        anime = AnimeCreate(name="Kimetsu no Yaiba",
                            description="description fr")
        author = AuthorCreate(name="LiSA", creation_year="2005")
        music = MusicCreate(name="Gurenge", release_date=datetime(
            2018, 10, 1), authors=[1], type_id=1, id_video="x45dsF", anime_id=1)

        response_post_lang = test_app_with_db.post("/languages/add", json=lang.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        assert response_post_lang.status_code == 201

        response_post_type = test_app_with_db.post("/types/add", json=type.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        assert response_post_type.status_code == 201

        response_post_type_translation = test_app_with_db.post("/types/1/add_translation?lang=fr", json=type.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        assert response_post_type_translation.status_code == 201

        file_anime = open(
            "/usr/src/app/tests/images_test/demon_slayer.jpg", mode="rb")

        response_post_anime = test_app_with_db.post("/animes/add", data={"anime": anime.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        }, files={"poster_img": (os.path.basename(file_anime.name), file_anime, "image/jpeg")})

        response_post_anime.status_code == 201

        file_author = open(
            "/usr/src/app/tests/images_test/LiSA.jpg", mode="rb")
        response_post_author = test_app_with_db.post("/authors/add", data={"author": author.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        }, files={"poster_img": (os.path.basename(file_author.name), file_author, "image/jpeg")})

        assert response_post_author.status_code == 201

        file_music = open(
            "/usr/src/app/tests/images_test/Gurenge.jpg", mode="rb")
        response_post_music = test_app_with_db.post(f"musics/add", data={"music": music.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        }, files={"poster_img": (os.path.basename(file_music.name), file_music, "image/jpeg")})

        assert response_post_music.status_code == 201

    def test_add_review(self, test_app_with_db, get_token_manager, get_token_not_manager):
        self.setUp(test_app_with_db, get_token_manager)
        review = ReviewCreate(note_music=5,
                              note_visual=4,
                              description="Bonne musique",
                              music_id=1)
        response_post = test_app_with_db.post(f"{self.ENDPOINT_BASE}/add", json=review.dict(), headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })

        assert response_post.status_code == 201
        assert response_post.json()["note_music"] == review.note_music
        assert response_post.json()["note_visual"] == review.note_visual
        assert response_post.json()["description"] == review.description
        assert response_post.json()["music"]["id"] == review.music_id

    def test_update_review(self, test_app_with_db, get_token_not_manager):
        review = ReviewUpdate(note_music=5,
                              note_visual=5,
                              description="Bonne musique updated",
                              music_id=1)
        response_post = test_app_with_db.put(f"{self.ENDPOINT_BASE}/update/1", json=review.dict(), headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })

        assert response_post.status_code == 200
        assert response_post.json()["note_music"] == review.note_music
        assert response_post.json()["note_visual"] == review.note_visual
        assert response_post.json()["description"] == review.description
        assert response_post.json()["music"]["id"] == review.music_id

    def test_get_review(self, test_app_with_db):
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/1")

        assert response_get.status_code == 200
        assert response_get.json()["id"] == 1
        assert response_get.json()["user"]["username"] == "test"
        assert response_get.json()["note_music"] == 5
        assert response_get.json()["note_visual"] == 5
        assert response_get.json()["description"] == "Bonne musique updated"

    def test_get_user_review(self, test_app_with_db, get_token_not_manager):
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/user/music/1", headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })

        response_get.status_code == 200
        assert response_get.json()["id"] == 1
        assert response_get.json()["user"]["username"] == "test"
        assert response_get.json()["note_music"] == 5
        assert response_get.json()["note_visual"] == 5
        assert response_get.json()["description"] == "Bonne musique updated"

    def test_get_music_reviews(self, test_app_with_db):
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/music/1")

        assert response_get.status_code == 200
        assert response_get.json()["total"] == 1
        assert type(response_get.json()["items"]) is list

    def test_delete_review(self, test_app_with_db, get_token_not_manager):
        response_delete = test_app_with_db.delete(f"{self.ENDPOINT_BASE}/delete/1", headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })

        assert response_delete.status_code == 200

        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/1")
        assert response_get.status_code == 404
