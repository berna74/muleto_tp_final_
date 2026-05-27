from django.urls import re_path

from .views import detalle_pago, coleccion_pagos


urlpatterns = [
    re_path(r"^pagos/?$", coleccion_pagos),
    re_path(r"^pagos/(?P<pk>\d+)/?$", detalle_pago),
]
