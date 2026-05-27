from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import Turno, TurnoJugador
from core_api.common import parse_json, response_item, response_paginated, serialize_turno


@csrf_exempt
def turnos_collection(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		turnos = Turno.objects.select_related("socio_reserva").prefetch_related("jugador_items").all().order_by("-fecha", "hora_inicio")
		return response_paginated([serialize_turno(turno) for turno in turnos], page=page)

	data = parse_json(request)
	if data is None:
		return response_item({"mensaje": "JSON inválido"}, status=400)

	with transaction.atomic():
		turno = Turno.objects.create(
			cancha=data.get("cancha", ""),
			fecha=data.get("fecha"),
			hora_inicio=data.get("hora_inicio"),
			hora_fin=data.get("hora_fin"),
			socio_reserva_id=data.get("socio_reserva_id"),
			estado=data.get("estado", "reservado"),
		)
		for jugador in data.get("jugadores", []):
			if str(jugador).strip():
				TurnoJugador.objects.create(turno=turno, jugador_nombre=str(jugador).strip())

	turno = Turno.objects.select_related("socio_reserva").prefetch_related("jugador_items").get(pk=turno.pk)
	return response_item(serialize_turno(turno), status=201)


@csrf_exempt
def turno_detail(request, pk):
	try:
		turno = Turno.objects.select_related("socio_reserva").prefetch_related("jugador_items").get(pk=pk)
	except Turno.DoesNotExist:
		return response_item({"mensaje": "Turno no encontrado"}, status=404)

	if request.method == "GET":
		return response_item(serialize_turno(turno))

	if request.method == "PUT":
		data = parse_json(request)
		if data is None:
			return response_item({"mensaje": "JSON inválido"}, status=400)
		with transaction.atomic():
			turno.cancha = data.get("cancha", turno.cancha)
			turno.fecha = data.get("fecha", turno.fecha)
			turno.hora_inicio = data.get("hora_inicio", turno.hora_inicio)
			turno.hora_fin = data.get("hora_fin", turno.hora_fin)
			turno.socio_reserva_id = data.get("socio_reserva_id", turno.socio_reserva_id)
			turno.estado = data.get("estado", turno.estado)
			turno.save()
			TurnoJugador.objects.filter(turno=turno).delete()
			for jugador in data.get("jugadores", []):
				if str(jugador).strip():
					TurnoJugador.objects.create(turno=turno, jugador_nombre=str(jugador).strip())
		turno = Turno.objects.select_related("socio_reserva").prefetch_related("jugador_items").get(pk=pk)
		return response_item(serialize_turno(turno))

	if request.method == "DELETE":
		turno.delete()
		return response_item({"mensaje": "Turno eliminado"})

	return response_item({"mensaje": "Método no permitido"}, status=405)
