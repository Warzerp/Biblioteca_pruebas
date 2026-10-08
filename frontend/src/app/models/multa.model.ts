export type EstadoMulta = 'PENDIENTE' | 'PAGADA' | 'CONDONADA';

export interface Multa {
  id: number;
  usuario: number;
  usuario_username?: string;
  prestamo: number;
  libro_titulo?: string;
  monto: string;
  motivo: string;
  estado: EstadoMulta;
  fecha_generacion: string;
  fecha_pago: string | null;
}