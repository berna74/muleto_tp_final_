import json

from django.http import JsonResponse


def parsear_json(request):
    try:
        body = request.body.decode("utf-8") if request.body else "{}"
        return json.loads(body or "{}")
    except json.JSONDecodeError:
        return None


def respuesta_lista(items, status=200):
    return JsonResponse(items, safe=False, status=status)


def respuesta_paginada(items, page=1, page_size=10):
    total_count = len(items)
    total_pages = (total_count + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]
    return JsonResponse(
        {
            "items": paginated_items,
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages,
        }
    )


def respuesta_item(item, status=200):
    return JsonResponse(item, status=status)


def serializar_categoria(categoria):
    return {
        "id": categoria.id,
        "nombre": categoria.nombre,
        "descripcion": categoria.descripcion,
    }


def serializar_profesor(profesor):
    if not profesor:
        return None
    return {
        "id": profesor.id,
        "nombre": profesor.nombre,
        "apellido": profesor.apellido,
        "dni": profesor.dni or "",
        "horarios_clases": profesor.horarios_clases,
        "telefono": profesor.telefono,
        "email": profesor.email,
    }


def serializar_alumno(alumno):
    return {
        "id": alumno.id,
        "nombre": alumno.nombre,
        "apellido": alumno.apellido,
        "dni": alumno.dni,
        "email": alumno.email,
        "telefono": alumno.telefono,
        "fecha_inscripcion": alumno.fecha_inscripcion.isoformat(),
        "profesor": serializar_profesor(alumno.profesor),
        "nivel": alumno.nivel or "",
        "activo": alumno.activo,
    }


def serializar_socio(socio):
    profesor = socio.profesor
    categorias = [serializar_categoria(item.categoria) for item in socio.sociocategoria_set.select_related("categoria").all()]
    return {
        "id": socio.id,
        "nombre": socio.nombre,
        "apellido": socio.apellido,
        "dni": socio.dni,
        "email": socio.email,
        "telefono": socio.telefono,
        "fecha_inscripcion": socio.fecha_inscripcion.isoformat(),
        "profesor_id": profesor.id if profesor else None,
        "profesor_nombre": f"{profesor.nombre} {profesor.apellido}" if profesor else None,
        "profesor": serializar_profesor(profesor),
        "categorias": categorias,
        "registra_deuda": socio.registra_deuda,
    }


def serializar_turno(turno):
    jugadores = list(turno.jugador_items.values_list("jugador_nombre", flat=True))
    socio_nombre = None
    if turno.socio_reserva:
        socio_nombre = f"{turno.socio_reserva.nombre} {turno.socio_reserva.apellido}"
    return {
        "id": turno.id,
        "cancha": turno.cancha,
        "fecha": turno.fecha.isoformat(),
        "hora_inicio": turno.hora_inicio.strftime("%H:%M:%S"),
        "hora_fin": turno.hora_fin.strftime("%H:%M:%S"),
        "socio_reserva_id": turno.socio_reserva_id,
        "socio_reserva_nombre": socio_nombre,
        "jugadores": jugadores,
        "estado": turno.estado,
    }


def serializar_pago(pago):
    socio_nombre = ""
    alumno_nombre = ""
    profesor_nombre = ""
    if pago.socio:
        socio_nombre = f"{pago.socio.nombre} {pago.socio.apellido}"
    if pago.alumno:
        alumno_nombre = f"{pago.alumno.nombre} {pago.alumno.apellido}"
    if pago.profesor:
        profesor_nombre = f"{pago.profesor.nombre} {pago.profesor.apellido}"
    return {
        "id": pago.id,
        "tipo": pago.tipo,
        "monto": float(pago.monto),
        "fecha_pago": pago.fecha_pago.isoformat(),
        "mes": pago.mes,
        "anio": pago.anio,
        "socio_id": pago.socio_id,
        "alumno_id": pago.alumno_id,
        "profesor_id": pago.profesor_id,
        "metodo_pago": pago.metodo_pago or "",
        "observaciones": pago.observaciones or "",
        "socio_nombre": socio_nombre,
        "alumno_nombre": alumno_nombre,
        "profesor_nombre": profesor_nombre,
    }


def serializar_pelotita(pelotita):
    return {
        "id": pelotita.id,
        "fecha": pelotita.fecha.isoformat(),
        "tipo": pelotita.tipo,
        "cantidad": pelotita.cantidad,
        "precio_unitario": float(pelotita.precio_unitario),
        "total": float(pelotita.total),
        "proveedor": pelotita.proveedor,
        "comprador_tipo": pelotita.comprador_tipo,
        "comprador_id": pelotita.comprador_id,
        "comprador_nombre": pelotita.comprador_nombre,
        "observaciones": pelotita.observaciones,
        "created_at": pelotita.created_at.isoformat() if pelotita.created_at else None,
        "updated_at": pelotita.updated_at.isoformat() if pelotita.updated_at else None,
    }
