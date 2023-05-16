import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { Anime } from '../models/Anime';

@Injectable({
  providedIn: 'root'
})
export class AnimeService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public get_all() {
    return this.http.get<Anime[]>(this.endpoint + '/animes/all')
  }
}
