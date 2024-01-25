
from app.db.schemas.types import Type, TypeCreate, TypeUpdate


class TestTypes():
    ENDPOINT_BASE = "/types"

    def test_create_type(self, test_app_with_db, get_token_manager):
        types = [TypeCreate(name="Opening"), TypeCreate(
            name="Ending"), TypeCreate(name="OST")]
        for type in types:
            response = test_app_with_db.post(f"{self.ENDPOINT_BASE}/add", json=type.dict(), headers={
                "Authorization": f"Bearer {get_token_manager}"
            })
            assert response.status_code == 201
            assert response.json()["name"] == type.name

    def test_get_type_by_id(self, test_app_with_db):
        type = Type(id=1, name="Opening")
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/{type.id}")
        assert response.status_code == 200
        assert response.json() == type

    def test_create_type_translation(self, test_app_with_db, get_token_manager):
        types = [TypeCreate(name="オープニング"), TypeCreate(name="エンディン")]
        for idx, type in enumerate(types):
            print(f"Index : {idx+1}")
            response = test_app_with_db.post(f"{self.ENDPOINT_BASE}/{idx+1}/add_translation?lang=jp", json=type.dict(), headers={
                "Authorization": f"Bearer {get_token_manager}"
            })
            assert response.status_code == 201

        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/all?lang=jp")
        response_get.status_code == 200
        response_get.json()[0]["name"] == types[0].name
        response_get.json()[1]["name"] == types[1].name

    def test_get_types(self, test_app_with_db):
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all?lang=jp")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert type(response.json()) is list

    def test_update_type(self, test_app_with_db, get_token_manager):
        type = TypeUpdate(name="BGM")
        response_put = test_app_with_db.put(
            f"{self.ENDPOINT_BASE}/update/3", json=type.dict(), headers={
                "Authorization": f"Bearer {get_token_manager}"
            })
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/3", headers={
            "Authorization": f"Bearer {get_token_manager}"
        })
        assert response_put.status_code == 200
        assert response_get.status_code == 200
        assert response_put.json() == response_get.json()

    def test_update_type_translation(self, test_app_with_db, get_token_manager):
        type = TypeUpdate(name="エンディング")
        response = test_app_with_db.put(f"{self.ENDPOINT_BASE}/2/update_translation?lang=jp", json=type.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })
        assert response.status_code == 200
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/2?lang=jp")
        response_get.status_code == 200
        response_get.json()["name"] == type.name
