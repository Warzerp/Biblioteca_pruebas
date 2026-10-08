import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export const errorInterceptor: HttpInterceptorFn = (req, next) =>{
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) =>{
      if (error.status === 401) {
        router.navigate(['/login']);
      }
      if (error.status === 403) {
        router.navigate(['/']);
      }
      return throwError(() =>error);
    })
  );
};