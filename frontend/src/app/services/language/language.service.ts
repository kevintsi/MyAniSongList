import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Language } from '../../models/language.model';
import { Anime } from '../../models/anime.model';
import { Type } from '../../models/type.model';

@Injectable({
  providedIn: 'root'
})
export class LanguageService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public getAll() {
    return this.http.get<Language[]>(this.endpoint + '/languages/all')
  }

  public get(id: number) {
    return this.http.get<Language>(this.endpoint + '/languages/' + id)
  }

  public getSupportedLanguagesByAnime(anime: Anime) {
    return this.http.get<Language[]>(this.endpoint + '/languages/animes/' + anime.id)
  }

  public getSupportedLanguagesByType(type: Type) {
    return this.http.get<Language[]>(this.endpoint + '/languages/types/' + type.id)
  }

  public add(lang: Language) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.post<Language>(this.endpoint + "/languages/add", JSON.stringify(lang), {
      headers: headers
    })
  }

  public update(id: Number, updatedLang: Language) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.put<Language>(this.endpoint + "/languages/update/" + id, JSON.stringify(updatedLang),
      {
        headers: headers
      })
  }

  public delete(lang: Language) {
    return this.http.delete(this.endpoint + "/languages/delete/" + lang.id)
  }

}
