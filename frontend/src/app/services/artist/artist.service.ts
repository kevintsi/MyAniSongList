import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Artist, PagedArtist } from '../../models/artist.model';

@Injectable({
  providedIn: 'root'
})
export class ArtistService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public search(term: string) {
    return this.http.get<PagedArtist>(this.endpoint + '/artists/search?query=' + term)
  }

  public getAll(page: number) {
    return this.http.get<PagedArtist>(this.endpoint + '/artists/all?page=' + page)
  }

  public get(id: number) {
    return this.http.get<Artist>(this.endpoint + '/artists/' + id)
  }

  public update(id: number, data: any) {
    const headers = new HttpHeaders()

    let artist = {
      name: data.name,
      creation_year: data.creation_year
    }

    const form_data = new FormData()
    form_data.append("artist", JSON.stringify(artist))
    data.poster_img ? form_data.append('poster_img', data.poster_img) : null

    return this.http.put(
      this.endpoint + '/artists/update/' + id,
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

    form_data.append("artist", JSON.stringify(artist))
    form_data.append('poster_img', data.poster_img)

    return this.http.post(
      this.endpoint + '/artists/add',
      form_data,
      {
        headers: headers,
      }
    )
  }

  public delete(id: number) {
    return this.http.delete(
      this.endpoint + '/artists/delete/' + id)
  }
}
