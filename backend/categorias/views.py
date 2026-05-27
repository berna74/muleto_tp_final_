from django.views.decorators.csrf import csrf_exempt

from .models import Categoria
from core_api.common import parse_json, response_item, response_paginated, serialize_categoria


@csrf_exempt
def categorias_collection(request):
	if request.method == "GET":
		page = int(request.GET.get("page", 1))
		categorias = [serialize_categoria(categoria) for categoria in Categoria.objects.all().order_by("id")]
		return response_paginated(categorias, page=page)

	data = parse_json(request)
	if data is None:
		return response_item({"mensaje": "JSON inválido"}, status=400)

	categoria = Categoria.objects.create(
		nombre=data.get("nombre", ""),
		descripcion=data.get("descripcion", ""),
	)
	return response_item(serialize_categoria(categoria), status=201)


@csrf_exempt
def categoria_detail(request, pk):
	try:
		categoria = Categoria.objects.get(pk=pk)
	except Categoria.DoesNotExist:
		return response_item({"mensaje": "Categoría no encontrada"}, status=404)

	if request.method == "GET":
		return response_item(serialize_categoria(categoria))

	if request.method == "PUT":
		data = parse_json(request)
		if data is None:
			return response_item({"mensaje": "JSON inválido"}, status=400)
		categoria.nombre = data.get("nombre", categoria.nombre)
		categoria.descripcion = data.get("descripcion", categoria.descripcion)
		categoria.save(update_fields=["nombre", "descripcion"])
		return response_item(serialize_categoria(categoria))

	if request.method == "DELETE":
		categoria.delete()
		return response_item({"mensaje": "Categoría eliminada"})

	return response_item({"mensaje": "Método no permitido"}, status=405)
