import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Libro, Categoria, Autor, PaginatedResponse } from '../../../models/libro.model';

const API = 'http://localhost:8000/api/v1/catalogo';

@Injectable({ providedIn: 'root' })
export class CatalogoService {
  private http = inject(HttpClient);

  getLibros(filtros: { busqueda?: string; categoria?: number; pagina?: number } = {}): Observable<PaginatedResponse<Libro>>{
    let params = new HttpParams();
    if (filtros.busqueda) params = params.set('search', filtros.busqueda);
    if (filtros.categoria) params = params.set('categoria', filtros.categoria.toString());
    if (filtros.pagina) params = params.set('page', filtros.pagina.toString());
    params = params.set('page_size', '50');
    return this.http.get<PaginatedResponse<Libro>>(`${API}/libros/`, { params });
  }

  getLibro(id: number): Observable<Libro>{
    return this.http.get<Libro>(`${API}/libros/${id}/`);
  }

  getCategorias(): Observable<PaginatedResponse<Categoria>>{
    return this.http.get<PaginatedResponse<Categoria>>(`${API}/categorias/`);
  }

  getAutores(): Observable<PaginatedResponse<Autor>>{
    return this.http.get<PaginatedResponse<Autor>>(`${API}/autores/`);
  }

  eliminarLibro(id: number): Observable<void>{
    return this.http.delete<void>(`${API}/libros/${id}/`);
  }

  crearLibro(data: Partial<Libro>): Observable<Libro>{
    return this.http.post<Libro>(`${API}/libros/`, data);
  }

  actualizarLibro(id: number, data: Partial<Libro>): Observable<Libro>{
    return this.http.patch<Libro>(`${API}/libros/${id}/`, data);
  }
}