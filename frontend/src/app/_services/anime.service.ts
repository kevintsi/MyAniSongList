import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Anime, PagedAnime } from '../models/Anime';

@Injectable({
  providedIn: 'root'
})
export class AnimeService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public search(term: string) {
    return this.http.get<PagedAnime>(this.endpoint + '/animes/search?query=' + term)
  }

  public getAll(page: number) {
    return this.http.get<PagedAnime>(this.endpoint + '/animes/all?page=' + page)
  }

  public get(id: number) {
    return this.http.get<Anime>(this.endpoint + '/animes/' + id)
  }

  public update(id: number, data: any) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    let anime = {
      name: data.name,
      description: data.description
    }

    form_data.append("anime", JSON.stringify(anime))
    form_data.append('poster_img', data.poster_img ? data.poster_img : "")

    return this.http.put(
      this.endpoint + '/animes/update/' + id,
      form_data,
      {
        headers: headers,
      }
    )
  }

  public create(data: any) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    let anime = {
      name: data.name,
      description: data.description
    }

    form_data.append("anime", JSON.stringify(anime))
    form_data.append('poster_img', data.poster_img)

    return this.http.post(
      this.endpoint + '/animes/add',
      form_data,
      {
        headers: headers,
      }
    )
  }

  public delete(id: number) {
    return this.http.delete(
      this.endpoint + '/animes/delete/' + id)
  }
}
