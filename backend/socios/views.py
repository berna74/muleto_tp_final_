from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import Socio
from .serializers import SocioSerializer
from core_api.common import parsear_json, respuesta_item, respuesta_paginada


@csrf_exempt
def coleccion_socios(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		socios = Socio.objects.select_related("profesor").all().order_by("id")
		return respuesta_paginada(SocioSerializer(socios, many=True).data, page=page)

	data = parsear_json(request)
	if data is None:
		return respuesta_item({"mensaje": "JSON inválido"}, status=400)

	serializer = SocioSerializer(data=data)
	if not serializer.is_valid():
		return respuesta_item(serializer.errors, status=400)
	with transaction.atomic():
		socio = serializer.save()

	socio = Socio.objects.select_related("profesor").get(pk=socio.pk)
	return respuesta_item(SocioSerializer(socio).data, status=201)


@csrf_exempt
def detalle_socio(request, pk):
	try:
		socio = Socio.objects.select_related("profesor").get(pk=pk)
	except Socio.DoesNotExist:
		return respuesta_item({"mensaje": "Socio no encontrado"}, status=404)

	if request.method == "GET":
		return respuesta_item(SocioSerializer(socio).data)

	if request.method == "PUT":
		data = parsear_json(request)
		if data is None:
			return respuesta_item({"mensaje": "JSON inválido"}, status=400)
		serializer = SocioSerializer(socio, data=data, partial=True)
		if not serializer.is_valid():
			return respuesta_item(serializer.errors, status=400)
		with transaction.atomic():
			socio = serializer.save()
		socio = Socio.objects.select_related("profesor").get(pk=pk)
		return respuesta_item(SocioSerializer(socio).data)

	if request.method == "DELETE":
		socio.delete()
		return respuesta_item({"mensaje": "Socio eliminado"})

	return respuesta_item({"mensaje": "Método no permitido"}, status=405)
