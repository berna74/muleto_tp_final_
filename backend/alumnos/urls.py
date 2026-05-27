from django.urls import re_path

from .views import detalle_alumno, coleccion_alumnos


urlpatterns = [
    re_path(r"^alumnos/?$", coleccion_alumnos),
    re_path(r"^alumnos/(?P<pk>\d+)/?$", detalle_alumno),
]
