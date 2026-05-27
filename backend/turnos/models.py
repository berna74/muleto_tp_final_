from django.db import models


class Turno(models.Model):
    cancha = models.CharField(max_length=50)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    socio_reserva = models.ForeignKey(
        "socios.Socio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="socio_reserva_id",
        related_name="turnos",
    )
    estado = models.CharField(max_length=20, default="disponible")

    class Meta:
        db_table = "TURNOS"
        managed = False

    def __str__(self):
        return f"{self.cancha} - {self.fecha}"


class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, db_column="turno_id", related_name="jugador_items")
    jugador_nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "TURNO_JUGADORES"
        managed = False
