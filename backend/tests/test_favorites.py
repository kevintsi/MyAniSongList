import pytest


@pytest.mark.usefixtures("setUp")
class TestFavorites():
    ENDPOINT_BASE = "/favorites"

    def test_add_favorite(self, test_app_with_db, get_token_not_manager):
        id_music = 1
        response_post = test_app_with_db.post(f"{self.ENDPOINT_BASE}/{id_music}", headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })
        assert response_post.status_code == 201

        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all", headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })
        assert response_get.status_code == 200
        assert response_get.json()[0]["id"] == id_music

    def test_user_favorites(self, test_app_with_db, get_token_not_manager):
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all", headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })

        assert response_get.status_code == 200
        assert type(response_get.json()) is list

    def test_other_user_favorites(self, test_app_with_db):
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/users/1")
        assert response_get.status_code == 200
        assert len(response_get.json()) == 0

    def test_delete_favorite(self, test_app_with_db, get_token_not_manager):
        response_delete = test_app_with_db.delete(f"{self.ENDPOINT_BASE}/1", headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })

        assert response_delete.status_code == 200

        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all", headers={
            "Authorization": f"Bearer {get_token_not_manager}"
        })
        assert response_get.status_code == 200
        assert len(response_get.json()) == 0
