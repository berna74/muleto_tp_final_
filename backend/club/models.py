from alumnos.models import Alumno
from categorias.models import Categoria
from pagos.models import Pago
from pelotitas.models import Pelotita
from profesores.models import Profesor
from socios.models import Socio, SocioCategoria
from turnos.models import Turno, TurnoJugador

__all__ = [
    "Categoria",
    "Profesor",
    "Socio",
    "SocioCategoria",
    "Alumno",
    "Turno",
    "TurnoJugador",
    "Pago",
    "Pelotita",
]
