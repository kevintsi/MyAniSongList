import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Artist } from '../models/Artist';

@Injectable({
  providedIn: 'root'
})
export class ArtistService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public search(term: string) {
    return this.http.get<Artist[]>(this.endpoint + '/authors/search?query=' + term)
  }

  public getAll() {
    return this.http.get<Artist[]>(this.endpoint + '/authors/all')
  }

  public get(id: number) {
    return this.http.get<Artist>(this.endpoint + '/authors/' + id)
  }

  public update(id: number, data: any, file: File) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    form_data.append("author", JSON.stringify(data))
    if (file != null)
      form_data.append('poster_img', file)

    return this.http.put(
      this.endpoint + '/authors/update/' + id,
      form_data,
      {
        headers: headers,
      }
    )
  }

  public create(data: any, file: File) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    form_data.append("author", JSON.stringify(data))
    form_data.append('poster_img', file)

    return this.http.post(
      this.endpoint + '/authors/add',
      form_data,
      {
        headers: headers,
      }
    )
  }

  public delete(id: number) {
    return this.http.delete(
      this.endpoint + '/authors/delete/' + id)
  }
}
