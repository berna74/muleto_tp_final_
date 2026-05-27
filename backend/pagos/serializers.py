from rest_framework import serializers

from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    socio_nombre = serializers.SerializerMethodField()
    alumno_nombre = serializers.SerializerMethodField()
    profesor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = (
            "id",
            "tipo",
            "monto",
            "fecha_pago",
            "mes",
            "anio",
            "socio_id",
            "alumno_id",
            "profesor_id",
            "metodo_pago",
            "observaciones",
            "socio_nombre",
            "alumno_nombre",
            "profesor_nombre",
        )

    def get_socio_nombre(self, obj):
        if not obj.socio:
            return ""
        return f"{obj.socio.nombre} {obj.socio.apellido}"

    def get_alumno_nombre(self, obj):
        if not obj.alumno:
            return ""
        return f"{obj.alumno.nombre} {obj.alumno.apellido}"

    def get_profesor_nombre(self, obj):
        if not obj.profesor:
            return ""
        return f"{obj.profesor.nombre} {obj.profesor.apellido}"
