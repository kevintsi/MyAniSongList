import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
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

  public getAll(page: number, size: number = 10) {
    return this.http.get<PagedMusic>(this.endpoint + '/musics/all?page=' + page + "&size=" + size)
  }

  public getMusicsAnime(id_anime: number) {
    return this.http.get<Music[]>(this.endpoint + '/musics/anime/' + id_anime)
  }

  public getMusicsArtist(id_artist: number) {
    return this.http.get<Music[]>(this.endpoint + '/musics/artist/' + id_artist)
  }

  public get(id: number) {
    return this.http.get<Music>(this.endpoint + '/musics/' + id)
  }

  public update(id: number, data: any, file: File, selected_anime: Anime, selected_artists: Artist[]) {
    const headers = new HttpHeaders()
    console.log(data.release_date)
    let artists_id = selected_artists.map(artist => artist.id)

    let music = {
      name: data.name,
      release_date: new Date(data.release_date),
      authors: artists_id,
      anime_id: selected_anime.id,
      type_id: data.type_id,
      id_video: data.id_video
    }
    const form_data = new FormData()
    console.log(music)
    form_data.append("music", JSON.stringify(music))
    if (file != null)
      form_data.append('poster_img', file)

    return this.http.put(
      this.endpoint + '/musics/update/' + id,
      form_data,
      {
        headers: headers,
      }
    )
  }

  public create(data: any, file: File, selected_anime: Anime, selected_artists: Artist[]) {
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

    let artists_id = selected_artists.map(artist => artist.id)
    let music = {
      name: data.name,
      release_date: new Date(data.release_date),
      authors: artists_id,
      anime_id: selected_anime.id,
      type_id: data.type_id
    }

    console.log(music)

    const form_data = new FormData()

    form_data.append("music", JSON.stringify(music))
    form_data.append('poster_img', file)

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
