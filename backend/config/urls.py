from django.http import JsonResponse
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("api/", include("core_api.urls")),
    path("api/", include("categorias.urls")),
    path("api/", include("profesores.urls")),
    path("api/", include("alumnos.urls")),
    path("api/", include("socios.urls")),
    path("api/", include("turnos.urls")),
    path("api/", include("pagos.urls")),
    path("api/", include("pelotitas.urls")),
    path("admin/", admin.site.urls),
    path("", lambda request: JsonResponse({"message": "Django backend activo"})),
]