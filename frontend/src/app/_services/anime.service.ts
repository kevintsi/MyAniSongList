import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { Anime, PagedAnime } from '../models/Anime';

@Injectable({
  providedIn: 'root'
})
export class AnimeService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public search(term: string) {
    return this.http.get<Anime[]>(this.endpoint + '/animes/search?query=' + term)
  }

  public getAll() {
    return this.http.get<PagedAnime>(this.endpoint + '/animes/all')
  }

  public get(id: number) {
    return this.http.get<Anime>(this.endpoint + '/animes/' + id)
  }

  public update(id: number, data: any, file: File) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    form_data.append("anime", JSON.stringify(data))
    form_data.append('poster_img', file ? file : "")

    return this.http.put(
      this.endpoint + '/animes/update/' + id,
      form_data,
      {
        headers: headers,
      }
    )
  }

  public create(data: any, file: File) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    form_data.append("anime", JSON.stringify(data))
    form_data.append('poster_img', file)

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
