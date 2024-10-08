import os
from app.db.schemas.artists import ArtistCreate, Artist, ArtistUpdate
from app.firebase import bucket


class TestArtists:
    ENDPOINT_BASE = "/artists"

    def test_create_artist(self, test_app_with_db, get_token_manager):
        artists = [
            {
                "artist": ArtistCreate(name="FLOW", creation_year="1998"),
                "poster_img": "flow_band.jpg",
            },
            {
                "artist": ArtistCreate(
                    name="MAN WITH A MISSION", creation_year="2000"
                ),
                "poster_img": "man_with_a_mission.jpg",
            },
            {
                "artist": ArtistCreate(name="Mile", creation_year="2003"),
                "poster_img": "milet.jpg",
            },
            {
                "artist": ArtistCreate(name="LiSA", creation_year="2005"),
                "poster_img": "LiSA.jpg",
            },
        ]
        for artist in artists:
            with open(
                f"/usr/src/app/tests/images_test/{artist['poster_img']}", "rb"
            ) as f:
                response = test_app_with_db.post(
                    f"{self.ENDPOINT_BASE}/add",
                    data={"artist": artist["artist"].json()},
                    headers={"Authorization": f"Bearer {get_token_manager}"},
                    files={
                        "poster_img": (
                            os.path.basename(f.name),
                            f,
                            "image/jpeg",
                        )
                    },
                )
                
                new_filename = artist["poster_img"].rsplit(".",1)[0]+".webp"

                blob = bucket.blob(
                    f"artist_poster_images/{new_filename}"
                )
                blob.make_public()

                assert response.status_code == 201
                assert response.json()["name"] == artist["artist"].name
                assert (
                    response.json()["creation_year"]
                    == artist["artist"].creation_year
                )
                assert response.json()["poster_img"] == blob.public_url

    def test_get_artist_by_id(self, test_app_with_db):
        blob = bucket.blob("artist_poster_images/flow_band.webp")
        blob.make_public()
        artist = Artist(
            id=1, name="FLOW", creation_year="1998", poster_img=blob.public_url
        )
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/{artist.id}")
        assert response.status_code == 200
        assert response.json()["name"] == artist.name
        assert response.json()["creation_year"] == artist.creation_year
        assert response.json()["poster_img"] == artist.poster_img

    def test_get_artists(self, test_app_with_db):
        response = test_app_with_db.get(f"{self.ENDPOINT_BASE}/all")
        assert response.status_code == 200
        assert response.json()["total"] == 4
        assert type(response.json()["items"]) is list

    def test_update_artist(self, test_app_with_db, get_token_manager):
        artist = ArtistUpdate(name="Milet", creation_year="2003")
        response_put = test_app_with_db.put(
            f"{self.ENDPOINT_BASE}/update/3",
            data={"artist": artist.json()},
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )
        response_get = test_app_with_db.get(
            f"{self.ENDPOINT_BASE}/3",
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )
        assert response_put.status_code == 200
        assert response_get.status_code == 200
        assert response_put.json() == response_get.json()

    def test_delete_artist(self, test_app_with_db, get_token_manager):
        response_delete = test_app_with_db.delete(
            f"{self.ENDPOINT_BASE}/delete/4",
            headers={"Authorization": f"Bearer {get_token_manager}"},
        )
        assert response_delete.status_code == 200
        response_get = test_app_with_db.get(f"{self.ENDPOINT_BASE}/4")
        assert response_get.status_code == 404
