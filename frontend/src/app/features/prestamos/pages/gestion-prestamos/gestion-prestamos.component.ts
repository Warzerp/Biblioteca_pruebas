import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PrestamoService } from '../../services/prestamo.service';
import { AdminService } from '../../../admin/services/admin.service';
import { Prestamo } from '../../../../models/prestamo.model';
import { Usuario } from '../../../../models/usuario.model';
import { Ejemplar } from '../../../../models/ejemplar.model';

@Component({
  selector: 'app-gestion-prestamos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h2 style="margin-bottom: 20px;">Gestión de préstamos</h2>

    <div class="card" style="margin-bottom: 24px;">
      <h3 style="margin-bottom: 12px;">Registrar préstamo</h3>
      <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 12px; align-items: end;">
        <div class="form-group">
          <label>Usuario</label>
          <select [(ngModel)]="usuarioId">
            <option [ngValue]="null">Seleccionar</option>
            @for (u of usuarios(); track u.id) {
              <option [ngValue]="u.id">{{ u.username }} ({{ u.rol }})</option>
            }
          </select>
        </div>
        <div class="form-group">
          <label>Ejemplar disponible</label>
          <select [(ngModel)]="ejemplarId">
            <option [ngValue]="null">Seleccionar</option>
            @for (e of ejemplaresDisponibles(); track e.id) {
              <option [ngValue]="e.id">{{ e.codigo_inventario }} — {{ e.libro_titulo }}</option>
            }
          </select>
        </div>
        <button class="btn-primary" (click)="crear()">Prestar</button>
      </div>
    </div>

    @if (mensaje()) {
      <div class="alert" [class.alert-success]="!errorMsg()" [class.alert-error]="errorMsg()" style="margin-bottom: 16px;">
        {{ mensaje() }}
      </div>
    }

    <div class="card">
      @if (cargando()) {
        <div class="spinner"><p>Cargando préstamos...</p></div>
      } @else {
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Usuario</th>
              <th>Libro</th>
              <th>Ejemplar</th>
              <th>Límite</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            @for (p of prestamos(); track p.id) {
              <tr>
                <td>{{ p.id }}</td>
                <td>{{ p.usuario_username }}</td>
                <td>{{ p.libro_titulo }}</td>
                <td>{{ p.ejemplar_codigo }}</td>
                <td>{{ p.fecha_limite_devolucion | date:'dd/MM/yyyy' }}</td>
                <td><span class="badge" [ngClass]="badgeClass(p.estado)">{{ p.estado }}</span></td>
                <td>
                  @if (p.estado === 'ACTIVO' || p.estado === 'CON_MORA') {
                    <button class="btn-secondary" style="padding: 4px 10px; font-size: 12px; margin-right: 4px;" (click)="renovar(p.id)">Renovar</button>
                    <button class="btn-primary" style="padding: 4px 10px; font-size: 12px;" (click)="devolver(p.id)">Devolver</button>
                  }
                </td>
              </tr>
            }
          </tbody>
        </table>
      }
    </div>
  `,
})
export class GestionPrestamosComponent implements OnInit {
  private prestamoService = inject(PrestamoService);
  private admin = inject(AdminService);

  prestamos = signal<Prestamo[]>([]);
  usuarios = signal<Usuario[]>([]);
  ejemplares = signal<Ejemplar[]>([]);
  cargando = signal(true);
  mensaje = signal('');
  errorMsg = signal(false);
  usuarioId: number | null = null;
  ejemplarId: number | null = null;

  ngOnInit(): void {
    this.admin.getUsuarios().subscribe(r => this.usuarios.set(r.results));
    this.cargar();
  }

  ejemplaresDisponibles(): Ejemplar[] {
    return this.ejemplares().filter(e => e.estado === 'DISPONIBLE');
  }

  cargar(): void {
    this.cargando.set(true);
    this.prestamoService.getTodosPrestamos().subscribe({
      next: (res) => { this.prestamos.set(res.results); this.cargando.set(false); },
      error: () => this.cargando.set(false),
    });
    this.admin.getEjemplares().subscribe(r => this.ejemplares.set(r.results));
  }

  crear(): void {
    if (!this.usuarioId || !this.ejemplarId) return;
    this.prestamoService.crearPrestamo({ usuario: this.usuarioId, ejemplar: this.ejemplarId }).subscribe({
      next: () => {
        this.mensaje.set('Préstamo creado.');
        this.errorMsg.set(false);
        this.usuarioId = null;
        this.ejemplarId = null;
        this.cargar();
      },
      error: (e) => {
        this.mensaje.set(e.error?.detail || 'No se pudo crear el préstamo.');
        this.errorMsg.set(true);
      },
    });
  }

  devolver(id: number): void {
    this.prestamoService.registrarDevolucion(id).subscribe({
      next: (res: any) => {
        this.mensaje.set(res.mora && res.mora !== '0.00' ? `Devuelto con mora de ${res.mora}.` : 'Devuelto.');
        this.errorMsg.set(false);
        this.cargar();
      },
      error: (e) => { this.mensaje.set(e.error?.error || 'No se pudo devolver.'); this.errorMsg.set(true); },
    });
  }

  renovar(id: number): void {
    this.prestamoService.renovarPrestamo(id).subscribe({
      next: () => { this.mensaje.set('Renovado.'); this.errorMsg.set(false); this.cargar(); },
      error: () => { this.mensaje.set('No se pudo renovar.'); this.errorMsg.set(true); },
    });
  }

  badgeClass(estado: string): string {
    const map: Record<string, string> = {
      ACTIVO: 'badge-active', DEVUELTO: 'badge-success', CON_MORA: 'badge-danger', EXTRAVIADO: 'badge-danger',
    };
    return map[estado] || 'badge-pending';
  }
}
