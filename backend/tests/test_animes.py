import os
from app.db.schemas.animes import Anime, AnimeCreate, AnimeUpdate
from app.firebase import bucket
from app.db.schemas.languages import LanguageCreate


class TestAnimes:
    ENDPOINT_BASE = "/animes"

    def test_create_anime(self, test_app_with_db, get_token_manager):
        lang = LanguageCreate(code="fr")
        test_app_with_db.post(
            "/languages/add",
            json=lang.dict(),
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )

        animes = [
            {
                "anime": AnimeCreate(
                    name="Naruto", description="description fr naruto"
                ),
                "poster_img": "naruto_affiche.jpg",
            },
            {
                "anime": AnimeCreate(
                    name="One Pice", description="description fr one piece"
                ),
                "poster_img": "one_piece.jpg",
            },
            {
                "anime": AnimeCreate(
                    name="Vinland Saga",
                    description="description fr vinland saga",
                ),
                "poster_img": "vinland_saga.jpg",
            },
        ]
        for anime in animes:
            with open(
                f"/usr/src/app/tests/images_test/{anime['poster_img']}", "rb"
            ) as f:
                print("Opening....")
                response = test_app_with_db.post(
                    f"{self.ENDPOINT_BASE}/add",
                    data={"anime": anime["anime"].json()},
                    headers={"Authorization": f"Bearer {get_token_manager}"},
                    files={
                        "poster_img": (
                            os.path.basename(f.name),
                            f,
                            "image/jpeg",
                        )
                    },
                )

                new_filename = response.json()["poster_img"].rsplit(".",1)[0]+".webp"

                blob = bucket.blob(
                    f"anime_poster_images/{new_filename}"
                )
                blob.make_public()

                assert response.status_code == 201
                assert response.json()["name"] == anime["anime"].name
                assert (
                    response.json()["description"]
                    == anime["anime"].description
                )
                assert new_filename == blob.public_url

    def test_get_anime_by_id(self, test_app_with_db):
        blob = bucket.blob("anime_poster_images/naruto_affiche.webp")
        blob.make_public()
        anime = Anime(
            id=1,
            name="Naruto",
            description="description fr naruto",
            poster_img=blob.public_url,
        )
        response = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/{anime.id}?lang=fr"
        )
        assert response.status_code == 200
        assert response.json() == anime

    def test_create_anime_translation(
        self, test_app_with_db, get_token_manager
    ):
        lang = LanguageCreate(code="jp")
        test_app_with_db.post(
            "/languages/add",
            json=lang.dict(),
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )

        animes = [
            AnimeCreate(name="ナルト", description="ナルト、説明"),
            AnimeCreate(name="ワンピース", description="ワンピース、説明"),
        ]
        for idx, anime in enumerate(animes):
            print(f"Index : {idx+1}")
            response = test_app_with_db.post(
                f"{self.ENDPOINT_BASE}/{idx+1}/add_translation?lang=jp",
                json=anime.dict(),
                headers={"Authorization": f"Bearer {get_token_manager}"},
            )
            assert response.status_code == 201
            assert response.json()["name"] == anime.name
            assert response.json()["description"] == anime.description

    def test_get_animes(self, test_app_with_db):
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all?lang=jp")
        assert response.status_code == 200
        assert response.json()["total"] == 2
        assert type(response.json()["items"]) is list

    def test_update_anime(self, test_app_with_db, get_token_manager):
        anime = AnimeUpdate(
            name="One Piece", description="description fr one piece updated"
        )
        response_put = test_app_with_db.put(
            f"{self.ENDPOINT_BASE}/update/2?lang=fr",
            data={"anime": anime.json()},
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/2?lang=fr")
        assert response_put.status_code == 200
        assert response_get.status_code == 200
        assert response_put.json() == response_get.json()

    def test_search_anime(self, test_app_with_db):
        response_search = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/search?query=ナル&lang=jp"
        )
        assert response_search.status_code == 200
        response_get_id = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/1?lang=jp"
        )
        response_search.status_code == 200
        response_get_id.status_code == 200
        response_search.json()["total"] == 1
        response_search.json()["items"][0] == response_get_id.json()

    def test_delete_anime(self, test_app_with_db, get_token_manager):
        anime = {
            "anime": AnimeCreate(name="Narut", description="A SUPPRIMER"),
            "poster_img": "naruto.jpg",
        }

        with open(
            f"/usr/src/app/tests/images_test/{anime['poster_img']}", "rb"
        ) as f:
            response_post = test_app_with_db.post(
                f"{self.ENDPOINT_BASE}/add",
                data={"anime": anime["anime"].json()},
                headers={"Authorization": f"Bearer {get_token_manager}"},
                files={
                    "poster_img": (os.path.basename(f.name), f, "image/jpeg")
                },
            )
            response_post.status_code == 201
        response_delete = test_app_with_db.delete(
            f"{self.ENDPOINT_BASE}/delete/{response_post.json()['id']}",
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )
        response_delete.status_code == 200
        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/{response_post.json()['id']}"
        )
        response_get.status_code == 404
