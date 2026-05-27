from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import Turno
from .serializers import TurnoSerializer
from core_api.common import parsear_json, respuesta_item, respuesta_paginada


@csrf_exempt
def coleccion_turnos(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		turnos = Turno.objects.select_related("socio_reserva").prefetch_related("jugador_items").all().order_by("-fecha", "hora_inicio")
		return respuesta_paginada(TurnoSerializer(turnos, many=True).data, page=page)

	data = parsear_json(request)
	if data is None:
		return respuesta_item({"mensaje": "JSON inválido"}, status=400)

	serializer = TurnoSerializer(data=data)
	if not serializer.is_valid():
		return respuesta_item(serializer.errors, status=400)
	with transaction.atomic():
		turno = serializer.save()

	turno = Turno.objects.select_related("socio_reserva").prefetch_related("jugador_items").get(pk=turno.pk)
	return respuesta_item(TurnoSerializer(turno).data, status=201)


@csrf_exempt
def detalle_turno(request, pk):
	try:
		turno = Turno.objects.select_related("socio_reserva").prefetch_related("jugador_items").get(pk=pk)
	except Turno.DoesNotExist:
		return respuesta_item({"mensaje": "Turno no encontrado"}, status=404)

	if request.method == "GET":
		return respuesta_item(TurnoSerializer(turno).data)

	if request.method == "PUT":
		data = parsear_json(request)
		if data is None:
			return respuesta_item({"mensaje": "JSON inválido"}, status=400)
		serializer = TurnoSerializer(turno, data=data, partial=True)
		if not serializer.is_valid():
			return respuesta_item(serializer.errors, status=400)
		with transaction.atomic():
			turno = serializer.save()
		turno = Turno.objects.select_related("socio_reserva").prefetch_related("jugador_items").get(pk=pk)
		return respuesta_item(TurnoSerializer(turno).data)

	if request.method == "DELETE":
		turno.delete()
		return respuesta_item({"mensaje": "Turno eliminado"})

	return respuesta_item({"mensaje": "Método no permitido"}, status=405)
