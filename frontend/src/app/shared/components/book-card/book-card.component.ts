import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Libro } from '../../../models/libro.model';

@Component({
  selector: 'app-book-card',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="card" style="display: flex; flex-direction: column; gap: 8px; height: 100%;">
      <img
        [src]="libro.portada_url || 'https://via.placeholder.com/150x200?text=Sin+portada'"
        [alt]="libro.titulo"
        style="width: 100%; height: 200px; object-fit: cover; border-radius: 4px;"
      >
      <h3 style="font-size: 14px; line-height: 1.3;">{{ libro.titulo }}</h3>
      <p style="font-size: 12px; color: #666;">
        {{ libro.autores.length ? libro.autores[0].nombre : 'Autor desconocido' }}
      </p>
      <p style="font-size: 12px;">
        <span
          class="badge"
          [class.badge-active]="libro.ejemplares_disponibles >0"
          [class.badge-danger]="libro.ejemplares_disponibles === 0"
        >
          {{ libro.ejemplares_disponibles >0 ? libro.ejemplares_disponibles + ' disponibles' : 'Sin stock' }}
        </span>
      </p>
      <div style="margin-top: auto; display: flex; gap: 8px;">
        <a [routerLink]="['/libro', libro.id]" class="btn-primary" style="display: block; text-align: center; padding: 6px 12px; border-radius: 4px; font-size: 13px;">Ver detalle</a>
        @if (libro.ejemplares_disponibles >0) {
          <button class="btn-secondary" style="font-size: 13px; padding: 6px 12px;" (click)="reservar.emit(libro)">Reservar</button>
        }
      </div>
    </div>
  `,
})
export class BookCardComponent {
  @Input({ required: true }) libro!: Libro;
  @Output() reservar = new EventEmitter<Libro>();
}