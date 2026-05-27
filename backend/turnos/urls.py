from django.urls import re_path

from .views import detalle_turno, coleccion_turnos


urlpatterns = [
    re_path(r"^turnos/?$", coleccion_turnos),
    re_path(r"^turnos/(?P<pk>\d+)/?$", detalle_turno),
]
