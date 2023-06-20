import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { HttpClient } from '@angular/common/http';
import { PagedReview } from '../models/Review';

@Injectable({
  providedIn: 'root'
})
export class ReviewService {

  endpoint: string = environment.REST_API_URL


  constructor(private http: HttpClient) { }

  public getAll(id_music: number, page: number = 1, size: number = 10) {
    return this.http.get<PagedReview>(this.endpoint + '/reviews/music/' + id_music + "?page=" + page + "&size=" + size)
  }
}
