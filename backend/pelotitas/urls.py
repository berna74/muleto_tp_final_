from django.urls import re_path

from .views import pelotita_detail, pelotitas_collection, pelotitas_resumen


urlpatterns = [
    re_path(r"^pelotitas/?$", pelotitas_collection),
    re_path(r"^pelotitas/(?P<pk>\d+)/?$", pelotita_detail),
    re_path(r"^pelotitas/resumen/?$", pelotitas_resumen),
]
