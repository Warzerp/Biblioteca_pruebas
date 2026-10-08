export type EstadoEjemplar = 'DISPONIBLE' | 'PRESTADO' | 'RESERVADO' | 'MANTENIMIENTO' | 'EXTRAVIADO';

export interface Ejemplar {
  id: number;
  libro: number;
  libro_titulo?: string;
  codigo_inventario: string;
  ubicacion_estante: string;
  estado: EstadoEjemplar;
}