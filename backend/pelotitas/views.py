from django.db import models
from django.views.decorators.csrf import csrf_exempt

from .models import Pelotita
from .serializers import PelotitaSerializer
from core_api.common import parsear_json, respuesta_item, respuesta_lista, respuesta_paginada


@csrf_exempt
def coleccion_pelotitas(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		pelotitas = Pelotita.objects.all().order_by("-fecha", "-id")
		return respuesta_paginada(PelotitaSerializer(pelotitas, many=True).data, page=page)

	data = parsear_json(request)
	if data is None:
		return respuesta_item({"mensaje": "JSON inválido"}, status=400)

	serializer = PelotitaSerializer(data=data)
	if not serializer.is_valid():
		return respuesta_item(serializer.errors, status=400)
	pelotita = serializer.save()
	pelotita.refresh_from_db()
	return respuesta_item(PelotitaSerializer(pelotita).data, status=201)


@csrf_exempt
def detalle_pelotita(request, pk):
	try:
		pelotita = Pelotita.objects.get(pk=pk)
	except Pelotita.DoesNotExist:
		return respuesta_item({"mensaje": "Pelotita no encontrada"}, status=404)

	if request.method == "GET":
		return respuesta_item(PelotitaSerializer(pelotita).data)

	if request.method == "PUT":
		data = parsear_json(request)
		if data is None:
			return respuesta_item({"mensaje": "JSON inválido"}, status=400)
		serializer = PelotitaSerializer(pelotita, data=data, partial=True)
		if not serializer.is_valid():
			return respuesta_item(serializer.errors, status=400)
		pelotita = serializer.save()
		pelotita.refresh_from_db()
		return respuesta_item(PelotitaSerializer(pelotita).data)

	if request.method == "DELETE":
		pelotita.delete()
		return respuesta_item({"mensaje": "Pelotita eliminada"})

	return respuesta_item({"mensaje": "Método no permitido"}, status=405)


def resumen_pelotitas(request):
	resumen = list(
		Pelotita.objects.values("tipo")
		.annotate(
			total_cantidad=models.Sum("cantidad"),
			total_monto=models.Sum("total"),
			total_registros=models.Count("id"),
		)
		.order_by("tipo")
	)
	return respuesta_lista(resumen)
