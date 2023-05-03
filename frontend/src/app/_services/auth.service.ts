import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http"
import { environment } from '../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  login(username: string, password: string) {
    console.log("Endpoint : " + this.endpoint + "/login")
    const body = new HttpParams()
      .set("username", username)
      .set("password", password)
    const headers = new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    return this.http.post(this.endpoint + '/login', body, {
      headers: headers
    })
  }

  public setSession(authResult: any) {
    localStorage.setItem('id_token', authResult.access_token);
  }

  logout() {
    localStorage.removeItem("id_token");
  }

  public isLoggedIn() {
    return localStorage.getItem("id_token") != null
  }

}
