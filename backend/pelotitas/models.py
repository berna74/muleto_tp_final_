from django.db import models


class Pelotita(models.Model):
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.CharField(max_length=200, blank=True, null=True)
    comprador_tipo = models.CharField(max_length=20, blank=True, null=True)
    comprador_id = models.IntegerField(blank=True, null=True)
    comprador_nombre = models.CharField(max_length=200, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "PELOTITAS"
        managed = False
