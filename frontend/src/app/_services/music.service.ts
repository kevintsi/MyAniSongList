import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Music } from '../models/Music';
import { Anime } from '../models/Anime';
import { Artist } from '../models/Artist';

@Injectable({
  providedIn: 'root'
})
export class MusicService {

  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public get_all() {
    return this.http.get<Music[]>(this.endpoint + '/musics/all')
  }

  public get(id: number) {
    return this.http.get<Music>(this.endpoint + '/musics/' + id)
  }

  public update(id: number, data: any, file: File) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    form_data.append("music", JSON.stringify(data))
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

  public create(data: any, file: File, selected_anime: any, selected_artists: Artist[]) {
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
      release_date: data.release_date,
      authors: artists_id,
      anime_id: selected_anime.id,
      type_id: data.type_id
    }

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
