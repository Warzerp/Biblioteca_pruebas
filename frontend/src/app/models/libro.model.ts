export interface Autor {
  id: number;
  nombre: string;
  nacionalidad: string;
  biografia: string;
}

export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
}

export interface Libro {
  id: number;
  isbn: string;
  titulo: string;
  sinopsis: string;
  categoria: number | null;
  categoria_detalle?: Categoria | null;
  autores: Autor[];
  anio_publicacion: number | null;
  portada_url: string;
  activo: boolean;
  ejemplares_disponibles: number;
}

export interface PaginatedResponse<T>{
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}