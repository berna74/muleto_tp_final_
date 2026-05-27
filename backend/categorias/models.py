from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "CATEGORIAS"
        managed = False

    def __str__(self):
        return self.nombre
