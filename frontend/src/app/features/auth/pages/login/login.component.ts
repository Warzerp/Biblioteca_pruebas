import { Component, inject, signal } from '@angular/core';
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
        <h2 style="margin-bottom: 24px; text-align: center;">� Iniciar Sesión</h2>

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
      next: () =>{ this.router.navigate(['/']); },
      error: () =>{
        this.error.set('Credenciales incorrectas. Verifica tu usuario y contraseña.');
        this.cargando.set(false);
      },
    });
  }
}