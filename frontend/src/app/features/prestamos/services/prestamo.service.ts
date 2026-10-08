import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Prestamo } from '../../../models/prestamo.model';
import { PaginatedResponse } from '../../../models/libro.model';

const API = 'http://localhost:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class PrestamoService {
  private http = inject(HttpClient);

  getMisPrestamos(): Observable<PaginatedResponse<Prestamo>>{
    return this.http.get<PaginatedResponse<Prestamo>>(`${API}/prestamos/mis-prestamos/`);
  }

  getTodosPrestamos(): Observable<PaginatedResponse<Prestamo>>{
    return this.http.get<PaginatedResponse<Prestamo>>(`${API}/prestamos/?page_size=100`);
  }

  crearPrestamo(data: { usuario: number; ejemplar: number }): Observable<Prestamo>{
    return this.http.post<Prestamo>(`${API}/prestamos/`, data);
  }

  registrarDevolucion(id: number, observaciones?: string): Observable<Prestamo>{
    return this.http.post<Prestamo>(`${API}/prestamos/${id}/devolucion/`, { observaciones });
  }

  renovarPrestamo(id: number): Observable<Prestamo>{
    return this.http.post<Prestamo>(`${API}/prestamos/${id}/renovar/`, {});
  }
}