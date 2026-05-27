from django.urls import re_path

from .views import categoria_detail, categorias_collection


urlpatterns = [
    re_path(r"^categorias/?$", categorias_collection),
    re_path(r"^categorias/(?P<pk>\d+)/?$", categoria_detail),
]
