import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reserva } from '../../../models/reserva.model';
import { PaginatedResponse } from '../../../models/libro.model';

const API = 'http://localhost:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class ReservaService {
  private http = inject(HttpClient);

  getMisReservas(): Observable<PaginatedResponse<Reserva>>{
    return this.http.get<PaginatedResponse<Reserva>>(`${API}/reservas/mis-reservas/`);
  }

  getTodasReservas(): Observable<PaginatedResponse<Reserva>>{
    return this.http.get<PaginatedResponse<Reserva>>(`${API}/reservas/`);
  }

  crearReserva(libroId: number): Observable<Reserva>{
    return this.http.post<Reserva>(`${API}/reservas/`, { libro: libroId });
  }

  cancelarReserva(id: number): Observable<Reserva>{
    return this.http.post<Reserva>(`${API}/reservas/${id}/cancelar/`, {});
  }
}