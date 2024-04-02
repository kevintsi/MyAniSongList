import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { PagedReview, Review } from '../../models/review.model';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReviewService {

  endpoint: string = environment.REST_API_URL
  reviewAdded: Subject<boolean>


  constructor(private http: HttpClient) {
    this.reviewAdded = new Subject<boolean>()
  }

  public getAllByIdMusic(id_music: number, page: number = 1, size: number = 10) {
    return this.http.get<PagedReview>(this.endpoint + '/reviews/music/' + id_music + "?page=" + page + "&size=" + size)
  }

  public getAll(page: number = 1, size: number = 10) {
    return this.http.get<PagedReview>(this.endpoint + '/reviews/all?page=' + page + '&size=' + size)
  }

  public create(review: any) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')

    return this.http.post(
      this.endpoint + '/reviews/add',
      JSON.stringify(review),
      {
        headers: headers,
      }
    )
  }

  public getUserReview(id_music: number) {

    return this.http.get<Review | null>(
      this.endpoint + '/reviews/user/music/' + id_music)
  }

}
