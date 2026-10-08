import { Component, inject, signal } from '@angular/core';
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
        <h2 style="margin-bottom: 24px; text-align: center;">Crear Cuenta</h2>

        @if (error()) { <div class="alert alert-error">{{ error() }}</div>}
        @if (exito()) { <div class="alert alert-success">{{ exito() }}</div>}

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
      next: () =>{
        this.exito.set('¡Cuenta creada exitosamente! Redirigiendo al login...');
        setTimeout(() =>this.router.navigate(['/login']), 2000);
      },
      error: (e) =>{
        const msgs = Object.values(e.error || {}).flat().join(' ');
        this.error.set(msgs || 'Error al crear la cuenta.');
        this.cargando.set(false);
      },
    });
  }
}