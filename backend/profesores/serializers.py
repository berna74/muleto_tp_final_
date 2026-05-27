from rest_framework import serializers

from .models import Profesor


class ProfesorSerializer(serializers.ModelSerializer):
    def validate_dni(self, value):
        if value in (None, ""):
            return value
        if not str(value).isdigit():
            raise serializers.ValidationError("El DNI debe contener solo números")
        return str(value)

    class Meta:
        model = Profesor
        fields = (
            "id",
            "nombre",
            "apellido",
            "dni",
            "horarios_clases",
            "telefono",
            "email",
        )
