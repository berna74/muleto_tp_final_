from django.views.decorators.csrf import csrf_exempt

from .models import Pago
from .serializers import PagoSerializer
from core_api.common import parsear_json, respuesta_item, respuesta_paginada


@csrf_exempt
def coleccion_pagos(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		pagos = Pago.objects.select_related("socio", "alumno", "profesor").all().order_by("-fecha_pago", "-id")
		return respuesta_paginada(PagoSerializer(pagos, many=True).data, page=page)

	data = parsear_json(request)
	if data is None:
		return respuesta_item({"mensaje": "JSON inválido"}, status=400)

	serializer = PagoSerializer(data=data)
	if not serializer.is_valid():
		return respuesta_item(serializer.errors, status=400)
	pago = serializer.save()
	pago = Pago.objects.select_related("socio", "alumno", "profesor").get(pk=pago.pk)
	return respuesta_item(PagoSerializer(pago).data, status=201)


@csrf_exempt
def detalle_pago(request, pk):
	try:
		pago = Pago.objects.select_related("socio", "alumno", "profesor").get(pk=pk)
	except Pago.DoesNotExist:
		return respuesta_item({"mensaje": "Pago no encontrado"}, status=404)

	if request.method == "GET":
		return respuesta_item(PagoSerializer(pago).data)

	if request.method == "PUT":
		data = parsear_json(request)
		if data is None:
			return respuesta_item({"mensaje": "JSON inválido"}, status=400)
		serializer = PagoSerializer(pago, data=data, partial=True)
		if not serializer.is_valid():
			return respuesta_item(serializer.errors, status=400)
		pago = serializer.save()
		pago = Pago.objects.select_related("socio", "alumno", "profesor").get(pk=pk)
		return respuesta_item(PagoSerializer(pago).data)

	if request.method == "DELETE":
		pago.delete()
		return respuesta_item({"mensaje": "Pago eliminado"})

	return respuesta_item({"mensaje": "Método no permitido"}, status=405)
