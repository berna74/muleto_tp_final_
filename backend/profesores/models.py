from django.db import models


class Profesor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, blank=True, null=True, unique=True)
    horarios_clases = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "PROFESORES"
        managed = False

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
