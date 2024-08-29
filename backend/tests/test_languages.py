from app.db.schemas.languages import Language, LanguageCreate, LanguageUpdate


class TestLanguages:
    ENDPOINT_BASE = "/languages"

    def test_create_language(self, test_app_with_db, get_token_manager):
        languages = [
            LanguageCreate(code="fr"),
            LanguageCreate(code="en"),
            LanguageCreate(code="ch"),
            LanguageCreate(code="it"),
        ]
        for lang in languages:
            response = test_app_with_db.post(
                f"{self.ENDPOINT_BASE}/add",
                json=lang.dict(),
                headers={"Authorization": f"Bearer {get_token_manager}"},
            )
            assert response.status_code == 201
            assert response.json()["code"] == lang.code

    def test_get_language_by_id(self, test_app_with_db):
        lang = Language(id=1, code="fr")
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/{lang.id}")
        assert response.status_code == 200
        assert response.json() == lang

    def test_get_languages(self, test_app_with_db):
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all")
        assert response.status_code == 200
        assert len(response.json()) == 4
        assert type(response.json()) is list

    def test_update_language(self, test_app_with_db, get_token_manager):
        lang = LanguageUpdate(code="jp")
        response_put = test_app_with_db.put(
            f"{self.ENDPOINT_BASE}/update/3",
            json=lang.dict(),
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )
        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/3",
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )
        assert response_put.status_code == 200
        assert response_get.status_code == 200
        assert response_put.json() == response_get.json()

    def test_delete_language(self, test_app_with_db, get_token_manager):
        response = test_app_with_db.delete(
            f"{self.ENDPOINT_BASE}/delete/4",
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )
        assert response.status_code == 200
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/4")
        assert response_get.status_code == 404
