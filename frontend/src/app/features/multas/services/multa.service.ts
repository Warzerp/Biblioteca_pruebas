import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Multa } from '../../../models/multa.model';
import { PaginatedResponse } from '../../../models/libro.model';

const API = 'http://localhost:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class MultaService {
  private http = inject(HttpClient);

  getMisMultas(): Observable<PaginatedResponse<Multa>>{
    return this.http.get<PaginatedResponse<Multa>>(`${API}/multas/mis-multas/`);
  }

  getTodasMultas(): Observable<PaginatedResponse<Multa>>{
    return this.http.get<PaginatedResponse<Multa>>(`${API}/multas/`);
  }

  pagarMulta(id: number, condonada = false): Observable<Multa>{
    return this.http.post<Multa>(`${API}/multas/${id}/pagar/`, { condonada });
  }
}

