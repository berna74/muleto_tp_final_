from django.views.decorators.csrf import csrf_exempt

from .models import Categoria
from .serializers import CategoriaSerializer
from core_api.common import parsear_json, respuesta_item, respuesta_paginada


@csrf_exempt
def coleccion_categorias(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		categorias = CategoriaSerializer(Categoria.objects.all().order_by("id"), many=True).data
		return respuesta_paginada(categorias, page=page)

	data = parsear_json(request)
	if data is None:
		return respuesta_item({"mensaje": "JSON inválido"}, status=400)

	serializer = CategoriaSerializer(data=data)
	if not serializer.is_valid():
		return respuesta_item(serializer.errors, status=400)
	categoria = serializer.save()
	return respuesta_item(CategoriaSerializer(categoria).data, status=201)


@csrf_exempt
def detalle_categoria(request, pk):
	try:
		categoria = Categoria.objects.get(pk=pk)
	except Categoria.DoesNotExist:
		return respuesta_item({"mensaje": "Categoría no encontrada"}, status=404)

	if request.method == "GET":
		return respuesta_item(CategoriaSerializer(categoria).data)

	if request.method == "PUT":
		data = parsear_json(request)
		if data is None:
			return respuesta_item({"mensaje": "JSON inválido"}, status=400)
		serializer = CategoriaSerializer(categoria, data=data, partial=True)
		if not serializer.is_valid():
			return respuesta_item(serializer.errors, status=400)
		serializer.save()
		return respuesta_item(serializer.data)

	if request.method == "DELETE":
		categoria.delete()
		return respuesta_item({"mensaje": "Categoría eliminada"})

	return respuesta_item({"mensaje": "Método no permitido"}, status=405)
