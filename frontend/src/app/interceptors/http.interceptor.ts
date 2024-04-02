import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HTTP_INTERCEPTORS, HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, switchMap, throwError } from 'rxjs';
import { TokenService } from '../services/token/token.service';
import { Token } from '../models/token.model';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

    constructor(private tokenService: TokenService, private router: Router) { }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        let token = this.tokenService.getToken()
        if (!!token) {
            req = req.clone({
                setHeaders: {
                    Authorization: `Bearer ${token}`
                }
            })
        }

        return next.handle(req).pipe(
            catchError((error: any) => {
                if (error instanceof HttpErrorResponse && error.status === 401 && error.error.detail == "Token has expired") {
                    console.log('Error when calling API access token probably expired')
                    return this.tokenService.getRefreshToken().pipe(
                        switchMap((token: Token) => {
                            const updatedRequest = req.clone({
                                setHeaders: {
                                    Authorization: `Bearer ${token.access_token}`
                                }
                            });
                            this.tokenService.setToken(token)
                            return next.handle(updatedRequest);
                        }),
                        catchError(() => {
                            console.log('Error from calling refresh token caught')
                            this.tokenService.clean()
                            this.router.navigateByUrl("/login")
                            return throwError(() => new Error('Error when calling refresh token, cleaning cookies and local storage'))
                        })
                    )
                } else if (error.status === 404 && error.error.detail != "Invalid username or password") {
                    this.router.navigateByUrl("/404", { skipLocationChange: true })
                }
                else if (error.status === 403) {
                    this.router.navigateByUrl("/login")
                }
                // For other errors, propagate the error
                return throwError(() => new HttpErrorResponse(error));
            })
        )
    }
}

export const httpInterceptorProviders = [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
];