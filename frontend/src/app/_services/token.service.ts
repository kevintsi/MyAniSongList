import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Token } from '../models/Token';
import { ACCESS_TOKEN_STORAGE_KEY } from '../config/storage';

@Injectable({
  providedIn: 'root'
})
export class TokenService {

  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  setToken(token: Token) {
    localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, token.access_token)
  }
  getToken() {
    return localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY)
  }

  getRefreshToken() {
    return this.http.post<Token>(this.endpoint + '/users/refresh_token', null, { withCredentials: true })
  }

  clean() {
    localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY)

  }
}