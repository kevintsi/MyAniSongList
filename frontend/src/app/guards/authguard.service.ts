import { inject } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { ActivatedRouteSnapshot, createUrlTreeFromSnapshot } from '@angular/router';

export const isSignedInGuard = (next: ActivatedRouteSnapshot) => {
  return inject(AuthService).isLoggedIn() ? true : createUrlTreeFromSnapshot(next, ['/', 'login'])
}

export const notSignedInGuard = (next: ActivatedRouteSnapshot) => {
  return !inject(AuthService).isLoggedIn() ? true : createUrlTreeFromSnapshot(next, ['/', 'home'])
}
