from django.urls import re_path

from .views import pago_detail, pagos_collection


urlpatterns = [
    re_path(r"^pagos/?$", pagos_collection),
    re_path(r"^pagos/(?P<pk>\d+)/?$", pago_detail),
]
