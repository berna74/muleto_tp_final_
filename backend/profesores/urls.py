from django.urls import re_path

from .views import detalle_profesor, coleccion_profesores


urlpatterns = [
    re_path(r"^profesores/?$", coleccion_profesores),
    re_path(r"^profesores/(?P<pk>\d+)/?$", detalle_profesor),
]
