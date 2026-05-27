from django.views.decorators.csrf import csrf_exempt

from .models import Profesor
from core_api.common import parse_json, response_item, response_paginated, serialize_profesor


@csrf_exempt
def profesores_collection(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		profesores = [serialize_profesor(profesor) for profesor in Profesor.objects.all().order_by("id")]
		return response_paginated(profesores, page=page)

	data = parse_json(request)
	if data is None:
		return response_item({"mensaje": "JSON inválido"}, status=400)

	profesor = Profesor.objects.create(
		nombre=data.get("nombre", ""),
		apellido=data.get("apellido", ""),
		dni=(data.get("dni") or None),
		horarios_clases=data.get("horarios_clases", ""),
		telefono=data.get("telefono", ""),
		email=data.get("email", ""),
	)
	return response_item(serialize_profesor(profesor), status=201)


@csrf_exempt
def profesor_detail(request, pk):
	try:
		profesor = Profesor.objects.get(pk=pk)
	except Profesor.DoesNotExist:
		return response_item({"mensaje": "Profesor no encontrado"}, status=404)

	if request.method == "GET":
		return response_item(serialize_profesor(profesor))

	if request.method == "PUT":
		data = parse_json(request)
		if data is None:
			return response_item({"mensaje": "JSON inválido"}, status=400)
		profesor.nombre = data.get("nombre", profesor.nombre)
		profesor.apellido = data.get("apellido", profesor.apellido)
		profesor.dni = data.get("dni", profesor.dni)
		profesor.horarios_clases = data.get("horarios_clases", profesor.horarios_clases)
		profesor.telefono = data.get("telefono", profesor.telefono)
		profesor.email = data.get("email", profesor.email)
		profesor.save()
		return response_item(serialize_profesor(profesor))

	if request.method == "DELETE":
		profesor.delete()
		return response_item({"mensaje": "Profesor eliminado"})

	return response_item({"mensaje": "Método no permitido"}, status=405)
