import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Type } from '../models/Type';

@Injectable({
  providedIn: 'root'
})
export class TypeService {

  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public getAll(lang: String = "fr") {
    return this.http.get<Type[]>(this.endpoint + '/types/all?lang=' + lang)
  }

  public get(id: number, lang: String = "fr") {
    return this.http.get<Type>(this.endpoint + '/types/' + id + "?lang=" + lang)
  }

  public add(type: Type) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.post<Type>(this.endpoint + "/types/add", JSON.stringify(type), {
      headers: headers
    })
  }

  public addTranslation(type: Type, lang: String = "fr") {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.post<Type>(this.endpoint + "/types/" + type.id + "/add_translation?lang=" + lang, JSON.stringify(type), {
      headers: headers
    })
  }

  public updateTranslation(id: number, updatedType: Type, lang: String = "fr") {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.put<Type>(this.endpoint + "/types/" + id + "/update_translation?lang=" + lang, JSON.stringify(updatedType), {
      headers: headers
    })
  }

  public delete(type: Type) {
    return this.http.delete(this.endpoint + "/types/delete/" + type.id)
  }

}
