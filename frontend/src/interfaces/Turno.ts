export interface Turno {
  id: number
  cancha: string
  fecha: string
  hora_inicio: string
  hora_fin: string
  socio_reserva_id: number | null
  socio_reserva_nombre: string
  jugadores: string[]
  estado: string
}
