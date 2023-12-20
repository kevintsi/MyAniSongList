import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Token } from '../models/Token';

@Injectable({
  providedIn: 'root'
})
export class TokenService {

  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  setToken(token: Token) {
    localStorage.setItem("access_token", token.access_token)
  }
  getToken() {
    return localStorage.getItem("access_token")
  }

  getRefreshToken() {
    return this.http.post<Token>(this.endpoint + '/users/refresh_token', null, { withCredentials: true })
  }

  clean() {
    localStorage.removeItem("access_token")

  }
}