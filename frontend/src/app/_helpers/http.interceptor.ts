import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HTTP_INTERCEPTORS, HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, switchMap, throwError } from 'rxjs';
import { TokenService } from '../_services/token.service';
import { Token } from '../models/Token';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

    constructor(private tokenService: TokenService) { }

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
                if (error instanceof HttpErrorResponse && error.status === 401) {
                    // Unauthorized error, attempt to refresh the token
                    return this.tokenService.getRefreshToken().pipe(
                        switchMap((token: Token) => {
                            // Update the original request with the new token
                            const updatedRequest = req.clone({
                                setHeaders: {
                                    Authorization: `Bearer ${token.access_token}`
                                }
                            });
                            return next.handle(updatedRequest);
                        }),
                        catchError((refreshError: any) => {
                            this.tokenService.clean()
                            return throwError(() => refreshError);
                        })
                    );
                }

                // For other errors, propagate the error
                return throwError(() => error);
            })
        );



        // const token = this.tokenService.getToken()
        // if (token) {
        //     let decoded_token: any = jwtDecode(token)
        //     if (Date.now() > decoded_token.exp * 1000) {
        //         console.log("Token has expired get a new one bitch")
        //         let new_token = this.tokenService.getRefreshToken()
        //     }
        //     req = req.clone({
        //         headers: req.headers.set("Authorization", "Bearer " + token),
        //     });
        // }

        // console.log("REQ before sending request : ", req)

        // return next.handle(req);
    }
}

export const httpInterceptorProviders = [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
];