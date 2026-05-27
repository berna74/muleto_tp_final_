from rest_framework import serializers

from .models import Pelotita


class PelotitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelotita
        fields = (
            "id",
            "fecha",
            "tipo",
            "cantidad",
            "precio_unitario",
            "total",
            "proveedor",
            "comprador_tipo",
            "comprador_id",
            "comprador_nombre",
            "observaciones",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
