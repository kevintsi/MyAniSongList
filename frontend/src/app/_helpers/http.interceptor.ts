import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HTTP_INTERCEPTORS, HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, switchMap, throwError } from 'rxjs';
import { TokenService } from '../_services/token.service';
import { Token } from '../models/Token';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

    constructor(private tokenService: TokenService, private router: Router) { }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        console.log('Intercept...')
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
                if (error instanceof HttpErrorResponse && error.status === 401) {
                    console.log('Error when calling API access token probably expired')
                    console.log("CALL REFRESH TOKEN API")
                    return this.tokenService.getRefreshToken().pipe(
                        switchMap((token: Token) => {
                            // Update the original request with the new token
                            console.log("New access token gotten")
                            const updatedRequest = req.clone({
                                setHeaders: {
                                    Authorization: `Bearer ${token.access_token}`
                                }
                            });
                            return next.handle(updatedRequest);
                        }),
                        catchError(() => {
                            console.log('Error from calling refresh token caught')
                            this.tokenService.clean()
                            this.router.navigateByUrl("/login")
                            return throwError(() => new Error('Error when calling refresh token, cleaning cookies and local storage'))
                        })
                    )
                }
                // For other errors, propagate the error
                return throwError(() => new Error(error.message));
            })
        )
    }
}

export const httpInterceptorProviders = [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
];