from django.urls import re_path

from .views import alumno_detail, alumnos_collection


urlpatterns = [
    re_path(r"^alumnos/?$", alumnos_collection),
    re_path(r"^alumnos/(?P<pk>\d+)/?$", alumno_detail),
]
