import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { LoginRequest, LoginResponse, RegistroRequest, Usuario } from '../../models/usuario.model';

const API = 'http://localhost:8000/api/v1/auth';
const TOKEN_KEY = 'biblioteca_access';
const REFRESH_KEY = 'biblioteca_refresh';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _usuario = signal<Usuario | null>(null);

  readonly usuario = this._usuario.asReadonly();
  readonly isLoggedIn = computed(() =>this._usuario() !== null);
  readonly esAdmin = computed(() =>
    this._usuario()?.rol === 'ADMIN' || this._usuario()?.rol === 'BIBLIOTECARIO'
  );

  constructor(private http: HttpClient, private router: Router) {
    this.cargarPerfil();
  }

  login(credentials: LoginRequest): Observable<LoginResponse>{
    return this.http.post<LoginResponse>(`${API}/login/`, credentials).pipe(
      tap((tokens) =>{
        localStorage.setItem(TOKEN_KEY, tokens.access);
        localStorage.setItem(REFRESH_KEY, tokens.refresh);
        this.cargarPerfil();
      })
    );
  }

  registro(data: RegistroRequest): Observable<Usuario>{
    return this.http.post<Usuario>(`${API}/registro/`, data);
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    this._usuario.set(null);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_KEY);
  }

  cargarPerfil(): void {
    const token = this.getToken();
    if (!token) return;
    this.http.get<Usuario>(`${API}/perfil/`).subscribe({
      next: (user) =>this._usuario.set(user),
      error: () =>this.logout(),
    });
  }

  refreshToken(): Observable<LoginResponse>{
    const refresh = this.getRefreshToken();
    return this.http.post<LoginResponse>(`${API}/refresh/`, { refresh }).pipe(
      tap((tokens) =>localStorage.setItem(TOKEN_KEY, tokens.access))
    );
  }
}