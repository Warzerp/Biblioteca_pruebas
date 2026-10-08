import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/catalogo/pages/catalogo-list/catalogo-list.component')
        .then(m =>m.CatalogoListComponent),
  },
  {
    path: 'libro/:id',
    loadComponent: () =>
      import('./features/catalogo/pages/libro-detail/libro-detail.component')
        .then(m =>m.LibroDetailComponent),
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/pages/login/login.component')
        .then(m =>m.LoginComponent),
  },
  {
    path: 'registro',
    loadComponent: () =>
      import('./features/auth/pages/register/register.component')
        .then(m =>m.RegisterComponent),
  },
  {
    path: 'panel',
    canActivate: [authGuard],
    children: [
      {
        path: 'reservas',
        loadComponent: () =>
          import('./features/reservas/pages/mis-reservas/mis-reservas.component')
            .then(m =>m.MisReservasComponent),
      },
      {
        path: 'prestamos',
        loadComponent: () =>
          import('./features/prestamos/pages/mis-prestamos/mis-prestamos.component')
            .then(m =>m.MisPrestamosComponent),
      },
      {
        path: 'multas',
        loadComponent: () =>
          import('./features/multas/pages/mis-multas/mis-multas.component')
            .then(m =>m.MisMultasComponent),
      },
      { path: '', redirectTo: 'reservas', pathMatch: 'full' },
    ],
  },
  {
    path: 'admin',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['BIBLIOTECARIO', 'ADMIN'] },
    children: [
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/admin/pages/dashboard/dashboard.component')
            .then(m =>m.DashboardComponent),
      },
      {
        path: 'libros',
        loadComponent: () =>
          import('./features/admin/pages/crud-libros/crud-libros.component')
            .then(m =>m.CrudLibrosComponent),
      },
      {
        path: 'ejemplares',
        loadComponent: () =>
          import('./features/admin/pages/crud-ejemplares/crud-ejemplares.component')
            .then(m =>m.CrudEjemplaresComponent),
      },
      {
        path: 'prestamos',
        loadComponent: () =>
          import('./features/prestamos/pages/gestion-prestamos/gestion-prestamos.component')
            .then(m =>m.GestionPrestamosComponent),
      },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    ],
  },
  { path: '**', redirectTo: '' },
];