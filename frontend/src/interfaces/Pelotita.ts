export interface Pelotita {
  id?: number
  fecha: string
  tipo: 'compra' | 'venta'
  cantidad: number
  precio_unitario: number
  total: number
  proveedor?: string
  comprador_tipo?: 'socio' | 'alumno' | 'otro' | null
  comprador_id?: number | null
  comprador_nombre?: string | null
  observaciones?: string
  created_at?: string
  updated_at?: string
}

export interface ResumenPelotitas {
  tipo: string
  total_cantidad: number
  total_monto: number
  total_registros: number
}
