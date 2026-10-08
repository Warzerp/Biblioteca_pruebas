export type EstadoReserva = 'PENDIENTE' | 'ASIGNADA' | 'CANCELADA' | 'EXPIRADA' | 'COMPLETADA';

export interface Reserva {
  id: number;
  usuario: number;
  usuario_username?: string;
  libro: number;
  libro_titulo?: string;
  fecha_reserva: string;
  fecha_expiracion: string;
  estado: EstadoReserva;
}