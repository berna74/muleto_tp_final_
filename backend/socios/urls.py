from django.urls import re_path

from .views import detalle_socio, coleccion_socios


urlpatterns = [
    re_path(r"^socios/?$", coleccion_socios),
    re_path(r"^socios/(?P<pk>\d+)/?$", detalle_socio),
]
