from django.urls import re_path

from .views import socio_detail, socios_collection


urlpatterns = [
    re_path(r"^socios/?$", socios_collection),
    re_path(r"^socios/(?P<pk>\d+)/?$", socio_detail),
]
