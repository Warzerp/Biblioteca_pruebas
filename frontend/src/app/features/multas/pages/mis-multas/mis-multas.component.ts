import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MultaService } from '../../services/multa.service';
import { Multa } from '../../../../models/multa.model';

@Component({
  selector: 'app-mis-multas',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2 style="margin-bottom: 20px;">Mis multas</h2>

    @if (cargando()) {
      <div class="spinner"><p>Cargando multas...</p></div>
    } @else if (multas().length === 0) {
      <div class="alert alert-warning">No tienes multas registradas.</div>
    } @else {
      <div class="card">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Libro</th>
              <th>Monto</th>
              <th>Motivo</th>
              <th>Estado</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            @for (m of multas(); track m.id) {
              <tr>
                <td>{{ m.id }}</td>
                <td>{{ m.libro_titulo || ('Préstamo #' + m.prestamo) }}</td>
                <td>{{ m.monto | number:'1.0-0' }}</td>
                <td>{{ m.motivo }}</td>
                <td><span class="badge" [ngClass]="badgeClass(m.estado)">{{ m.estado }}</span></td>
                <td>{{ m.fecha_generacion | date:'dd/MM/yyyy' }}</td>
              </tr>
            }
          </tbody>
        </table>
      </div>
    }
  `,
})
export class MisMultasComponent implements OnInit {
  private multaService = inject(MultaService);
  multas = signal<Multa[]>([]);
  cargando = signal(true);

  ngOnInit(): void {
    this.multaService.getMisMultas().subscribe({
      next: (res) => { this.multas.set(res.results); this.cargando.set(false); },
      error: () => this.cargando.set(false),
    });
  }

  badgeClass(estado: string): string {
    const map: Record<string, string> = {
      PENDIENTE: 'badge-danger', PAGADA: 'badge-success', CONDONADA: 'badge-pending',
    };
    return map[estado] || '';
  }
}
