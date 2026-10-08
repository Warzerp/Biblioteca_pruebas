import { Component, inject, signal, OnInit } from '@angular/core';
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

          <p><strong>Autores:</strong>{{ getAutoresString() }}</p>
          <p><strong>Categoría:</strong>{{ libro()!.categoria_detalle?.nombre || 'Sin categoría' }}</p>
          <p><strong>ISBN:</strong>{{ libro()!.isbn }}</p>

          <p style="margin: 16px 0;">
            <span class="badge" [class.badge-active]="libro()!.ejemplares_disponibles >0" [class.badge-danger]="libro()!.ejemplares_disponibles === 0">
              {{ libro()!.ejemplares_disponibles >0 ? libro()!.ejemplares_disponibles + ' ejemplar(es) disponible(s)' : 'Sin stock disponible' }}
            </span>
          </p>

          <h3>Sinopsis</h3>
          <p style="line-height: 1.7; margin: 8px 0;">{{ libro()!.sinopsis || 'Sin sinopsis disponible.' }}</p>

          @if (mensaje()) {
            <div class="alert" [class.alert-success]="!errorMsg()" [class.alert-error]="errorMsg()">
              {{ mensaje() }}
            </div>
          }

          @if (libro()!.ejemplares_disponibles >0) {
            <button class="btn-primary" style="margin-top: 16px; padding: 10px 24px;" (click)="reservar()">Reservar este libro</button>
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

  getAutoresString(): string {
    const l = this.libro();
    if (!l || !l.autores || l.autores.length === 0) return 'N/D';
    return l.autores.map(a =>a.nombre).join(', ');
  }

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.catalogoService.getLibro(id).subscribe({
      next: (l) =>{ this.libro.set(l); this.cargando.set(false); },
      error: () =>this.cargando.set(false),
    });
  }

  reservar(): void {
    if (!this.auth.isLoggedIn()) { this.router.navigate(['/login']); return; }
    this.reservaService.crearReserva(this.libro()!.id).subscribe({
      next: () =>{ this.mensaje.set(' Reserva creada exitosamente.'); this.errorMsg.set(false); },
      error: (e) =>{ this.mensaje.set(' ' + (e.error?.detail || 'No se pudo crear la reserva.')); this.errorMsg.set(true); },
    });
  }
}