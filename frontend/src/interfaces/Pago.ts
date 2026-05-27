export interface Pago {
  id: number
  tipo: string
  monto: number
  fecha_pago: string
  mes: number
  anio: number
  socio_id: number | null
  alumno_id: number | null
  profesor_id: number | null
  metodo_pago: string
  observaciones: string
  socio_nombre: string
  alumno_nombre: string
  profesor_nombre: string
}
