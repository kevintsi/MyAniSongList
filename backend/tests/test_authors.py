import os
from app.db.schemas.authors import AuthorCreate, Author, AuthorUpdate
from app.firebase import bucket


class TestAuthors:
    ENDPOINT_BASE = "/authors"

    def test_create_author(self, test_app_with_db, get_token_manager):
        authors = [{"author": AuthorCreate(name="FLOW", creation_year="1998"), "poster_img": "flow_band.jpg"},
                   {"author": AuthorCreate(
                       name="MAN WITH A MISSION", creation_year="2000"), "poster_img": "man_with_a_mission.jpg"},
                   {"author": AuthorCreate(name="Mile", creation_year="2003"), "poster_img": "milet.jpg"}, {"author": AuthorCreate(name="LiSA", creation_year="2005"), "poster_img": "LiSA.jpg"}]
        for author in authors:
            with open(f"/usr/src/app/tests/images_test/{author['poster_img']}", "rb") as f:
                response = test_app_with_db.post(f"{self.ENDPOINT_BASE}/add", data={"author": author["author"].json()}, headers={
                    "Authorization": f"Bearer {get_token_manager}"
                }, files={"poster_img": (os.path.basename(f.name), f, "image/jpeg")})

                blob = bucket.blob(
                    f"artist_poster_images/{author['poster_img']}")
                blob.make_public()

                assert response.status_code == 201
                assert response.json()["name"] == author["author"].name
                assert response.json()[
                    "creation_year"] == author["author"].creation_year
                assert response.json()["poster_img"] == blob.public_url

    def test_get_author_by_id(self, test_app_with_db):
        blob = bucket.blob("artist_poster_images/flow_band.jpg")
        blob.make_public()
        author = Author(id=1, name="FLOW", creation_year="1998",
                        poster_img=blob.public_url)
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/{author.id}")
        assert response.status_code == 200
        assert response.json()["name"] == author.name
        assert response.json()[
            "creation_year"] == author.creation_year
        assert response.json()["poster_img"] == author.poster_img

    def test_get_authors(self, test_app_with_db):
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all")
        assert response.status_code == 200
        assert response.json()["total"] == 4
        assert type(response.json()["items"]) is list

    def test_update_author(self, test_app_with_db, get_token_manager):
        author = AuthorUpdate(name="Milet", creation_year="2003")
        response_put = test_app_with_db.put(
            f"{self.ENDPOINT_BASE}/update/3", data={"author": author.json()}, headers={
                "Authorization": f"Bearer {get_token_manager}"
            })
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/3", headers={
            "Authorization": f"Bearer {get_token_manager}"
        })
        assert response_put.status_code == 200
        assert response_get.status_code == 200
        assert response_put.json() == response_get.json()

    def test_delete_author(self, test_app_with_db, get_token_manager):
        response_delete = test_app_with_db.delete(f"{self.ENDPOINT_BASE}/delete/4", headers={
            "Authorization": f"Bearer {get_token_manager}"
        })
        assert response_delete.status_code == 200
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/4")
        assert response_get.status_code == 404
