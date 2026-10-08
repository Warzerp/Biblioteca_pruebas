import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../services/admin.service';
import { Ejemplar, EstadoEjemplar } from '../../../../models/ejemplar.model';

const ESTADOS: EstadoEjemplar[] = [
  'DISPONIBLE', 'PRESTADO', 'RESERVADO', 'MANTENIMIENTO', 'EXTRAVIADO',
];

@Component({
  selector: 'app-crud-ejemplares',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h2 style="margin-bottom: 20px;">Gestión de Ejemplares</h2>

    <!-- Formulario para crear ejemplar -->
    <div class="card" style="margin-bottom: 24px;">
      <h3 style="margin-bottom: 12px;">{{ editando() ? 'Editar Ejemplar' : 'Agregar Ejemplar' }}</h3>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
        <div class="form-group">
          <label>ID del Libro *</label>
          <input type="number" [(ngModel)]="form.libro" placeholder="ID del libro">
        </div>
        <div class="form-group">
          <label>Código de inventario *</label>
          <input [(ngModel)]="form.codigo_inventario" placeholder="EJ-001">
        </div>
        <div class="form-group">
          <label>Ubicación en estante</label>
          <input [(ngModel)]="form.ubicacion_estante" placeholder="Estante A-3">
        </div>
        <div class="form-group">
          <label>Estado</label>
          <select [(ngModel)]="form.estado">
            @for (e of estados; track e) {
              <option [value]="e">{{ e }}</option>
            }
          </select>
        </div>
      </div>
      <div style="display: flex; gap: 8px; margin-top: 8px;">
        <button class="btn-primary" (click)="guardar()">{{ editando() ? 'Actualizar' : 'Crear Ejemplar' }}</button>
        @if (editando()) {
          <button (click)="cancelarEdicion()" style="background: #e0e0e0;">Cancelar</button>
        }
      </div>
    </div>

    @if (mensaje()) {
      <div class="alert" [class.alert-success]="!errorMsg()" [class.alert-error]="errorMsg()" style="margin-bottom: 16px;">
        {{ mensaje() }}
      </div>
    }

    <!-- Tabla de ejemplares -->
    <div class="card">
      <h3 style="margin-bottom: 12px;">Inventario de Ejemplares</h3>
      @if (cargando()) {
        <div class="spinner"><p>Cargando...</p></div>
      } @else if (ejemplares().length === 0) {
        <div class="alert alert-warning">No hay ejemplares registrados.</div>
      } @else {
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Código</th>
              <th>Libro ID</th>
              <th>Ubicación</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            @for (ej of ejemplares(); track ej.id) {
              <tr>
                <td>{{ ej.id }}</td>
                <td>{{ ej.codigo_inventario }}</td>
                <td>{{ ej.libro }}</td>
                <td>{{ ej.ubicacion_estante || '-' }}</td>
                <td>
                  <span class="badge" [ngClass]="badgeClass(ej.estado)">{{ ej.estado }}</span>
                </td>
                <td>
                  <button class="btn-secondary" style="padding: 4px 10px; font-size: 12px; margin-right: 4px;" (click)="editar(ej)">Editar</button>
                </td>
              </tr>
            }
          </tbody>
        </table>
      }
    </div>
  `,
})
export class CrudEjemplaresComponent implements OnInit {
  private adminService = inject(AdminService);

  ejemplares = signal<Ejemplar[]>([]);
  cargando = signal(true);
  editando = signal<number | null>(null);
  mensaje = signal('');
  errorMsg = signal(false);

  estados = ESTADOS;

  form: Partial<Ejemplar>= {
    libro: undefined,
    codigo_inventario: '',
    ubicacion_estante: '',
    estado: 'DISPONIBLE',
  };

  ngOnInit(): void {
    this.cargar();
  }

  cargar(): void {
    this.cargando.set(true);
    this.adminService.getEjemplares().subscribe({
      next: (res) =>{ this.ejemplares.set(res.results); this.cargando.set(false); },
      error: () =>this.cargando.set(false),
    });
  }

  guardar(): void {
    const obs = this.editando()
      ? this.adminService.actualizarEjemplar(this.editando()!, this.form)
      : this.adminService.crearEjemplar(this.form);

    obs.subscribe({
      next: () =>{
        this.mensaje.set(this.editando() ? 'Ejemplar actualizado.' : 'Ejemplar creado.');
        this.errorMsg.set(false);
        this.cancelarEdicion();
        this.cargar();
      },
      error: (e) =>{
        const msgs = Object.values(e.error || {}).flat().join(' ');
        this.mensaje.set(msgs || 'Error al guardar.');
        this.errorMsg.set(true);
      },
    });
  }

  editar(ej: Ejemplar): void {
    this.editando.set(ej.id);
    this.form = {
      libro: ej.libro,
      codigo_inventario: ej.codigo_inventario,
      ubicacion_estante: ej.ubicacion_estante,
      estado: ej.estado,
    };
  }

  cancelarEdicion(): void {
    this.editando.set(null);
    this.form = { libro: undefined, codigo_inventario: '', ubicacion_estante: '', estado: 'DISPONIBLE' };
  }

  badgeClass(estado: string): string {
    const map: Record<string, string>= {
      DISPONIBLE: 'badge-active',
      PRESTADO: 'badge-pending',
      RESERVADO: 'badge-pending',
      MANTENIMIENTO: 'badge-danger',
      EXTRAVIADO: 'badge-danger',
    };
    return map[estado] ?? '';
  }
}
