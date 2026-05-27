import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error

load_dotenv()
database_name = os.getenv("DB_NAME")

database_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'port': int(os.getenv("DB_PORT", 5432)),
    'dbname': database_name,
}

DROPPED_TB = {
    "pagos": 'DROP TABLE IF EXISTS "PAGOS" CASCADE;',
    "turno_jugadores": 'DROP TABLE IF EXISTS "TURNO_JUGADORES" CASCADE;',
    "turnos": 'DROP TABLE IF EXISTS "TURNOS" CASCADE;',
    "alumnos": 'DROP TABLE IF EXISTS "ALUMNOS" CASCADE;',
    "socio_categoria": 'DROP TABLE IF EXISTS "SOCIO_CATEGORIA" CASCADE;',
    "socios": 'DROP TABLE IF EXISTS "SOCIOS" CASCADE;',
    "profesores": 'DROP TABLE IF EXISTS "PROFESORES" CASCADE;',
    "categorias": 'DROP TABLE IF EXISTS "CATEGORIAS" CASCADE;',
    "pelotitas": 'DROP TABLE IF EXISTS "PELOTITAS" CASCADE;',
}


def rollback_db():
    with psycopg2.connect(**database_config) as cxn:
        with cxn.cursor() as cursor:
            for table in DROPPED_TB:
                print(f"Dropped table: {table}", end=" ")
                try:
                    cursor.execute(DROPPED_TB[table])
                    print('ok')
                except Error as exc:
                    print(f"{exc}")
        cxn.commit()

rollback_db()
