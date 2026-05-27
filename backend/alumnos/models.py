from django.db import models


class Alumno(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_inscripcion = models.DateField()
    profesor = models.ForeignKey(
        "profesores.Profesor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="profesor_id",
        related_name="alumnos",
    )
    nivel = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "ALUMNOS"
        managed = False

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
