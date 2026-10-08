import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrestamoService } from '../../services/prestamo.service';
import { Prestamo } from '../../../../models/prestamo.model';

@Component({
  selector: 'app-mis-prestamos',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2 style="margin-bottom: 20px;">� Mis Préstamos</h2>

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
      next: (res) =>{ this.prestamos.set(res.results); this.cargando.set(false); },
      error: () =>this.cargando.set(false),
    });
  }

  renovar(id: number): void {
    this.prestamoService.renovarPrestamo(id).subscribe({
      next: () =>{ this.mensaje.set('Préstamo renovado.'); this.errorMsg.set(false); this.cargar(); },
      error: (e) =>{ this.mensaje.set(e.error?.detail || 'No se pudo renovar.'); this.errorMsg.set(true); },
    });
  }

  badgeClass(estado: string): string {
    const map: Record<string, string>= {
      ACTIVO: 'badge-active',
      DEVUELTO: 'badge-success',
      CON_MORA: 'badge-danger',
      EXTRAVIADO: 'badge-danger'
    };
    return map[estado] || 'badge-pending';
  }
}