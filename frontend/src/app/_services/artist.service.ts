import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Artist, PagedArtist } from '../models/Artist';

@Injectable({
  providedIn: 'root'
})
export class ArtistService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public search(term: string) {
    return this.http.get<PagedArtist>(this.endpoint + '/authors/search?query=' + term)
  }

  public getAll(page: number, size: number = 10) {
    return this.http.get<PagedArtist>(this.endpoint + '/authors/all?page=' + page + "&size=" + size)
  }

  public get(id: number) {
    return this.http.get<Artist>(this.endpoint + '/authors/' + id)
  }

  public update(id: number, data: any) {
    const headers = new HttpHeaders()

    let artist = {
      name: data.name,
      creation_year: data.creation_year
    }

    const form_data = new FormData()

    form_data.append("author", JSON.stringify(artist))
    if (data.file != null)
      form_data.append('poster_img', data.file)

    return this.http.put(
      this.endpoint + '/authors/update/' + id,
      form_data,
      {
        headers: headers,
      }
    )
  }

  public create(data: any) {
    const headers = new HttpHeaders()

    let artist = {
      name: data.name,
      creation_year: data.creation_year
    }

    const form_data = new FormData()

    form_data.append("author", JSON.stringify(artist))
    form_data.append('poster_img', data.poster_img)

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
