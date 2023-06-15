import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { environment } from '../environments/environment';
import jwtDecode from 'jwt-decode';
import { Token } from '../models/Token';

@Injectable({
  providedIn: 'root'
})
export class TokenService {

  endpoint: string = environment.REST_API_URL

  constructor(private http: HttpClient) { }

  setToken(token: Token) {
    localStorage.setItem("access_token", token.access_token)
    let decoded_token: any = jwtDecode(token.refresh_token)
    this.setSecureCookie("refresh_token", token.refresh_token, decoded_token.exp)
  }
  getToken() {
    return localStorage.getItem("access_token")
  }

  getRefreshToken() {
    console.log("GET REFRESH TOKEN")
    return this.http.post<Token>(this.endpoint + '/users/refresh_token', null, { withCredentials: true })
  }

  clean() {
    localStorage.removeItem("access_token")
    this.deleteCookie("refresh_token")

  }

  deleteCookie(name: string): void {
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() - 1);

    const cookieOptions: string[] = [
      `${name}=`,
      `expires=${expirationDate.toUTCString()}`,
      `path=/`
    ];

    document.cookie = cookieOptions.join(';');
  }

  setSecureCookie(name: string, value: string, expirationDays: number): void {
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + expirationDays);

    const cookieOptions: string[] = [
      `${name}=${value}`,
      `expires=${expirationDate.toUTCString()}`,
      `path=/`,
      `secure`,
      `SameSite=Strict`
    ];

    document.cookie = cookieOptions.join(';');
  }

  getCookie(name: string): string {
    const cookieString = decodeURIComponent(document.cookie);
    const cookies = cookieString.split(';');

    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      // Check if the cookie name matches
      if (cookie.startsWith(name + '=')) {
        return cookie.substring(name.length + 1);
      }
    }

    // Return empty string if the cookie is not found
    return '';
  }
}