from rest_framework import serializers

from .models import Alumno
from profesores.serializers import ProfesorSerializer


class AlumnoSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer(read_only=True)
    profesor_id = serializers.PrimaryKeyRelatedField(
        source="profesor",
        queryset=Alumno._meta.get_field("profesor").related_model.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
    )

    def validate_dni(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("El DNI debe contener solo números")
        return str(value)

    class Meta:
        model = Alumno
        fields = (
            "id",
            "nombre",
            "apellido",
            "dni",
            "email",
            "telefono",
            "fecha_inscripcion",
            "profesor",
            "profesor_id",
            "nivel",
            "activo",
        )
