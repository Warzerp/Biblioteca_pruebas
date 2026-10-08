import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReservaService } from '../../services/reserva.service';
import { Reserva } from '../../../../models/reserva.model';

@Component({
  selector: 'app-mis-reservas',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2 style="margin-bottom: 20px;">� Mis Reservas</h2>

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
      next: (res) =>{ this.reservas.set(res.results); this.cargando.set(false); },
      error: () =>this.cargando.set(false),
    });
  }

  cancelar(id: number): void {
    this.reservaService.cancelarReserva(id).subscribe({
      next: () =>{
        this.mensaje.set('Reserva cancelada.');
        this.errorMsg.set(false);
        this.cargarReservas();
      },
      error: () =>{ this.mensaje.set('No se pudo cancelar.'); this.errorMsg.set(true); },
    });
  }

  badgeClass(estado: string): string {
    const map: Record<string, string>= {
      PENDIENTE: 'badge-pending', ASIGNADA: 'badge-active',
      CANCELADA: 'badge-danger', EXPIRADA: 'badge-danger', COMPLETADA: 'badge-active',
    };
    return map[estado] ?? '';
  }
}