import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Music, PagedMusic } from '../models/Music';
import { Anime } from '../models/Anime';
import { Artist } from '../models/Artist';

@Injectable({
  providedIn: 'root'
})
export class MusicService {

  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public search(term: string) {
    return this.http.get<PagedMusic>(this.endpoint + '/musics/search?query=' + term)
  }

  public getAll(page: number, filter: string = 'name') {
    return this.http.get<PagedMusic>(this.endpoint + '/musics/all?order_by=' + filter + '&page=' + page)
  }

  public getPopular() {
    return this.http.get<Music[]>(this.endpoint + '/musics/popular')
  }

  public getLatest() {
    return this.http.get<Music[]>(this.endpoint + '/musics/latest')
  }

  public getFavorites() {
    return this.http.get<Music[]>(this.endpoint + '/favorites/all')
  }
  public addToFavorites(id: number) {
    return this.http.post<Music[]>(this.endpoint + '/favorites/' + id, null)
  }
  public removeFromFavorites(id: number) {
    return this.http.delete<Music[]>(this.endpoint + '/favorites/' + id)
  }

  public getMusicsAnime(id_anime: number, lang: string) {
    return this.http.get<Music[]>(this.endpoint + '/musics/anime/' + id_anime + "?lang=" + lang)
  }

  public getMusicsArtist(id_artist: number, lang: string) {
    return this.http.get<Music[]>(this.endpoint + '/musics/artist/' + id_artist + "?lang=" + lang)
  }

  public get(id: number, lang: string) {
    return this.http.get<Music>(this.endpoint + '/musics/' + id + "?lang=" + lang)
  }

  public update(id: number, data: any) {
    const headers = new HttpHeaders()
    let artists_id = data.selected_artists.map((artist: Artist) => artist.id)

    let music = {
      name: data.name,
      release_date: new Date(data.release_date),
      artists: artists_id,
      anime_id: data.selected_anime.id,
      type_id: data.type_id,
      id_video: data.id_video
    }

    const form_data = new FormData()
    form_data.append("music", JSON.stringify(music))
    if (data.poster_img != null)
      form_data.append('poster_img', data.poster_img)

    return this.http.put(
      this.endpoint + '/musics/update/' + id,
      form_data,
      {
        headers: headers,
      }
    )
  }

  public create(data: any) {
    const headers = new HttpHeaders()
    // {
    //   "name": "string",
    //   "release_date": "string",
    //   "authors": [
    //     0
    //   ],
    //   "anime_id": 0,
    //   "type_id": 0
    // }

    let artists_id = data.selected_artists.map((artist: Artist) => artist.id)
    let music = {
      name: data.name,
      release_date: new Date(data.release_date),
      artists: artists_id,
      anime_id: data.selected_anime.id,
      type_id: data.type_id,
      id_video: data.id_video
    }


    const form_data = new FormData()

    form_data.append("music", JSON.stringify(music))
    form_data.append('poster_img', data.poster_img)

    return this.http.post(
      this.endpoint + '/musics/add',
      form_data,
      {
        headers: headers,
      }
    )
  }

  public delete(id: number) {
    return this.http.delete(
      this.endpoint + '/musics/delete/' + id)
  }
}
