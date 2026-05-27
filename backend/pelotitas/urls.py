from django.urls import re_path

from .views import detalle_pelotita, coleccion_pelotitas, resumen_pelotitas


urlpatterns = [
    re_path(r"^pelotitas/?$", coleccion_pelotitas),
    re_path(r"^pelotitas/(?P<pk>\d+)/?$", detalle_pelotita),
    re_path(r"^pelotitas/resumen/?$", resumen_pelotitas),
]
