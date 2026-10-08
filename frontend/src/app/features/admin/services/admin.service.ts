import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ejemplar } from '../../../models/ejemplar.model';
import { PaginatedResponse } from '../../../models/libro.model';
import { Usuario } from '../../../models/usuario.model';

const API = 'http://localhost:8000/api/v1/catalogo';
const AUTH = 'http://localhost:8000/api/v1/auth';

@Injectable({ providedIn: 'root' })
export class AdminService {
  private http = inject(HttpClient);

  getUsuarios(): Observable<PaginatedResponse<Usuario>>{
    return this.http.get<PaginatedResponse<Usuario>>(`${AUTH}/usuarios/`);
  }

  getEjemplares(): Observable<PaginatedResponse<Ejemplar>>{
    return this.http.get<PaginatedResponse<Ejemplar>>(`${API}/ejemplares/?page_size=100`);
  }

  crearEjemplar(data: Partial<Ejemplar>): Observable<Ejemplar>{
    return this.http.post<Ejemplar>(`${API}/ejemplares/`, data);
  }

  actualizarEjemplar(id: number, data: Partial<Ejemplar>): Observable<Ejemplar>{
    return this.http.patch<Ejemplar>(`${API}/ejemplares/${id}/`, data);
  }

  eliminarEjemplar(id: number): Observable<void>{
    return this.http.delete<void>(`${API}/ejemplares/${id}/`);
  }
}

