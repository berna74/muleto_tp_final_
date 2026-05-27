from django.urls import re_path

from .views import api_root


urlpatterns = [
    re_path(r"^$", api_root),
]
