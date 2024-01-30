from datetime import datetime
import os
from app.db.schemas.musics import Music, MusicCreate, MusicUpdate
from app.db.schemas.authors import Author, AuthorCreate
from app.db.schemas.types import Type, TypeCreate
from app.db.schemas.animes import Anime, AnimeCreate
from app.db.schemas.languages import LanguageCreate
from app.firebase import bucket


class TestMusics():
    ENDPOINT_BASE = "/musics"

    def test_create_music(self, test_app_with_db, get_token_manager):
        lang = LanguageCreate(code="fr")
        type = TypeCreate(name="Opening")
        anime = AnimeCreate(name="Kimetsu no Yaiba",
                            description="description fr")
        author = AuthorCreate(name="LiSA", creation_year="2005")
        music = MusicCreate(name="GurengezzzzzFAIL", release_date=datetime(
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
        response_post_music = test_app_with_db.post(f"{self.ENDPOINT_BASE}/add", data={"music": music.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        }, files={"poster_img": (os.path.basename(file_music.name), file_music, "image/jpeg")})

        response_get_music = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/1?lang=fr")

        assert response_post_music.status_code == 201
        assert response_get_music.json()["anime"]["id"] == response_post_music.json()[
            "anime"]["id"]
        assert response_get_music.json(
        )["id"] == response_post_music.json()["id"]
        assert response_get_music.json()["type"]["id"] == response_post_music.json()[
            "type"]["id"]
        assert response_get_music.json()["name"] == response_post_music.json()[
            "name"]

    def test_get_music_by_id(self, test_app_with_db):
        blob_music = bucket.blob(
            f"music_poster_images/Gurenge.jpg")
        blob_music.make_public()

        blob_anime = bucket.blob(
            f"anime_poster_images/demon_slayer.jpg")
        blob_anime.make_public()

        blob_author = bucket.blob(
            f"artist_poster_images/LiSA.jpg")
        blob_anime.make_public()

        music = Music(id=1, name="GurengezzzzzFAIL", avg_note=None,  poster_img=blob_music.public_url, release_date=datetime(
            2018, 10, 1), authors=[Author(id=1, name="LiSA", creation_year="2005", poster_img=blob_author.public_url)], type=Type(id=1, name="Opening"), id_video="x45dsF", anime=Anime(id=1, name="Kimetsu no Yaiba",
                                                                                                                                                                                        description="description fr", poster_img=blob_anime.public_url))

        response = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/{music.id}?lang=fr")
        assert response.status_code == 200
        assert response.json()["name"] == music.name
        assert response.json()["id"] == music.id

    def test_update_music(self, test_app_with_db, get_token_manager):
        music = MusicUpdate(name="Gurenge", release_date=datetime(
            2018, 10, 1), authors=[1], anime_id=1, type_id=1, id_video="xpdo5d")

        response_update = test_app_with_db.put(f"{self.ENDPOINT_BASE}/update/1", data={"music": music.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/1?lang=fr")

        assert response_update.status_code == 200
        assert response_get.status_code == 200

        assert response_update.json()["name"] == response_get.json()["name"]
        assert response_update.json()["id_video"] == response_get.json()[
            "id_video"]

    # def test_create_anime_translation(self, test_app_with_db, get_token_manager):
    #     lang = LanguageCreate(code="jp")
    #     test_app_with_db.post("/languages/add", json=lang.dict(), headers={
    #         "Authorization": f"Bearer {get_token_manager}"
    #     })

    #     animes = [AnimeCreate(name="ナルト", description="ナルト、説明"), AnimeCreate(
    #         name="ワンピース", description="ワンピース、説明")]
    #     for idx, anime in enumerate(animes):
    #         print(f"Index : {idx+1}")
    #         response = test_app_with_db.post(f"{self.ENDPOINT_BASE}/{idx+1}/add_translation?lang=jp", json=anime.dict(), headers={
    #             "Authorization": f"Bearer {get_token_manager}"
    #         })
    #         assert response.status_code == 201
    #         assert response.json()["name"] == anime.name
    #         assert response.json()["description"] == anime.description

    # def test_get_animes(self, test_app_with_db):
    #     response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all?lang=jp")
    #     assert response.status_code == 200
    #     assert response.json()["total"] == 2
    #     assert type(response.json()["items"]) is list

    # def test_update_anime(self, test_app_with_db, get_token_manager):
    #     anime = AnimeUpdate(
    #         name="One Piece", description="description fr one piece updated")
    #     response_put = test_app_with_db.put(
    #         f"{self.ENDPOINT_BASE}/update/2?lang=fr", data={"anime": anime.json()}, headers={
    #             "Authorization": f"Bearer {get_token_manager}"
    #         })
    #     response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/2?lang=fr")
    #     assert response_put.status_code == 200
    #     assert response_get.status_code == 200
    #     assert response_put.json() == response_get.json()

    # def test_search_anime(self, test_app_with_db):
    #     response_search = test_app_with_db.get(
    #         f"{self.ENDPOINT_BASE}/search?query=ナル&lang=jp")
    #     assert response_search.status_code == 200
    #     response_get_id = test_app_with_db.get(
    #         f"{self.ENDPOINT_BASE}/1?lang=jp")
    #     response_search.status_code == 200
    #     response_get_id.status_code == 200
    #     response_search.json()["total"] == 1
    #     response_search.json()["items"][0] == response_get_id.json()

    # def test_delete_anime(self, test_app_with_db, get_token_manager):
    #     anime = {"anime":  AnimeCreate(
    #         name="Narut", description="A SUPPRIMER"), "poster_img": "naruto.jpg"}

    #     with open(f"/usr/src/app/tests/images_test/{anime['poster_img']}", "rb") as f:
    #         response_post = test_app_with_db.post(f"{self.ENDPOINT_BASE}/add", data={"anime": anime["anime"].json()}, headers={
    #             "Authorization": f"Bearer {get_token_manager}"
    #         }, files={"poster_img": (os.path.basename(f.name), f, "image/jpeg")})
    #         response_post.status_code == 201
    #     response_delete = test_app_with_db.delete(
    #         f"{self.ENDPOINT_BASE}/delete/{response_post.json()['id']}", headers={
    #             "Authorization": f"Bearer {get_token_manager}"
    #         })
    #     response_delete.status_code == 200
    #     response_get = test_app_with_db.get(
    #         f"{self.ENDPOINT_BASE}/{response_post.json()['id']}")
    #     response_get.status_code == 404
