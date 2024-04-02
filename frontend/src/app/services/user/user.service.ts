import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { PagedUser, User } from '../../models/user.model';
import { HttpClient } from '@angular/common/http';
import { Music } from '../../models/music.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public search(term: string) {
    return this.http.get<PagedUser>(this.endpoint + '/users/search?query=' + term)
  }

  public get(id: number) {
    return this.http.get<User>(this.endpoint + '/users/' + id)
  }

  public getFavorites(id: number) {
    return this.http.get<Music[]>(this.endpoint + '/favorites/users/' + id)
  }
}
