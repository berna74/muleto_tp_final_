from django.views.decorators.csrf import csrf_exempt

from .models import Pago
from core_api.common import parse_json, response_item, response_paginated, serialize_pago


@csrf_exempt
def pagos_collection(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		pagos = Pago.objects.select_related("socio", "alumno", "profesor").all().order_by("-fecha_pago", "-id")
		return response_paginated([serialize_pago(pago) for pago in pagos], page=page)

	data = parse_json(request)
	if data is None:
		return response_item({"mensaje": "JSON inválido"}, status=400)

	pago = Pago.objects.create(
		tipo=data.get("tipo", ""),
		monto=data.get("monto", 0),
		fecha_pago=data.get("fecha_pago"),
		mes=data.get("mes", 0),
		anio=data.get("anio", 0),
		socio_id=data.get("socio_id"),
		alumno_id=data.get("alumno_id"),
		profesor_id=data.get("profesor_id"),
		metodo_pago=data.get("metodo_pago", ""),
		observaciones=data.get("observaciones", ""),
	)
	pago = Pago.objects.select_related("socio", "alumno", "profesor").get(pk=pago.pk)
	return response_item(serialize_pago(pago), status=201)


@csrf_exempt
def pago_detail(request, pk):
	try:
		pago = Pago.objects.select_related("socio", "alumno", "profesor").get(pk=pk)
	except Pago.DoesNotExist:
		return response_item({"mensaje": "Pago no encontrado"}, status=404)

	if request.method == "GET":
		return response_item(serialize_pago(pago))

	if request.method == "PUT":
		data = parse_json(request)
		if data is None:
			return response_item({"mensaje": "JSON inválido"}, status=400)
		pago.tipo = data.get("tipo", pago.tipo)
		pago.monto = data.get("monto", pago.monto)
		pago.fecha_pago = data.get("fecha_pago", pago.fecha_pago)
		pago.mes = data.get("mes", pago.mes)
		pago.anio = data.get("anio", pago.anio)
		pago.socio_id = data.get("socio_id", pago.socio_id)
		pago.alumno_id = data.get("alumno_id", pago.alumno_id)
		pago.profesor_id = data.get("profesor_id", pago.profesor_id)
		pago.metodo_pago = data.get("metodo_pago", pago.metodo_pago)
		pago.observaciones = data.get("observaciones", pago.observaciones)
		pago.save()
		pago = Pago.objects.select_related("socio", "alumno", "profesor").get(pk=pk)
		return response_item(serialize_pago(pago))

	if request.method == "DELETE":
		pago.delete()
		return response_item({"mensaje": "Pago eliminado"})

	return response_item({"mensaje": "Método no permitido"}, status=405)
