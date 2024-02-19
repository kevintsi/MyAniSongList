
from app.db.schemas.types import Type, TypeCreate, TypeUpdate
from app.db.schemas.languages import LanguageCreate


class TestTypes():
    ENDPOINT_BASE = "/types"

    def test_create_type(self, test_app_with_db, get_token_manager):
        lang = LanguageCreate(code="fr")
        response = test_app_with_db.post("/languages/add", json=lang.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        assert response.status_code == 201

        type = TypeCreate(name="Opening")
        response = test_app_with_db.post(f"{self.ENDPOINT_BASE}/add", json=type.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })
        assert response.status_code == 201
        assert response.json()["name"] == type.name

    def test_get_type_by_id(self, test_app_with_db):
        type = Type(id=1, name="Opening")
        response = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/{type.id}?lang=fr")
        assert response.status_code == 200
        assert response.json() == type

    def test_create_type_translation(self, test_app_with_db, get_token_manager):
        lang = LanguageCreate(code="jp")
        response = test_app_with_db.post("/languages/add", json=lang.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        type_ = TypeCreate(name="エンディング")
        response = test_app_with_db.post(f"{self.ENDPOINT_BASE}/1/add_translation?lang=jp", json=type_.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })
        assert response.status_code == 201

        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/all?lang=jp")
        response_get.status_code == 200
        response_get.json()[0]["name"] == type_.name

    def test_get_types(self, test_app_with_db):
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all?lang=jp")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert type(response.json()) is list

    def test_update_type_translation(self, test_app_with_db, get_token_manager):
        type = TypeUpdate(name="オープニング")
        response = test_app_with_db.put(f"{self.ENDPOINT_BASE}/1/update_translation?lang=jp", json=type.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })
        assert response.status_code == 200
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/1?lang=jp")
        response_get.status_code == 200
        response_get.json()["name"] == type.name
