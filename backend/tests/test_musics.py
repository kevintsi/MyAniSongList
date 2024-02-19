from datetime import datetime
import os
from app.db.schemas.musics import Music, MusicCreate, MusicUpdate
from app.db.schemas.artists import Artist, ArtistCreate
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
        artist = ArtistCreate(name="LiSA", creation_year="2005")
        music = MusicCreate(name="GurengezzzzzFAIL", release_date=datetime(
            2018, 10, 1), artists=[1], type_id=1, id_video="x45dsF", anime_id=1)

        response_post_lang = test_app_with_db.post("/languages/add", json=lang.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        assert response_post_lang.status_code == 201

        response_post_type = test_app_with_db.post("/types/add", json=type.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        assert response_post_type.status_code == 201

        file_anime = open(
            "/usr/src/app/tests/images_test/demon_slayer.jpg", mode="rb")

        response_post_anime = test_app_with_db.post("/animes/add", data={"anime": anime.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        }, files={"poster_img": (os.path.basename(file_anime.name), file_anime, "image/jpeg")})

        response_post_anime.status_code == 201

        file_artist = open(
            "/usr/src/app/tests/images_test/LiSA.jpg", mode="rb")
        response_post_artist = test_app_with_db.post("/artists/add", data={"artist": artist.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        }, files={"poster_img": (os.path.basename(file_artist.name), file_artist, "image/jpeg")})

        assert response_post_artist.status_code == 201

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

        blob_artist = bucket.blob(
            f"artist_poster_images/LiSA.jpg")
        blob_anime.make_public()

        music = Music(id=1, name="GurengezzzzzFAIL", avg_note=None,  poster_img=blob_music.public_url, release_date=datetime(
            2018, 10, 1), artists=[Artist(id=1, name="LiSA", creation_year="2005", poster_img=blob_artist.public_url)], type=Type(id=1, name="Opening"), id_video="x45dsF", anime=Anime(id=1, name="Kimetsu no Yaiba",
                                                                                                                                                                                        description="description fr", poster_img=blob_anime.public_url))

        response = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/{music.id}?lang=fr")

        assert response.status_code == 200
        assert response.json()["name"] == music.name
        assert response.json()["id"] == music.id

    def test_update_music(self, test_app_with_db, get_token_manager):
        music = MusicUpdate(name="Gurenge", release_date=datetime(
            2018, 10, 1), artists=[1], anime_id=1, type_id=1, id_video="xpdo5d")

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

    def test_get_musics_by_id_anime(self, test_app_with_db, get_token_manager):
        type_ = TypeCreate(name="Ending")
        artist = ArtistCreate(name="Milet", creation_year="2004")
        music = MusicCreate(name="Koi kogare", release_date=datetime(
            2023, 10, 1), artists=[2], type_id=2, id_video="x45dsF", anime_id=1)

        response_post_type = test_app_with_db.post("/types/add", json=type_.dict(), headers={
            "Authorization": f"Bearer {get_token_manager}"
        })

        assert response_post_type.status_code == 201

        file_artist = open(
            "/usr/src/app/tests/images_test/milet.jpg", mode="rb")
        response_post_artist = test_app_with_db.post("/artists/add", data={"artist": artist.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        }, files={"poster_img": (os.path.basename(file_artist.name), file_artist, "image/jpeg")})

        assert response_post_artist.status_code == 201

        file_music = open(
            "/usr/src/app/tests/images_test/koi_kogare_ending_kny.jpg", mode="rb")

        response_post_music = test_app_with_db.post(f"{self.ENDPOINT_BASE}/add", data={"music": music.json()}, headers={
            "Authorization": f"Bearer {get_token_manager}"
        }, files={"poster_img": (os.path.basename(file_music.name), file_music, "image/jpeg")})

        assert response_post_music.status_code == 201

        response_get_musics_by_id_anime = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/anime/{music.anime_id}?lang=fr")

        assert type(response_get_musics_by_id_anime.json()) is list
        assert len(response_get_musics_by_id_anime.json()) == 2

    def test_get_musics_by_id_artist(self, test_app_with_db):
        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/artist/1?lang=fr")
        assert response_get.status_code == 200
        assert type(response_get.json()) is list
        assert len(response_get.json()) == 1

    def test_search(self, test_app_with_db):
        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/search?query=Gur")
        assert response_get.status_code == 200
        assert response_get.json()["items"][0]["name"] == "Gurenge"
        assert response_get.json()["items"][0]["id"] == 1

    def test_delete(self, test_app_with_db, get_token_manager):
        response_delete = test_app_with_db.delete(f"{self.ENDPOINT_BASE}/delete/1", headers={
            "Authorization": f"Bearer {get_token_manager}"
        })
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/1?lang=fr")

        assert response_delete.status_code == 200
        assert response_get.status_code == 404
