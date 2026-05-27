from django.views.decorators.csrf import csrf_exempt

from .models import Alumno
from .serializers import AlumnoSerializer
from core_api.common import parsear_json, respuesta_item, respuesta_paginada


@csrf_exempt
def coleccion_alumnos(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		alumnos = AlumnoSerializer(
			Alumno.objects.select_related("profesor").all().order_by("id"),
			many=True,
		).data
		return respuesta_paginada(alumnos, page=page)

	data = parsear_json(request)
	if data is None:
		return respuesta_item({"mensaje": "JSON inválido"}, status=400)

	serializer = AlumnoSerializer(data=data)
	if not serializer.is_valid():
		return respuesta_item(serializer.errors, status=400)
	alumno = serializer.save()
	alumno.refresh_from_db()
	return respuesta_item(AlumnoSerializer(alumno).data, status=201)


@csrf_exempt
def detalle_alumno(request, pk):
	try:
		alumno = Alumno.objects.select_related("profesor").get(pk=pk)
	except Alumno.DoesNotExist:
		return respuesta_item({"mensaje": "Alumno no encontrado"}, status=404)

	if request.method == "GET":
		return respuesta_item(AlumnoSerializer(alumno).data)

	if request.method == "PUT":
		data = parsear_json(request)
		if data is None:
			return respuesta_item({"mensaje": "JSON inválido"}, status=400)
		serializer = AlumnoSerializer(alumno, data=data, partial=True)
		if not serializer.is_valid():
			return respuesta_item(serializer.errors, status=400)
		alumno = serializer.save()
		alumno.refresh_from_db()
		return respuesta_item(AlumnoSerializer(alumno).data)

	if request.method == "DELETE":
		alumno.delete()
		return respuesta_item({"mensaje": "Alumno eliminado"})

	return respuesta_item({"mensaje": "Método no permitido"}, status=405)
