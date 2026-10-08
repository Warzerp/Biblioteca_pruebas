import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (route: ActivatedRouteSnapshot) =>{
  const auth = inject(AuthService);
  const router = inject(Router);
  const requiredRoles: string[] = route.data['roles'] ?? [];
  const userRol = auth.usuario()?.rol;

  if (userRol && requiredRoles.includes(userRol)) {
    return true;
  }
  return router.createUrlTree(['/']);
};