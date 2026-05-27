from django.urls import re_path

from .views import raiz_api


urlpatterns = [
    re_path(r"^$", raiz_api),
]
