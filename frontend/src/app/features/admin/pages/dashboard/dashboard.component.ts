import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CatalogoService } from '../../../catalogo/services/catalogo.service';
import { PrestamoService } from '../../../prestamos/services/prestamo.service';
import { MultaService } from '../../../multas/services/multa.service';
import { AdminService } from '../../services/admin.service';
import { ReservaService } from '../../../reservas/services/reserva.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <h2 style="margin-bottom: 8px;">Panel de administración</h2>
    <p style="color: var(--text-muted); margin-bottom: 24px;">Resumen operativo de la biblioteca.</p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 28px;">
      @for (card of tarjetas(); track card.label) {
        <a [routerLink]="card.link" class="card" style="text-decoration: none; color: inherit;">
          <p style="font-size: 13px; color: var(--text-muted);">{{ card.label }}</p>
          <p style="font-size: 28px; font-weight: 700; margin-top: 8px;">{{ card.valor }}</p>
        </a>
      }
    </div>

    <div style="display: flex; gap: 12px; flex-wrap: wrap;">
      <a routerLink="/admin/libros" class="btn-primary">Gestionar libros</a>
      <a routerLink="/admin/ejemplares" class="btn-secondary">Gestionar ejemplares</a>
      <a routerLink="/admin/prestamos" class="btn-secondary">Gestionar préstamos</a>
    </div>
  `,
})
export class DashboardComponent implements OnInit {
  private catalogo = inject(CatalogoService);
  private prestamos = inject(PrestamoService);
  private multas = inject(MultaService);
  private admin = inject(AdminService);
  private reservas = inject(ReservaService);

  tarjetas = signal([
    { label: 'Libros', valor: '—', link: '/admin/libros' },
    { label: 'Ejemplares', valor: '—', link: '/admin/ejemplares' },
    { label: 'Préstamos', valor: '—', link: '/admin/prestamos' },
    { label: 'Reservas', valor: '—', link: '/admin/prestamos' },
    { label: 'Multas', valor: '—', link: '/admin/prestamos' },
    { label: 'Usuarios', valor: '—', link: '/admin/dashboard' },
  ]);

  ngOnInit(): void {
    this.catalogo.getLibros({ pagina: 1 }).subscribe(r => this.patch('Libros', r.count));
    this.admin.getEjemplares().subscribe(r => this.patch('Ejemplares', r.count));
    this.prestamos.getTodosPrestamos().subscribe(r => this.patch('Préstamos', r.count));
    this.reservas.getTodasReservas().subscribe(r => this.patch('Reservas', r.count));
    this.multas.getTodasMultas().subscribe(r => this.patch('Multas', r.count));
    this.admin.getUsuarios().subscribe(r => this.patch('Usuarios', r.count));
  }

  private patch(label: string, valor: number): void {
    this.tarjetas.update(cards => cards.map(c => c.label === label ? { ...c, valor: String(valor) } : c));
  }
}
