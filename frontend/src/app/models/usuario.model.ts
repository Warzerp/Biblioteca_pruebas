export interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  telefono: string;
  rol: 'LECTOR' | 'BIBLIOTECARIO' | 'ADMIN';
  is_active: boolean;
  date_joined: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RegistroRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  telefono?: string;
}