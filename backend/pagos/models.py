from django.db import models


class Pago(models.Model):
    tipo = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    mes = models.IntegerField()
    anio = models.IntegerField()
    socio = models.ForeignKey(
        "socios.Socio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="socio_id",
        related_name="pagos",
    )
    alumno = models.ForeignKey(
        "alumnos.Alumno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="alumno_id",
        related_name="pagos",
    )
    profesor = models.ForeignKey(
        "profesores.Profesor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="profesor_id",
        related_name="pagos",
    )
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "PAGOS"
        managed = False
