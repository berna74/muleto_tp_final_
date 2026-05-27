from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import Socio, SocioCategoria
from core_api.common import parse_json, response_item, response_paginated, serialize_socio


@csrf_exempt
def socios_collection(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		socios = Socio.objects.select_related("profesor").all().order_by("id")
		return response_paginated([serialize_socio(socio) for socio in socios], page=page)

	data = parse_json(request)
	if data is None:
		return response_item({"mensaje": "JSON inválido"}, status=400)

	with transaction.atomic():
		socio = Socio.objects.create(
			nombre=data.get("nombre", ""),
			apellido=data.get("apellido", ""),
			dni=data.get("dni", ""),
			email=data.get("email", ""),
			telefono=data.get("telefono", ""),
			fecha_inscripcion=data.get("fecha_inscripcion"),
			profesor_id=data.get("profesor_id"),
			registra_deuda=data.get("registra_deuda", False),
		)
		for categoria_id in data.get("categorias", []):
			SocioCategoria.objects.create(socio=socio, categoria_id=categoria_id)

	socio = Socio.objects.select_related("profesor").get(pk=socio.pk)
	return response_item(serialize_socio(socio), status=201)


@csrf_exempt
def socio_detail(request, pk):
	try:
		socio = Socio.objects.select_related("profesor").get(pk=pk)
	except Socio.DoesNotExist:
		return response_item({"mensaje": "Socio no encontrado"}, status=404)

	if request.method == "GET":
		return response_item(serialize_socio(socio))

	if request.method == "PUT":
		data = parse_json(request)
		if data is None:
			return response_item({"mensaje": "JSON inválido"}, status=400)
		with transaction.atomic():
			socio.nombre = data.get("nombre", socio.nombre)
			socio.apellido = data.get("apellido", socio.apellido)
			socio.dni = data.get("dni", socio.dni)
			socio.email = data.get("email", socio.email)
			socio.telefono = data.get("telefono", socio.telefono)
			socio.fecha_inscripcion = data.get("fecha_inscripcion", socio.fecha_inscripcion)
			socio.profesor_id = data.get("profesor_id", socio.profesor_id)
			socio.registra_deuda = data.get("registra_deuda", socio.registra_deuda)
			socio.save()
			SocioCategoria.objects.filter(socio=socio).delete()
			for categoria_id in data.get("categorias", []):
				SocioCategoria.objects.create(socio=socio, categoria_id=categoria_id)
		socio = Socio.objects.select_related("profesor").get(pk=pk)
		return response_item(serialize_socio(socio))

	if request.method == "DELETE":
		socio.delete()
		return response_item({"mensaje": "Socio eliminado"})

	return response_item({"mensaje": "Método no permitido"}, status=405)
