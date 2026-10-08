import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CatalogoService } from '../../../catalogo/services/catalogo.service';
import { Autor, Categoria, Libro } from '../../../../models/libro.model';

@Component({
  selector: 'app-crud-libros',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h2 style="margin-bottom: 20px;">Gestión de libros</h2>

    <div class="card" style="margin-bottom: 24px;">
      <h3 style="margin-bottom: 12px;">{{ editando() ? 'Editar libro' : 'Nuevo libro' }}</h3>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div class="form-group">
          <label>ISBN *</label>
          <input [(ngModel)]="form.isbn" placeholder="978-...">
        </div>
        <div class="form-group">
          <label>Título *</label>
          <input [(ngModel)]="form.titulo" placeholder="Título">
        </div>
        <div class="form-group">
          <label>Categoría</label>
          <select [(ngModel)]="form.categoria">
            <option [ngValue]="null">Sin categoría</option>
            @for (cat of categorias(); track cat.id) {
              <option [ngValue]="cat.id">{{ cat.nombre }}</option>
            }
          </select>
        </div>
        <div class="form-group">
          <label>Año</label>
          <input type="number" [(ngModel)]="form.anio_publicacion">
        </div>
        <div class="form-group" style="grid-column: 1 / -1;">
          <label>URL de portada</label>
          <input [(ngModel)]="form.portada_url" placeholder="https://...">
        </div>
        <div class="form-group" style="grid-column: 1 / -1;">
          <label>Sinopsis</label>
          <textarea [(ngModel)]="form.sinopsis" rows="3"></textarea>
        </div>
        <div class="form-group" style="grid-column: 1 / -1;">
          <label>Autores</label>
          <select multiple [(ngModel)]="autoresIds" style="min-height: 90px;">
            @for (a of autores(); track a.id) {
              <option [ngValue]="a.id">{{ a.nombre }}</option>
            }
          </select>
        </div>
      </div>
      <div style="display: flex; gap: 8px; margin-top: 8px;">
        <button class="btn-primary" (click)="guardar()">{{ editando() ? 'Actualizar' : 'Crear libro' }}</button>
        @if (editando()) {
          <button (click)="cancelar()" style="background: #e0e0e0;">Cancelar</button>
        }
      </div>
    </div>

    @if (mensaje()) {
      <div class="alert" [class.alert-success]="!errorMsg()" [class.alert-error]="errorMsg()" style="margin-bottom: 16px;">
        {{ mensaje() }}
      </div>
    }

    <div class="card">
      @if (cargando()) {
        <div class="spinner"><p>Cargando...</p></div>
      } @else {
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Título</th>
              <th>ISBN</th>
              <th>Categoría</th>
              <th>Stock</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            @for (libro of libros(); track libro.id) {
              <tr>
                <td>{{ libro.id }}</td>
                <td>{{ libro.titulo }}</td>
                <td>{{ libro.isbn }}</td>
                <td>{{ libro.categoria_detalle?.nombre || '—' }}</td>
                <td>{{ libro.ejemplares_disponibles }}</td>
                <td>
                  <button class="btn-secondary" style="padding: 4px 10px; font-size: 12px; margin-right: 4px;" (click)="editar(libro)">Editar</button>
                  <button class="btn-danger" style="padding: 4px 10px; font-size: 12px;" (click)="eliminar(libro.id)">Desactivar</button>
                </td>
              </tr>
            }
          </tbody>
        </table>
      }
    </div>
  `,
})
export class CrudLibrosComponent implements OnInit {
  private catalogo = inject(CatalogoService);

  libros = signal<Libro[]>([]);
  categorias = signal<Categoria[]>([]);
  autores = signal<Autor[]>([]);
  cargando = signal(true);
  editando = signal<number | null>(null);
  mensaje = signal('');
  errorMsg = signal(false);
  autoresIds: number[] = [];

  form: Partial<Libro> = this.vacio();

  ngOnInit(): void {
    this.catalogo.getCategorias().subscribe(r => this.categorias.set(r.results));
    this.catalogo.getAutores().subscribe(r => this.autores.set(r.results));
    this.cargar();
  }

  cargar(): void {
    this.cargando.set(true);
    this.catalogo.getLibros({ pagina: 1 }).subscribe({
      next: (res) => { this.libros.set(res.results); this.cargando.set(false); },
      error: () => this.cargando.set(false),
    });
  }

  guardar(): void {
    const payload: any = { ...this.form, autores_ids: this.autoresIds };
    const obs = this.editando()
      ? this.catalogo.actualizarLibro(this.editando()!, payload)
      : this.catalogo.crearLibro(payload);

    obs.subscribe({
      next: () => {
        this.mensaje.set(this.editando() ? 'Libro actualizado.' : 'Libro creado.');
        this.errorMsg.set(false);
        this.cancelar();
        this.cargar();
      },
      error: (e) => {
        this.mensaje.set(Object.values(e.error || {}).flat().join(' ') || 'Error al guardar.');
        this.errorMsg.set(true);
      },
    });
  }

  editar(libro: Libro): void {
    this.editando.set(libro.id);
    this.form = {
      isbn: libro.isbn,
      titulo: libro.titulo,
      sinopsis: libro.sinopsis,
      categoria: libro.categoria,
      anio_publicacion: libro.anio_publicacion,
      portada_url: libro.portada_url,
    };
    this.autoresIds = (libro.autores || []).map(a => a.id);
  }

  eliminar(id: number): void {
    this.catalogo.eliminarLibro(id).subscribe({
      next: () => { this.mensaje.set('Libro desactivado.'); this.errorMsg.set(false); this.cargar(); },
      error: () => { this.mensaje.set('No se pudo desactivar.'); this.errorMsg.set(true); },
    });
  }

  cancelar(): void {
    this.editando.set(null);
    this.form = this.vacio();
    this.autoresIds = [];
  }

  private vacio(): Partial<Libro> {
    return { isbn: '', titulo: '', sinopsis: '', categoria: null, anio_publicacion: null, portada_url: '' };
  }
}
