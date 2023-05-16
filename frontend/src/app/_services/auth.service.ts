import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http"
import { environment } from '../environments/environment';
import { User } from '../models/User';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  public login(user: User) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.post(this.endpoint + '/users/login', JSON.stringify(user), {
      headers: headers
    })
  }

  public register(user: User) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.post(this.endpoint + '/users/register', JSON.stringify(user), {
      headers: headers
    })

  }

  public get() {
    return this.http.get(this.endpoint + '/users')
  }

  public logout() {
    return this.http.post(this.endpoint + '/users/logout', null)
  }

  public isLoggedIn() {
    return sessionStorage.getItem("auth-user") != null
  }

}
