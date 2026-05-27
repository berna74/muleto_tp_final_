from django.urls import re_path

from .views import turno_detail, turnos_collection


urlpatterns = [
    re_path(r"^turnos/?$", turnos_collection),
    re_path(r"^turnos/(?P<pk>\d+)/?$", turno_detail),
]
