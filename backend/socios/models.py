from django.db import models


class Socio(models.Model):
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
        related_name="socios",
    )
    registra_deuda = models.BooleanField(default=False)
    categorias = models.ManyToManyField("categorias.Categoria", through="SocioCategoria", related_name="socios")

    class Meta:
        db_table = "SOCIOS"
        managed = False

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class SocioCategoria(models.Model):
    id = models.AutoField(primary_key=True)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, db_column="socio_id")
    categoria = models.ForeignKey("categorias.Categoria", on_delete=models.CASCADE, db_column="categoria_id")

    class Meta:
        db_table = "SOCIO_CATEGORIA"
        managed = False
        unique_together = (("socio", "categoria"),)
