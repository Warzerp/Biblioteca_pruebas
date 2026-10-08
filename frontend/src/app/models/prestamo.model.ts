export type EstadoPrestamo = 'ACTIVO' | 'DEVUELTO' | 'CON_MORA' | 'EXTRAVIADO';

export interface Prestamo {
  id: number;
  usuario: number;
  usuario_username?: string;
  ejemplar: number;
  ejemplar_codigo?: string;
  libro_titulo?: string;
  fecha_prestamo: string;
  fecha_limite_devolucion: string;
  fecha_devolucion_real: string | null;
  estado: EstadoPrestamo;
  observaciones: string;
}