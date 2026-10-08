import { Component, inject, signal, OnInit } from '@angular/core';
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
      <h1 style="margin-bottom: 16px;">Catálogo de Libros</h1>

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
      next: (res) =>this.categorias.set(res.results),
    });
  }

  cargarLibros(): void {
    this.cargando.set(true);
    this.catalosoService.getLibros({
      busqueda: this.busqueda || undefined,
      categoria: this.categoriaSeleccionada ?? undefined,
      pagina: this.pagina(),
    }).subscribe({
      next: (res) =>{
        this.libros.set(res.results);
        this.total.set(res.count);
        this.hayMas.set(!!res.next);
        this.cargando.set(false);
      },
      error: () =>this.cargando.set(false),
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
      next: () =>{
        this.mensaje.set(` Reserva de "${libro.titulo}" creada exitosamente.`);
        this.error.set(false);
        setTimeout(() =>this.mensaje.set(''), 4000);
      },
      error: (e) =>{
        const msg = e.error?.detail || e.error?.non_field_errors?.[0] || 'No se pudo crear la reserva.';
        this.mensaje.set(` ${msg}`);
        this.error.set(true);
        setTimeout(() =>this.mensaje.set(''), 5000);
      },
    });
  }
}