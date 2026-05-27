from django.urls import re_path

from .views import profesor_detail, profesores_collection


urlpatterns = [
    re_path(r"^profesores/?$", profesores_collection),
    re_path(r"^profesores/(?P<pk>\d+)/?$", profesor_detail),
]
