from django.http import JsonResponse


def raiz_api(request):
	return JsonResponse({"message": "API Django andando"})
