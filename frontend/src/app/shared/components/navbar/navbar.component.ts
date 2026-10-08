import { Component, inject } from '@angular/core';
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
        <a routerLink="/" style="color: white; font-size: 1.3rem; font-weight: 700;">Biblioteca Digital</a>
        <nav style="display: flex; gap: 16px; align-items: center;">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}" style="color: rgba(255,255,255,0.85);">Catálogo</a>
          @if (auth.isLoggedIn()) {
            <a routerLink="/panel/reservas" style="color: rgba(255,255,255,0.85);">Mis Reservas</a>
            <a routerLink="/panel/prestamos" style="color: rgba(255,255,255,0.85);">Mis Préstamos</a>
            <a routerLink="/panel/multas" style="color: rgba(255,255,255,0.85);">Mis Multas</a>
            @if (auth.esAdmin()) {
              <a routerLink="/admin/dashboard" style="color: #ffe082;">Panel Admin</a>
              <a routerLink="/admin/libros" style="color: #ffe082;">Libros</a>
              <a routerLink="/admin/prestamos" style="color: #ffe082;">Préstamos</a>
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
}