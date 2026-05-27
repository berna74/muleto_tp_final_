from django.db import transaction
from rest_framework import serializers

from .models import Turno, TurnoJugador


class TurnoSerializer(serializers.ModelSerializer):
    socio_reserva_id = serializers.PrimaryKeyRelatedField(
        source="socio_reserva",
        queryset=Turno._meta.get_field("socio_reserva").related_model.objects.all(),
        allow_null=True,
        required=False,
    )
    socio_reserva_nombre = serializers.SerializerMethodField()
    jugadores = serializers.ListField(
        child=serializers.CharField(max_length=100, allow_blank=False),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Turno
        fields = (
            "id",
            "cancha",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "socio_reserva_id",
            "socio_reserva_nombre",
            "jugadores",
            "estado",
        )

    def get_socio_reserva_nombre(self, obj):
        if not obj.socio_reserva:
            return None
        return f"{obj.socio_reserva.nombre} {obj.socio_reserva.apellido}"

    def _sync_jugadores(self, turno, jugadores):
        if jugadores is None:
            return
        TurnoJugador.objects.filter(turno=turno).delete()
        items = [
            TurnoJugador(turno=turno, jugador_nombre=str(jugador).strip())
            for jugador in jugadores
            if str(jugador).strip()
        ]
        TurnoJugador.objects.bulk_create(items)

    def create(self, validated_data):
        jugadores = validated_data.pop("jugadores", [])
        with transaction.atomic():
            turno = Turno.objects.create(**validated_data)
            self._sync_jugadores(turno, jugadores)
        return turno

    def update(self, instance, validated_data):
        jugadores = validated_data.pop("jugadores", None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            self._sync_jugadores(instance, jugadores)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["jugadores"] = list(
            instance.jugador_items.values_list("jugador_nombre", flat=True)
        )
        return data
