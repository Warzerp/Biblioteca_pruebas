import os
import json

base_dir = r"c:\Users\USUARIO\Desktop\DOAP - copia\frontend"

files = {
    "package.json": """{
  "name": "biblioteca-frontend",
  "version": "1.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "watch": "ng build --watch --configuration development",
    "test": "ng test"
  },
  "private": true,
  "dependencies": {
    "@angular/animations": "^17.0.0",
    "@angular/common": "^17.0.0",
    "@angular/compiler": "^17.0.0",
    "@angular/core": "^17.0.0",
    "@angular/forms": "^17.0.0",
    "@angular/platform-browser": "^17.0.0",
    "@angular/platform-browser-dynamic": "^17.0.0",
    "@angular/router": "^17.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.6.2",
    "zone.js": "~0.14.2"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^17.0.0",
    "@angular/cli": "^17.0.0",
    "@angular/compiler-cli": "^17.0.0",
    "typescript": "~5.2.2"
  }
}""",
    "tsconfig.json": """{
  "compileOnSave": false,
  "compilerOptions": {
    "outDir": "./dist/out-tsc",
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "sourceMap": true,
    "declaration": false,
    "experimentalDecorators": true,
    "moduleResolution": "bundler",
    "importHelpers": true,
    "target": "ES2022",
    "module": "ES2022",
    "useDefineForClassFields": false,
    "lib": ["ES2022", "dom"]
  },
  "angularCompilerOptions": {
    "enableI18nLegacyMessageIdFormat": false,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  }
}""",
    "angular.json": """{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "biblioteca-frontend": {
      "projectType": "application",
      "schematics": {},
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:application",
          "options": {
            "outputPath": "dist/biblioteca-frontend",
            "index": "src/index.html",
            "browser": "src/main.ts",
            "polyfills": [
              "zone.js"
            ],
            "tsConfig": "tsconfig.json",
            "assets": [
              "src/favicon.ico",
              "src/assets"
            ],
            "styles": [
              "src/styles.css"
            ],
            "scripts": []
          },
          "configurations": {
            "production": {
              "budgets": [
                {
                  "type": "initial",
                  "maximumWarning": "500kb",
                  "maximumError": "1mb"
                },
                {
                  "type": "anyComponentStyle",
                  "maximumWarning": "2kb",
                  "maximumError": "4kb"
                }
              ],
              "outputHashing": "all"
            },
            "development": {
              "optimization": false,
              "extractLicenses": false,
              "sourceMap": true
            }
          },
          "defaultConfiguration": "production"
        },
        "serve": {
          "builder": "@angular-devkit/build-angular:dev-server",
          "configurations": {
            "production": {
              "buildTarget": "biblioteca-frontend:build:production"
            },
            "development": {
              "buildTarget": "biblioteca-frontend:build:development"
            }
          },
          "defaultConfiguration": "development"
        }
      }
    }
  }
}""",
    "src/index.html": """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Biblioteca Digital</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root></app-root>
</body>
</html>""",
    "src/main.ts": """import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));""",
    "src/styles.css": """/* Estilos globales de la Biblioteca Digital */
:root {
  --primary: #1a3a5c;
  --secondary: #2e7d32;
  --accent: #f57c00;
  --danger: #c62828;
  --bg: #f5f5f5;
  --text: #212121;
  --white: #ffffff;
  --card-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }

button {
  cursor: pointer;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  transition: background 0.2s;
}

.btn-primary {
  background: var(--primary);
  color: var(--white);
}
.btn-primary:hover { background: #0d2540; }

.btn-secondary {
  background: var(--secondary);
  color: var(--white);
}

.btn-danger {
  background: var(--danger);
  color: var(--white);
}

.card {
  background: var(--white);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  padding: 16px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.grid-libros {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.alert {
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.alert-error { background: #ffcdd2; color: var(--danger); }
.alert-success { background: #c8e6c9; color: var(--secondary); }
.alert-warning { background: #ffe0b2; color: #e65100; }

input, select, textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

input:focus, select:focus, textarea:focus {
  outline: 2px solid var(--primary);
  border-color: var(--primary);
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 600;
  font-size: 14px;
}

.spinner {
  display: flex;
  justify-content: center;
  padding: 40px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

th { background: var(--primary); color: var(--white); }

tr:hover td { background: #f5f5f5; }

badge, .badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.badge-active { background: #c8e6c9; color: #1b5e20; }
.badge-pending { background: #fff3e0; color: #e65100; }
.badge-danger { background: #ffcdd2; color: #b71c1c; }""",
    "src/app/app.component.ts": """import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { FooterComponent } from './shared/components/footer/footer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, FooterComponent],
  template: `
    <app-navbar />
    <main class="container" style="padding: 24px 16px; min-height: calc(100vh - 130px);">
      <router-outlet />
    </main>
    <app-footer />
  `,
})
export class AppComponent {}""",
    "src/app/app.config.ts": """import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { routes } from './app.routes';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { errorInterceptor } from './core/interceptors/error.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor, errorInterceptor])),
    provideAnimations(),
  ],
};""",
    "src/app/app.routes.ts": """import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/catalogo/pages/catalogo-list/catalogo-list.component')
        .then(m => m.CatalogoListComponent),
  },
  {
    path: 'libro/:id',
    loadComponent: () =>
      import('./features/catalogo/pages/libro-detail/libro-detail.component')
        .then(m => m.LibroDetailComponent),
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/pages/login/login.component')
        .then(m => m.LoginComponent),
  },
  {
    path: 'registro',
    loadComponent: () =>
      import('./features/auth/pages/register/register.component')
        .then(m => m.RegisterComponent),
  },
  {
    path: 'panel',
    canActivate: [authGuard],
    children: [
      {
        path: 'reservas',
        loadComponent: () =>
          import('./features/reservas/pages/mis-reservas/mis-reservas.component')
            .then(m => m.MisReservasComponent),
      },
      {
        path: 'prestamos',
        loadComponent: () =>
          import('./features/prestamos/pages/mis-prestamos/mis-prestamos.component')
            .then(m => m.MisPrestamosComponent),
      },
      {
        path: 'multas',
        loadComponent: () =>
          import('./features/multas/pages/mis-multas/mis-multas.component')
            .then(m => m.MisMultasComponent),
      },
      { path: '', redirectTo: 'reservas', pathMatch: 'full' },
    ],
  },
  {
    path: 'admin',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['BIBLIOTECARIO', 'ADMIN'] },
    children: [
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/admin/pages/dashboard/dashboard.component')
            .then(m => m.DashboardComponent),
      },
      {
        path: 'libros',
        loadComponent: () =>
          import('./features/admin/pages/crud-libros/crud-libros.component')
            .then(m => m.CrudLibrosComponent),
      },
      {
        path: 'ejemplares',
        loadComponent: () =>
          import('./features/admin/pages/crud-ejemplares/crud-ejemplares.component')
            .then(m => m.CrudEjemplaresComponent),
      },
      {
        path: 'prestamos',
        loadComponent: () =>
          import('./features/prestamos/pages/gestion-prestamos/gestion-prestamos.component')
            .then(m => m.GestionPrestamosComponent),
      },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    ],
  },
  { path: '**', redirectTo: '' },
];""",
    "src/app/models/usuario.model.ts": """export interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  telefono: string;
  rol: 'LECTOR' | 'BIBLIOTECARIO' | 'ADMIN';
  is_active: boolean;
  date_joined: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RegistroRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  telefono?: string;
}""",
    "src/app/models/libro.model.ts": """export interface Autor {
  id: number;
  nombre: string;
  nacionalidad: string;
  biografia: string;
}

export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
}

export interface Libro {
  id: number;
  isbn: string;
  titulo: string;
  sinopsis: string;
  categoria: Categoria | null;
  autores: Autor[];
  anio_publicacion: number | null;
  portada_url: string;
  activo: boolean;
  ejemplares_disponibles: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}""",
    "src/app/models/ejemplar.model.ts": """export type EstadoEjemplar = 'DISPONIBLE' | 'PRESTADO' | 'RESERVADO' | 'MANTENIMIENTO' | 'EXTRAVIADO';

export interface Ejemplar {
  id: number;
  libro: number;
  libro_titulo?: string;
  codigo_inventario: string;
  ubicacion_estante: string;
  estado: EstadoEjemplar;
}""",
    "src/app/models/reserva.model.ts": """export type EstadoReserva = 'PENDIENTE' | 'ASIGNADA' | 'CANCELADA' | 'EXPIRADA' | 'COMPLETADA';

export interface Reserva {
  id: number;
  usuario: number;
  usuario_username?: string;
  libro: number;
  libro_titulo?: string;
  fecha_reserva: string;
  fecha_expiracion: string;
  estado: EstadoReserva;
}""",
    "src/app/models/prestamo.model.ts": """export type EstadoPrestamo = 'ACTIVO' | 'DEVUELTO' | 'CON_MORA' | 'EXTRAVIADO';

export interface Prestamo {
  id: number;
  usuario: number;
  usuario_username?: string;
  ejemplar: number;
  ejemplar_codigo?: string;
  libro_titulo?: string;
  fecha_prestamo: string;
  fecha_limite_devolucion: string;
  fecha_devolucion_real: string | null;
  estado: EstadoPrestamo;
  observaciones: string;
}""",
    "src/app/models/multa.model.ts": """export type EstadoMulta = 'PENDIENTE' | 'PAGADA' | 'CONDONADA';

export interface Multa {
  id: number;
  usuario: number;
  usuario_username?: string;
  prestamo: number;
  monto: string;
  motivo: string;
  estado: EstadoMulta;
  fecha_generacion: string;
  fecha_pago: string | null;
}""",
    "src/app/core/services/auth.service.ts": """import { Injectable, signal, computed } from '@angular/core';
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
  readonly isLoggedIn = computed(() => this._usuario() !== null);
  readonly esAdmin = computed(() =>
    this._usuario()?.rol === 'ADMIN' || this._usuario()?.rol === 'BIBLIOTECARIO'
  );

  constructor(private http: HttpClient, private router: Router) {
    this.cargarPerfil();
  }

  login(credentials: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${API}/login/`, credentials).pipe(
      tap((tokens) => {
        localStorage.setItem(TOKEN_KEY, tokens.access);
        localStorage.setItem(REFRESH_KEY, tokens.refresh);
        this.cargarPerfil();
      })
    );
  }

  registro(data: RegistroRequest): Observable<Usuario> {
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
      next: (user) => this._usuario.set(user),
      error: () => this.logout(),
    });
  }

  refreshToken(): Observable<LoginResponse> {
    const refresh = this.getRefreshToken();
    return this.http.post<LoginResponse>(`${API}/refresh/`, { refresh }).pipe(
      tap((tokens) => localStorage.setItem(TOKEN_KEY, tokens.access))
    );
  }
}""",
    "src/app/core/interceptors/auth.interceptor.ts": """import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    });
  }

  return next(req);
};""",
    "src/app/core/interceptors/error.interceptor.ts": """import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        router.navigate(['/login']);
      }
      if (error.status === 403) {
        router.navigate(['/']);
      }
      return throwError(() => error);
    })
  );
};""",
    "src/app/core/guards/auth.guard.ts": """import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (auth.isLoggedIn()) {
    return true;
  }
  return router.createUrlTree(['/login']);
};""",
    "src/app/core/guards/role.guard.ts": """import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const requiredRoles: string[] = route.data['roles'] ?? [];
  const userRol = auth.usuario()?.rol;

  if (userRol && requiredRoles.includes(userRol)) {
    return true;
  }
  return router.createUrlTree(['/']);
};""",
    "src/app/shared/components/navbar/navbar.component.ts": """import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, CommonModule],
  template: `
    <header style="background: var(--primary); color: white; padding: 12px 0;">
      <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
        <a routerLink="/" style="color: white; font-size: 1.3rem; font-weight: 700;">📚 Biblioteca Digital</a>
        <nav style="display: flex; gap: 16px; align-items: center;">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}" style="color: rgba(255,255,255,0.85);">Catálogo</a>
          @if (auth.isLoggedIn()) {
            <a routerLink="/panel/reservas" style="color: rgba(255,255,255,0.85);">Mis Reservas</a>
            <a routerLink="/panel/prestamos" style="color: rgba(255,255,255,0.85);">Mis Préstamos</a>
            <a routerLink="/panel/multas" style="color: rgba(255,255,255,0.85);">Mis Multas</a>
            @if (auth.esAdmin()) {
              <a routerLink="/admin/dashboard" style="color: #ffe082;">Panel Admin</a>
            }
            <button class="btn-danger" (click)="auth.logout()" style="padding: 6px 14px;">Cerrar sesión</button>
          } @else {
            <a routerLink="/login" style="color: rgba(255,255,255,0.85);">Iniciar sesión</a>
            <a routerLink="/registro" style="color: rgba(255,255,255,0.85);">Registrarse</a>
          }
        </nav>
      </div>
    </header>
  `,
})
export class NavbarComponent {
  auth = inject(AuthService);
}""",
    "src/app/shared/components/footer/footer.component.ts": """import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  standalone: true,
  template: `
    <footer style="background: var(--primary); color: rgba(255,255,255,0.8); padding: 24px 0; margin-top: 40px;">
      <div class="container" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 24px;">
        <div>
          <strong style="color: white;">📚 Biblioteca Digital</strong>
          <ul style="list-style: none; margin-top: 8px;">
            <li>Catálogo de libros</li>
            <li>Sistema de reservas</li>
            <li>Gestión de préstamos</li>
          </ul>
        </div>
        <div>
          <strong style="color: white;">Contacto</strong>
          <ul style="list-style: none; margin-top: 8px;">
            <li>📍 Calle Victoria</li>
            <li>📞 0-600-libros</li>
            <li>✉️ labiblio&#64;gmail.com</li>
            <li>🕐 24/7</li>
          </ul>
        </div>
        <div>
          <strong style="color: white;">Tecnologías</strong>
          <ul style="list-style: none; margin-top: 8px;">
            <li>Django REST Framework</li>
            <li>Angular 17+</li>
            <li>PostgreSQL</li>
          </ul>
        </div>
      </div>
      <p style="text-align: center; margin-top: 16px; font-size: 12px;">© 2024 Biblioteca Digital. Todos los derechos reservados.</p>
    </footer>
  `,
})
export class FooterComponent {}""",
    "src/app/shared/components/book-card/book-card.component.ts": """import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Libro } from '../../../models/libro.model';

@Component({
  selector: 'app-book-card',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="card" style="display: flex; flex-direction: column; gap: 8px; height: 100%;">
      <img
        [src]="libro.portada_url || 'https://via.placeholder.com/150x200?text=Sin+portada'"
        [alt]="libro.titulo"
        style="width: 100%; height: 200px; object-fit: cover; border-radius: 4px;"
      >
      <h3 style="font-size: 14px; line-height: 1.3;">{{ libro.titulo }}</h3>
      <p style="font-size: 12px; color: #666;">
        {{ libro.autores.length ? libro.autores[0].nombre : 'Autor desconocido' }}
      </p>
      <p style="font-size: 12px;">
        <span
          class="badge"
          [class.badge-active]="libro.ejemplares_disponibles > 0"
          [class.badge-danger]="libro.ejemplares_disponibles === 0"
        >
          {{ libro.ejemplares_disponibles > 0 ? libro.ejemplares_disponibles + ' disponibles' : 'Sin stock' }}
        </span>
      </p>
      <div style="margin-top: auto; display: flex; gap: 8px;">
        <a [routerLink]="['/libro', libro.id]" class="btn-primary" style="display: block; text-align: center; padding: 6px 12px; border-radius: 4px; font-size: 13px;">Ver detalle</a>
        @if (libro.ejemplares_disponibles > 0) {
          <button class="btn-secondary" style="font-size: 13px; padding: 6px 12px;" (click)="reservar.emit(libro)">Reservar</button>
        }
      </div>
    </div>
  `,
})
export class BookCardComponent {
  @Input({ required: true }) libro!: Libro;
  @Output() reservar = new EventEmitter<Libro>();
}""",
    "src/app/shared/components/alert-modal/alert-modal.component.ts": """import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alert-modal',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (visible) {
      <div style="position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
        <div class="card" style="max-width: 400px; width: 90%;">
          <h3 style="margin-bottom: 12px;">{{ titulo }}</h3>
          <p style="margin-bottom: 16px;">{{ mensaje }}</p>
          <div style="display: flex; gap: 8px; justify-content: flex-end;">
            @if (confirmText) {
              <button class="btn-primary" (click)="confirmar.emit(); visible = false">{{ confirmText }}</button>
            }
            <button (click)="cancelar.emit(); visible = false" style="background: #e0e0e0;">{{ cancelText }}</button>
          </div>
        </div>
      </div>
    }
  `,
})
export class AlertModalComponent {
  @Input() titulo = 'Aviso';
  @Input() mensaje = '';
  @Input() confirmText = 'Confirmar';
  @Input() cancelText = 'Cancelar';
  @Input() visible = false;
  @Output() confirmar = new EventEmitter<void>();
  @Output() cancelar = new EventEmitter<void>();
}""",
    "src/app/shared/pipes/safe-url.pipe.ts": """import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';

@Pipe({
  name: 'safeUrl',
  standalone: true,
})
export class SafeUrlPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(url: string): SafeUrl {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }
}""",
    "src/app/features/catalogo/services/catalogo.service.ts": """import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Libro, Categoria, Autor, PaginatedResponse } from '../../../models/libro.model';

const API = 'http://localhost:8000/api/v1/catalogo';

@Injectable({ providedIn: 'root' })
export class CatalogoService {
  private http = inject(HttpClient);

  getLibros(filtros: { busqueda?: string; categoria?: number; pagina?: number } = {}): Observable<PaginatedResponse<Libro>> {
    let params = new HttpParams();
    if (filtros.busqueda) params = params.set('search', filtros.busqueda);
    if (filtros.categoria) params = params.set('categoria', filtros.categoria.toString());
    if (filtros.pagina) params = params.set('page', filtros.pagina.toString());
    return this.http.get<PaginatedResponse<Libro>>(`${API}/libros/`, { params });
  }

  getLibro(id: number): Observable<Libro> {
    return this.http.get<Libro>(`${API}/libros/${id}/`);
  }

  getCategorias(): Observable<PaginatedResponse<Categoria>> {
    return this.http.get<PaginatedResponse<Categoria>>(`${API}/categorias/`);
  }

  crearLibro(data: Partial<Libro>): Observable<Libro> {
    return this.http.post<Libro>(`${API}/libros/`, data);
  }

  actualizarLibro(id: number, data: Partial<Libro>): Observable<Libro> {
    return this.http.patch<Libro>(`${API}/libros/${id}/`, data);
  }
}""",
    "src/app/features/catalogo/pages/catalogo-list/catalogo-list.component.ts": """import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CatalogoService } from '../../services/catalogo.service';
import { BookCardComponent } from '../../../../shared/components/book-card/book-card.component';
import { Libro, Categoria, PaginatedResponse } from '../../../../models/libro.model';
import { ReservaService } from '../../../reservas/services/reserva.service';
import { AuthService } from '../../../../core/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-catalogo-list',
  standalone: true,
  imports: [CommonModule, FormsModule, BookCardComponent],
  template: `
    <section>
      <h1 style="margin-bottom: 16px;">📚 Catálogo de Libros</h1>

      <!-- Filtros -->
      <div style="display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap;">
        <input
          [(ngModel)]="busqueda"
          placeholder="Buscar por título o autor..."
          style="flex: 1; min-width: 200px;"
          (keyup.enter)="buscar()"
        >
        <select [(ngModel)]="categoriaSeleccionada" (change)="buscar()" style="min-width: 160px;">
          <option [ngValue]="null">Todas las categorías</option>
          @for (cat of categorias(); track cat.id) {
            <option [ngValue]="cat.id">{{ cat.nombre }}</option>
          }
        </select>
        <button class="btn-primary" (click)="buscar()">Buscar</button>
      </div>

      <!-- Resultados -->
      @if (cargando()) {
        <div class="spinner"><p>Cargando libros...</p></div>
      } @else if (libros().length === 0) {
        <div class="alert alert-warning">No se encontraron libros con esos criterios.</div>
      } @else {
        <p style="margin-bottom: 12px; color: #666;">{{ total() }} libro(s) encontrado(s)</p>
        <div class="grid-libros">
          @for (libro of libros(); track libro.id) {
            <app-book-card [libro]="libro" (reservar)="onReservar($event)" />
          }
        </div>

        <!-- Paginación -->
        <div style="display: flex; gap: 8px; justify-content: center; margin-top: 24px;">
          <button [disabled]="pagina() === 1" (click)="cambiarPagina(pagina() - 1)" style="background: #e0e0e0;">Anterior</button>
          <span style="padding: 8px;">Página {{ pagina() }}</span>
          <button [disabled]="!hayMas()" (click)="cambiarPagina(pagina() + 1)" style="background: #e0e0e0;">Siguiente</button>
        </div>
      }

      @if (mensaje()) {
        <div class="alert" [class.alert-success]="!error()" [class.alert-error]="error()" style="position: fixed; bottom: 20px; right: 20px; max-width: 300px;">
          {{ mensaje() }}
        </div>
      }
    </section>
  `,
})
export class CatalogoListComponent implements OnInit {
  private catalosoService = inject(CatalogoService);
  private reservaService = inject(ReservaService);
  private auth = inject(AuthService);
  private router = inject(Router);

  libros = signal<Libro[]>([]);
  categorias = signal<Categoria[]>([]);
  cargando = signal(false);
  total = signal(0);
  pagina = signal(1);
  hayMas = signal(false);
  mensaje = signal('');
  error = signal(false);

  busqueda = '';
  categoriaSeleccionada: number | null = null;

  ngOnInit(): void {
    this.cargarCategorias();
    this.cargarLibros();
  }

  cargarCategorias(): void {
    this.catalosoService.getCategorias().subscribe({
      next: (res) => this.categorias.set(res.results),
    });
  }

  cargarLibros(): void {
    this.cargando.set(true);
    this.catalosoService.getLibros({
      busqueda: this.busqueda || undefined,
      categoria: this.categoriaSeleccionada ?? undefined,
      pagina: this.pagina(),
    }).subscribe({
      next: (res) => {
        this.libros.set(res.results);
        this.total.set(res.count);
        this.hayMas.set(!!res.next);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false),
    });
  }

  buscar(): void {
    this.pagina.set(1);
    this.cargarLibros();
  }

  cambiarPagina(nueva: number): void {
    this.pagina.set(nueva);
    this.cargarLibros();
  }

  onReservar(libro: Libro): void {
    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/login']);
      return;
    }
    this.reservaService.crearReserva(libro.id).subscribe({
      next: () => {
        this.mensaje.set(`✅ Reserva de "${libro.titulo}" creada exitosamente.`);
        this.error.set(false);
        setTimeout(() => this.mensaje.set(''), 4000);
      },
      error: (e) => {
        const msg = e.error?.detail || e.error?.non_field_errors?.[0] || 'No se pudo crear la reserva.';
        this.mensaje.set(`❌ ${msg}`);
        this.error.set(true);
        setTimeout(() => this.mensaje.set(''), 5000);
      },
    });
  }
}""",
    "src/app/features/catalogo/pages/libro-detail/libro-detail.component.ts": """import { Component, inject, signal, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { CatalogoService } from '../../services/catalogo.service';
import { ReservaService } from '../../../reservas/services/reserva.service';
import { AuthService } from '../../../../core/services/auth.service';
import { Libro } from '../../../../models/libro.model';

@Component({
  selector: 'app-libro-detail',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (cargando()) {
      <div class="spinner"><p>Cargando...</p></div>
    } @else if (libro()) {
      <div style="display: grid; grid-template-columns: 250px 1fr; gap: 32px; max-width: 900px;">
        <div>
          <img
            [src]="libro()!.portada_url || 'https://via.placeholder.com/250x350?text=Sin+portada'"
            [alt]="libro()!.titulo"
            style="width: 100%; border-radius: 8px; box-shadow: var(--card-shadow);"
          >
        </div>
        <div>
          <h1>{{ libro()!.titulo }}</h1>
          <p style="color: #666; margin: 8px 0;">{{ libro()!.anio_publicacion }}</p>

          <p><strong>Autores:</strong> {{ libro()!.autores.map(a => a.nombre).join(', ') || 'N/D' }}</p>
          <p><strong>Categoría:</strong> {{ libro()!.categoria?.nombre || 'Sin categoría' }}</p>
          <p><strong>ISBN:</strong> {{ libro()!.isbn }}</p>

          <p style="margin: 16px 0;">
            <span class="badge" [class.badge-active]="libro()!.ejemplares_disponibles > 0" [class.badge-danger]="libro()!.ejemplares_disponibles === 0">
              {{ libro()!.ejemplares_disponibles > 0 ? libro()!.ejemplares_disponibles + ' ejemplar(es) disponible(s)' : 'Sin stock disponible' }}
            </span>
          </p>

          <h3>Sinopsis</h3>
          <p style="line-height: 1.7; margin: 8px 0;">{{ libro()!.sinopsis || 'Sin sinopsis disponible.' }}</p>

          @if (mensaje()) {
            <div class="alert" [class.alert-success]="!errorMsg()" [class.alert-error]="errorMsg()">
              {{ mensaje() }}
            </div>
          }

          @if (libro()!.ejemplares_disponibles > 0) {
            <button class="btn-primary" style="margin-top: 16px; padding: 10px 24px;" (click)="reservar()">📖 Reservar este libro</button>
          }
        </div>
      </div>
    } @else {
      <div class="alert alert-error">Libro no encontrado.</div>
    }
  `,
})
export class LibroDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private catalogoService = inject(CatalogoService);
  private reservaService = inject(ReservaService);
  private auth = inject(AuthService);
  private router = inject(Router);

  libro = signal<Libro | null>(null);
  cargando = signal(true);
  mensaje = signal('');
  errorMsg = signal(false);

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.catalogoService.getLibro(id).subscribe({
      next: (l) => { this.libro.set(l); this.cargando.set(false); },
      error: () => this.cargando.set(false),
    });
  }

  reservar(): void {
    if (!this.auth.isLoggedIn()) { this.router.navigate(['/login']); return; }
    this.reservaService.crearReserva(this.libro()!.id).subscribe({
      next: () => { this.mensaje.set('✅ Reserva creada exitosamente.'); this.errorMsg.set(false); },
      error: (e) => { this.mensaje.set('❌ ' + (e.error?.detail || 'No se pudo crear la reserva.')); this.errorMsg.set(true); },
    });
  }
}""",
    "src/app/features/auth/pages/login/login.component.ts": """import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div style="max-width: 400px; margin: 40px auto;">
      <div class="card">
        <h2 style="margin-bottom: 24px; text-align: center;">🔐 Iniciar Sesión</h2>

        @if (error()) {
          <div class="alert alert-error">{{ error() }}</div>
        }

        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label>Usuario</label>
            <input formControlName="username" placeholder="Nombre de usuario">
          </div>
          <div class="form-group">
            <label>Contraseña</label>
            <input type="password" formControlName="password" placeholder="Contraseña">
          </div>
          <button type="submit" class="btn-primary" style="width: 100%; padding: 12px;" [disabled]="cargando()">
            {{ cargando() ? 'Ingresando...' : 'Ingresar' }}
          </button>
        </form>

        <p style="text-align: center; margin-top: 16px;">
          ¿No tienes cuenta? <a routerLink="/registro">Regístrate aquí</a>
        </p>
      </div>
    </div>
  `,
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);

  error = signal('');
  cargando = signal(false);

  form = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required],
  });

  onSubmit(): void {
    if (this.form.invalid) return;
    this.cargando.set(true);
    this.error.set('');

    this.auth.login(this.form.value as { username: string; password: string }).subscribe({
      next: () => { this.router.navigate(['/']); },
      error: () => {
        this.error.set('Credenciales incorrectas. Verifica tu usuario y contraseña.');
        this.cargando.set(false);
      },
    });
  }
}""",
    "src/app/features/auth/pages/register/register.component.ts": """import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div style="max-width: 500px; margin: 40px auto;">
      <div class="card">
        <h2 style="margin-bottom: 24px; text-align: center;">📝 Crear Cuenta</h2>

        @if (error()) { <div class="alert alert-error">{{ error() }}</div> }
        @if (exito()) { <div class="alert alert-success">{{ exito() }}</div> }

        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div class="form-group">
              <label>Nombre</label>
              <input formControlName="first_name" placeholder="Nombre">
            </div>
            <div class="form-group">
              <label>Apellido</label>
              <input formControlName="last_name" placeholder="Apellido">
            </div>
          </div>
          <div class="form-group">
            <label>Nombre de usuario</label>
            <input formControlName="username" placeholder="usuario123">
          </div>
          <div class="form-group">
            <label>Correo electrónico</label>
            <input type="email" formControlName="email" placeholder="correo@ejemplo.com">
          </div>
          <div class="form-group">
            <label>Teléfono (opcional)</label>
            <input formControlName="telefono" placeholder="+56912345678">
          </div>
          <div class="form-group">
            <label>Contraseña</label>
            <input type="password" formControlName="password" placeholder="Mínimo 8 caracteres">
          </div>
          <button type="submit" class="btn-primary" style="width: 100%; padding: 12px;" [disabled]="cargando()">
            {{ cargando() ? 'Registrando...' : 'Registrarme' }}
          </button>
        </form>

        <p style="text-align: center; margin-top: 16px;">
          ¿Ya tienes cuenta? <a routerLink="/login">Inicia sesión</a>
        </p>
      </div>
    </div>
  `,
})
export class RegisterComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);

  error = signal('');
  exito = signal('');
  cargando = signal(false);

  form = this.fb.group({
    first_name: ['', Validators.required],
    last_name: ['', Validators.required],
    username: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    telefono: [''],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  onSubmit(): void {
    if (this.form.invalid) return;
    this.cargando.set(true);
    this.error.set('');
    this.auth.registro(this.form.value as any).subscribe({
      next: () => {
        this.exito.set('¡Cuenta creada exitosamente! Redirigiendo al login...');
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: (e) => {
        const msgs = Object.values(e.error || {}).flat().join(' ');
        this.error.set(msgs || 'Error al crear la cuenta.');
        this.cargando.set(false);
      },
    });
  }
}""",
    "src/app/features/reservas/services/reserva.service.ts": """import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reserva } from '../../../models/reserva.model';
import { PaginatedResponse } from '../../../models/libro.model';

const API = 'http://localhost:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class ReservaService {
  private http = inject(HttpClient);

  getMisReservas(): Observable<PaginatedResponse<Reserva>> {
    return this.http.get<PaginatedResponse<Reserva>>(`${API}/reservas/mis-reservas/`);
  }

  getTodasReservas(): Observable<PaginatedResponse<Reserva>> {
    return this.http.get<PaginatedResponse<Reserva>>(`${API}/reservas/`);
  }

  crearReserva(libroId: number): Observable<Reserva> {
    return this.http.post<Reserva>(`${API}/reservas/`, { libro: libroId });
  }

  cancelarReserva(id: number): Observable<Reserva> {
    return this.http.patch<Reserva>(`${API}/reservas/${id}/cancelar/`, {});
  }
}""",
    "src/app/features/reservas/pages/mis-reservas/mis-reservas.component.ts": """import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReservaService } from '../../services/reserva.service';
import { Reserva } from '../../../../models/reserva.model';

@Component({
  selector: 'app-mis-reservas',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2 style="margin-bottom: 20px;">📋 Mis Reservas</h2>

    @if (cargando()) {
      <div class="spinner"><p>Cargando reservas...</p></div>
    } @else if (reservas().length === 0) {
      <div class="alert alert-warning">No tienes reservas activas.</div>
    } @else {
      <div class="card">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Libro</th>
              <th>Fecha reserva</th>
              <th>Expira</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            @for (r of reservas(); track r.id) {
              <tr>
                <td>{{ r.id }}</td>
                <td>{{ r.libro_titulo || 'Libro #' + r.libro }}</td>
                <td>{{ r.fecha_reserva | date:'dd/MM/yyyy HH:mm' }}</td>
                <td>{{ r.fecha_expiracion | date:'dd/MM/yyyy HH:mm' }}</td>
                <td>
                  <span class="badge" [ngClass]="badgeClass(r.estado)">{{ r.estado }}</span>
                </td>
                <td>
                  @if (r.estado === 'PENDIENTE') {
                    <button class="btn-danger" style="padding: 4px 10px; font-size: 12px;" (click)="cancelar(r.id)">Cancelar</button>
                  }
                </td>
              </tr>
            }
          </tbody>
        </table>
      </div>
    }

    @if (mensaje()) {
      <div class="alert" [class.alert-success]="!errorMsg()" [class.alert-error]="errorMsg()" style="margin-top: 12px;">
        {{ mensaje() }}
      </div>
    }
  `,
})
export class MisReservasComponent implements OnInit {
  private reservaService = inject(ReservaService);

  reservas = signal<Reserva[]>([]);
  cargando = signal(true);
  mensaje = signal('');
  errorMsg = signal(false);

  ngOnInit(): void {
    this.cargarReservas();
  }

  cargarReservas(): void {
    this.cargando.set(true);
    this.reservaService.getMisReservas().subscribe({
      next: (res) => { this.reservas.set(res.results); this.cargando.set(false); },
      error: () => this.cargando.set(false),
    });
  }

  cancelar(id: number): void {
    this.reservaService.cancelarReserva(id).subscribe({
      next: () => {
        this.mensaje.set('Reserva cancelada.');
        this.errorMsg.set(false);
        this.cargarReservas();
      },
      error: () => { this.mensaje.set('No se pudo cancelar.'); this.errorMsg.set(true); },
    });
  }

  badgeClass(estado: string): string {
    const map: Record<string, string> = {
      PENDIENTE: 'badge-pending', ASIGNADA: 'badge-active',
      CANCELADA: 'badge-danger', EXPIRADA: 'badge-danger', COMPLETADA: 'badge-active',
    };
    return map[estado] ?? '';
  }
}""",
    "src/app/features/prestamos/services/prestamo.service.ts": """import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Prestamo } from '../../../models/prestamo.model';
import { PaginatedResponse } from '../../../models/libro.model';

const API = 'http://localhost:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class PrestamoService {
  private http = inject(HttpClient);

  getMisPrestamos(): Observable<PaginatedResponse<Prestamo>> {
    return this.http.get<PaginatedResponse<Prestamo>>(`${API}/prestamos/mis-prestamos/`);
  }

  getTodosPrestamos(): Observable<PaginatedResponse<Prestamo>> {
    return this.http.get<PaginatedResponse<Prestamo>>(`${API}/prestamos/`);
  }

  crearPrestamo(data: { usuario: number; ejemplar: number }): Observable<Prestamo> {
    return this.http.post<Prestamo>(`${API}/prestamos/`, data);
  }

  registrarDevolucion(id: number, observaciones?: string): Observable<Prestamo> {
    return this.http.post<Prestamo>(`${API}/prestamos/${id}/devolucion/`, { observaciones });
  }

  renovarPrestamo(id: number): Observable<Prestamo> {
    return this.http.post<Prestamo>(`${API}/prestamos/${id}/renovar/`, {});
  }
}""",
    "src/app/features/prestamos/pages/mis-prestamos/mis-prestamos.component.ts": """import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrestamoService } from '../../services/prestamo.service';
import { Prestamo } from '../../../../models/prestamo.model';

@Component({
  selector: 'app-mis-prestamos',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2 style="margin-bottom: 20px;">📦 Mis Préstamos</h2>

    @if (cargando()) {
      <div class="spinner"><p>Cargando préstamos...</p></div>
    } @else if (prestamos().length === 0) {
      <div class="alert alert-warning">No tienes préstamos activos.</div>
    } @else {
      <div class="card">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Libro</th>
              <th>Ejemplar</th>
              <th>Fecha préstamo</th>
              <th>Devolver antes de</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            @for (p of prestamos(); track p.id) {
              <tr>
                <td>{{ p.id }}</td>
                <td>{{ p.libro_titulo || 'Libro' }}</td>
                <td>{{ p.ejemplar_codigo || '#' + p.ejemplar }}</td>
                <td>{{ p.fecha_prestamo | date:'dd/MM/yyyy' }}</td>
                <td>{{ p.fecha_limite_devolucion | date:'dd/MM/yyyy' }}</td>
                <td><span class="badge" [ngClass]="badgeClass(p.estado)">{{ p.estado }}</span></td>
                <td>
                  @if (p.estado === 'ACTIVO') {
                    <button class="btn-secondary" style="padding: 4px 10px; font-size: 12px;" (click)="renovar(p.id)">Renovar</button>
                  }
                </td>
              </tr>
            }
          </tbody>
        </table>
      </div>
    }

    @if (mensaje()) {
      <div class="alert" [class.alert-success]="!errorMsg()" [class.alert-error]="errorMsg()" style="margin-top: 12px;">
        {{ mensaje() }}
      </div>
    }
  `,
})
export class MisPrestamosComponent implements OnInit {
  private prestamoService = inject(PrestamoService);

  prestamos = signal<Prestamo[]>([]);
  cargando = signal(true);
  mensaje = signal('');
  errorMsg = signal(false);

  ngOnInit(): void { this.cargar(); }

  cargar(): void {
    this.cargando.set(true);
    this.prestamoService.getMisPrestamos().subscribe({
      next: (res) => { this.prestamos.set(res.results); this.cargando.set(false); },
      error: () => this.cargando.set(false),
    });
  }

  renovar(id: number): void {
    this.prestamoService.renovarPrestamo(id).subscribe({
      next: () => { this.mensaje.set('Préstamo renovado.'); this.errorMsg.set(false); this.cargar(); },
      error: (e) => { this.mensaje.set(e.error?.detail || 'No se pudo renovar.'); this.errorMsg.set(true); },
    });
  }

  badgeClass(estado: string): string {
    const map: Record<string, string> = {
      ACTIVO: 'badge-active',
      DEVUELTO: 'badge-success',
      CON_MORA: 'badge-danger',
      EXTRAVIADO: 'badge-danger'
    };
    return map[estado] || 'badge-pending';
  }
}"""
}

for path_suffix, content in files.items():
    full_path = os.path.join(base_dir, path_suffix.replace('/', os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
