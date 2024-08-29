import pytest
from app.db.schemas.reviews import ReviewCreate, ReviewUpdate


@pytest.mark.usefixtures("setUp")
class TestReviews:
    ENDPOINT_BASE = "/reviews"

    def test_add_review(self, test_app_with_db, get_token_not_manager):
        review = ReviewCreate(
            note_music=5,
            note_visual=4,
            description="Bonne musique",
            music_id=1,
        )
        response_post = test_app_with_db.post(
            f"{self.ENDPOINT_BASE}/add",
            json=review.dict(),
            headers={"Authorization": f"Bearer {get_token_not_manager}"},
        )

        assert response_post.status_code == 201
        assert response_post.json()["note_music"] == review.note_music
        assert response_post.json()["note_visual"] == review.note_visual
        assert response_post.json()["description"] == review.description
        assert response_post.json()["music"]["id"] == review.music_id

    def test_update_review(self, test_app_with_db, get_token_not_manager):
        review = ReviewUpdate(
            note_music=5,
            note_visual=5,
            description="Bonne musique updated",
            music_id=1,
        )
        response_post = test_app_with_db.put(
            f"{self.ENDPOINT_BASE}/update/1",
            json=review.dict(),
            headers={"Authorization": f"Bearer {get_token_not_manager}"},
        )

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
        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/user/music/1",
            headers={"Authorization": f"Bearer {get_token_not_manager}"},
        )

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
        response_delete = test_app_with_db.delete(
            f"{self.ENDPOINT_BASE}/delete/1",
            headers={"Authorization": f"Bearer {get_token_not_manager}"},
        )

        assert response_delete.status_code == 200

        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/1")
        assert response_get.status_code == 404
