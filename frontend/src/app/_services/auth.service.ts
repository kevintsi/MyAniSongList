import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http"
import { environment } from '../../environments/environment';
import { User } from '../models/User';
import { TokenService } from './token.service';
import { Token } from '../models/Token';
import jwtDecode from 'jwt-decode';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient, private tokenService: TokenService) { }

  public login(user: User) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.post<Token>(this.endpoint + '/users/login', JSON.stringify(user), {
      headers: headers,
      withCredentials: true
    })
  }

  public register(user: User) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json')
    return this.http.post(this.endpoint + '/users/register', JSON.stringify(user), {
      headers: headers
    })

  }

  public update(user: User, file: File) {
    const headers = new HttpHeaders()

    const form_data = new FormData()

    form_data.append("user", JSON.stringify(user))
    form_data.append('profile_picture', file ? file : "")

    return this.http.put(
      this.endpoint + '/users/update/',
      form_data,
      {
        headers: headers,
      })

  }

  public get() {
    return this.http.get<User>(this.endpoint + '/users/me')
  }

  public logout() {
    return this.http.post(this.endpoint + '/users/logout', null, { withCredentials: true })
  }

  public isLoggedIn() {
    return !!this.tokenService.getToken()
  }

  public isManager() {
    let decodedToken: any = jwtDecode(String(this.tokenService.getToken()))
    return decodedToken.sub.is_manager
  }

}
