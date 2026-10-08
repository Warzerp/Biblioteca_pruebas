import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alert-modal',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (visible) {
      <div style="position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
        <div class="card" style="max-width: 400px; width: 90%;">
          <h3 style="margin-bottom: 12px;">{{ titulo }}</h3>
          <p style="margin-bottom: 16px;">{{ mensaje }}</p>
          <div style="display: flex; gap: 8px; justify-content: flex-end;">
            @if (confirmText) {
              <button class="btn-primary" (click)="confirmar.emit(); visible = false">{{ confirmText }}</button>
            }
            <button (click)="cancelar.emit(); visible = false" style="background: #e0e0e0;">{{ cancelText }}</button>
          </div>
        </div>
      </div>
    }
  `,
})
export class AlertModalComponent {
  @Input() titulo = 'Aviso';
  @Input() mensaje = '';
  @Input() confirmText = 'Confirmar';
  @Input() cancelText = 'Cancelar';
  @Input() visible = false;
  @Output() confirmar = new EventEmitter<void>();
  @Output() cancelar = new EventEmitter<void>();
}