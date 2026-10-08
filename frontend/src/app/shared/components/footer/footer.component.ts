import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  standalone: true,
  template: `
    <footer style="background: var(--primary); color: rgba(255,255,255,0.8); padding: 24px 0; margin-top: 40px;">
      <div class="container" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 24px;">
        <div>
          <strong style="color: white;">Biblioteca Digital</strong>
          <ul style="list-style: none; margin-top: 8px;">
            <li>Catálogo de libros</li>
            <li>Sistema de reservas</li>
            <li>Gestión de préstamos</li>
          </ul>
        </div>
        <div>
          <strong style="color: white;">Contacto</strong>
          <ul style="list-style: none; margin-top: 8px;">
            <li>� Calle Victoria</li>
            <li>� 0-600-libros</li>
            <li>✉️ labiblio&#64;gmail.com</li>
            <li>� 24/7</li>
          </ul>
        </div>
        <div>
          <strong style="color: white;">Tecnologías</strong>
          <ul style="list-style: none; margin-top: 8px;">
            <li>Django REST Framework</li>
            <li>Angular 17+</li>
            <li>PostgreSQL</li>
          </ul>
        </div>
      </div>
      <p style="text-align: center; margin-top: 16px; font-size: 12px;">© 2024 Biblioteca Digital. Todos los derechos reservados.</p>
    </footer>
  `,
})
export class FooterComponent {}