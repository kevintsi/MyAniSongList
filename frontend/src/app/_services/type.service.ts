import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Type } from '../models/Type';

@Injectable({
  providedIn: 'root'
})
export class TypeService {

  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public getAll() {
    return this.http.get<Type[]>(this.endpoint + '/types/all')
  }

  public get(id: number) {
    return this.http.get<Type>(this.endpoint + '/types/' + id)
  }

}
