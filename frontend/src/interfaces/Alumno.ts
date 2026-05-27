import type { Profesor } from './Profesor'

export interface Alumno {
  id: number
  nombre: string
  apellido: string
  dni: string
  email: string
  telefono: string
  fecha_inscripcion: string
  profesor: Profesor
  nivel: string
  activo: boolean
}
