from django.views.decorators.csrf import csrf_exempt

from .models import Alumno
from core_api.common import parse_json, response_item, response_paginated, serialize_alumno


@csrf_exempt
def alumnos_collection(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		alumnos = [
			serialize_alumno(alumno)
			for alumno in Alumno.objects.select_related("profesor").all().order_by("id")
		]
		return response_paginated(alumnos, page=page)

	data = parse_json(request)
	if data is None:
		return response_item({"mensaje": "JSON inválido"}, status=400)

	alumno = Alumno.objects.create(
		nombre=data.get("nombre", ""),
		apellido=data.get("apellido", ""),
		dni=data.get("dni", ""),
		email=data.get("email", ""),
		telefono=data.get("telefono", ""),
		fecha_inscripcion=data.get("fecha_inscripcion"),
		profesor_id=data.get("profesor_id"),
		nivel=data.get("nivel", ""),
		activo=data.get("activo", True),
	)
	alumno.refresh_from_db()
	return response_item(serialize_alumno(alumno), status=201)


@csrf_exempt
def alumno_detail(request, pk):
	try:
		alumno = Alumno.objects.select_related("profesor").get(pk=pk)
	except Alumno.DoesNotExist:
		return response_item({"mensaje": "Alumno no encontrado"}, status=404)

	if request.method == "GET":
		return response_item(serialize_alumno(alumno))

	if request.method == "PUT":
		data = parse_json(request)
		if data is None:
			return response_item({"mensaje": "JSON inválido"}, status=400)
		alumno.nombre = data.get("nombre", alumno.nombre)
		alumno.apellido = data.get("apellido", alumno.apellido)
		alumno.dni = data.get("dni", alumno.dni)
		alumno.email = data.get("email", alumno.email)
		alumno.telefono = data.get("telefono", alumno.telefono)
		alumno.fecha_inscripcion = data.get("fecha_inscripcion", alumno.fecha_inscripcion)
		alumno.profesor_id = data.get("profesor_id", alumno.profesor_id)
		alumno.nivel = data.get("nivel", alumno.nivel)
		alumno.activo = data.get("activo", alumno.activo)
		alumno.save()
		alumno.refresh_from_db()
		return response_item(serialize_alumno(alumno))

	if request.method == "DELETE":
		alumno.delete()
		return response_item({"mensaje": "Alumno eliminado"})

	return response_item({"mensaje": "Método no permitido"}, status=405)
