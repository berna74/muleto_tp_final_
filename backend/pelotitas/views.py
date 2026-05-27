from django.db import models
from django.views.decorators.csrf import csrf_exempt

from .models import Pelotita
from core_api.common import parse_json, response_item, response_list, response_paginated, serialize_pelotita


@csrf_exempt
def pelotitas_collection(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		pelotitas = Pelotita.objects.all().order_by("-fecha", "-id")
		return response_paginated([serialize_pelotita(pelotita) for pelotita in pelotitas], page=page)

	data = parse_json(request)
	if data is None:
		return response_item({"mensaje": "JSON inválido"}, status=400)

	pelotita = Pelotita.objects.create(
		fecha=data.get("fecha"),
		tipo=data.get("tipo", ""),
		cantidad=data.get("cantidad", 0),
		precio_unitario=data.get("precio_unitario", 0),
		total=data.get("total", 0),
		proveedor=data.get("proveedor"),
		comprador_tipo=data.get("comprador_tipo"),
		comprador_id=data.get("comprador_id"),
		comprador_nombre=data.get("comprador_nombre"),
		observaciones=data.get("observaciones"),
	)
	pelotita.refresh_from_db()
	return response_item(serialize_pelotita(pelotita), status=201)


@csrf_exempt
def pelotita_detail(request, pk):
	try:
		pelotita = Pelotita.objects.get(pk=pk)
	except Pelotita.DoesNotExist:
		return response_item({"mensaje": "Pelotita no encontrada"}, status=404)

	if request.method == "GET":
		return response_item(serialize_pelotita(pelotita))

	if request.method == "PUT":
		data = parse_json(request)
		if data is None:
			return response_item({"mensaje": "JSON inválido"}, status=400)
		pelotita.fecha = data.get("fecha", pelotita.fecha)
		pelotita.tipo = data.get("tipo", pelotita.tipo)
		pelotita.cantidad = data.get("cantidad", pelotita.cantidad)
		pelotita.precio_unitario = data.get("precio_unitario", pelotita.precio_unitario)
		pelotita.total = data.get("total", pelotita.total)
		pelotita.proveedor = data.get("proveedor", pelotita.proveedor)
		pelotita.comprador_tipo = data.get("comprador_tipo", pelotita.comprador_tipo)
		pelotita.comprador_id = data.get("comprador_id", pelotita.comprador_id)
		pelotita.comprador_nombre = data.get("comprador_nombre", pelotita.comprador_nombre)
		pelotita.observaciones = data.get("observaciones", pelotita.observaciones)
		pelotita.save()
		pelotita.refresh_from_db()
		return response_item(serialize_pelotita(pelotita))

	if request.method == "DELETE":
		pelotita.delete()
		return response_item({"mensaje": "Pelotita eliminada"})

	return response_item({"mensaje": "Método no permitido"}, status=405)


def pelotitas_resumen(request):
	resumen = list(
		Pelotita.objects.values("tipo")
		.annotate(
			total_cantidad=models.Sum("cantidad"),
			total_monto=models.Sum("total"),
			total_registros=models.Count("id"),
		)
		.order_by("tipo")
	)
	return response_list(resumen)
