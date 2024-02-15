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

  public search(term: string, lang: string = "fr") {
    return this.http.get<PagedAnime>(this.endpoint + '/animes/search?query=' + term + "&lang=" + lang)
  }

  public getAll(page: number, lang: string = "fr") {
    return this.http.get<PagedAnime>(this.endpoint + '/animes/all?page=' + page + "&lang=" + lang)
  }

  public get(id: number, lang: string = "fr") {
    return this.http.get<Anime>(this.endpoint + '/animes/' + id + "?lang=" + lang)
  }
  public addTranslation(anime: Anime, lang: string) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.post<Anime>(this.endpoint + "/animes/" + anime.id + "/add_translation?lang=" + lang, JSON.stringify(anime), {
      headers: headers
    })
  }
  public update(id: number, data: any, lang: string) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    let anime: Anime = {
      name: data.name,
      description: data.description
    }

    form_data.append("anime", JSON.stringify(anime))
    data?.poster_img ? form_data.append('poster_img', data?.poster_img) : null

    return this.http.put(
      this.endpoint + '/animes/update/' + id + "?lang=" + lang,
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

  public delete(anime: Anime) {
    return this.http.delete(
      this.endpoint + '/animes/delete/' + anime.id)
  }
}
