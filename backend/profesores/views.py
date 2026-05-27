from django.views.decorators.csrf import csrf_exempt

from .models import Profesor
from .serializers import ProfesorSerializer
from core_api.common import parsear_json, respuesta_item, respuesta_paginada


@csrf_exempt
def coleccion_profesores(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		profesores = ProfesorSerializer(Profesor.objects.all().order_by("id"), many=True).data
		return respuesta_paginada(profesores, page=page)

	data = parsear_json(request)
	if data is None:
		return respuesta_item({"mensaje": "JSON inválido"}, status=400)

	serializer = ProfesorSerializer(data=data)
	if not serializer.is_valid():
		return respuesta_item(serializer.errors, status=400)
	profesor = serializer.save()
	return respuesta_item(ProfesorSerializer(profesor).data, status=201)


@csrf_exempt
def detalle_profesor(request, pk):
	try:
		profesor = Profesor.objects.get(pk=pk)
	except Profesor.DoesNotExist:
		return respuesta_item({"mensaje": "Profesor no encontrado"}, status=404)

	if request.method == "GET":
		return respuesta_item(ProfesorSerializer(profesor).data)

	if request.method == "PUT":
		data = parsear_json(request)
		if data is None:
			return respuesta_item({"mensaje": "JSON inválido"}, status=400)
		serializer = ProfesorSerializer(profesor, data=data, partial=True)
		if not serializer.is_valid():
			return respuesta_item(serializer.errors, status=400)
		serializer.save()
		return respuesta_item(serializer.data)

	if request.method == "DELETE":
		profesor.delete()
		return respuesta_item({"mensaje": "Profesor eliminado"})

	return respuesta_item({"mensaje": "Método no permitido"}, status=405)
