import type { Profesor } from './Profesor';
import type { Categoria } from './Categoria';

export interface Socio {
  id: number;
  nombre: string;
  apellido: string;
  dni: string;
  email: string;
  telefono: string;
  direccion?: string;
  fecha_nacimiento?: string;
  fecha_inscripcion: string;
  profesor_id?: number;
  profesor_nombre?: string;
  profesor?: Profesor;
  categorias?: Categoria[];
  registra_deuda?: boolean;
}
