from django.urls import re_path

from .views import detalle_categoria, coleccion_categorias


urlpatterns = [
    re_path(r"^categorias/?$", coleccion_categorias),
    re_path(r"^categorias/(?P<pk>\d+)/?$", detalle_categoria),
]
