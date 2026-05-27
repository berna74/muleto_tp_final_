import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv("DB_NAME")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

TABLES = {
    "CATEGORIAS": """
        CREATE TABLE IF NOT EXISTS "CATEGORIAS" (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            descripcion VARCHAR(200)
        )
    """,
    "PROFESORES": """
        CREATE TABLE IF NOT EXISTS "PROFESORES" (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            dni VARCHAR(20) UNIQUE,
            horarios_clases VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """,
    "SOCIOS": """
        CREATE TABLE IF NOT EXISTS "SOCIOS" (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            dni VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            fecha_inscripcion DATE NOT NULL,
            profesor_id INTEGER NULL,
            registra_deuda BOOLEAN NOT NULL DEFAULT FALSE,
            CONSTRAINT fk_socios_profesor
                FOREIGN KEY (profesor_id)
                REFERENCES "PROFESORES" (id)
                ON DELETE SET NULL
        )
    """,
    "SOCIO_CATEGORIA": """
        CREATE TABLE IF NOT EXISTS "SOCIO_CATEGORIA" (
            id SERIAL PRIMARY KEY,
            socio_id INTEGER NOT NULL,
            categoria_id INTEGER NOT NULL,
            CONSTRAINT fk_socio_categoria_socio
                FOREIGN KEY (socio_id)
                REFERENCES "SOCIOS" (id)
                ON DELETE CASCADE,
            CONSTRAINT fk_socio_categoria_categoria
                FOREIGN KEY (categoria_id)
                REFERENCES "CATEGORIAS" (id)
                ON DELETE CASCADE,
            PRIMARY KEY (socio_id, categoria_id)
        )
    """,
    "TURNOS": """
        CREATE TABLE IF NOT EXISTS "TURNOS" (
            id SERIAL PRIMARY KEY,
            cancha VARCHAR(50) NOT NULL,
            fecha DATE NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fin TIME NOT NULL,
            socio_reserva_id INTEGER NULL,
            estado VARCHAR(20) NOT NULL DEFAULT 'disponible',
            CONSTRAINT fk_turnos_socio
                FOREIGN KEY (socio_reserva_id)
                REFERENCES "SOCIOS" (id)
                ON DELETE SET NULL
        )
    """,
    "TURNO_JUGADORES": """
        CREATE TABLE IF NOT EXISTS "TURNO_JUGADORES" (
            id SERIAL PRIMARY KEY,
            turno_id INTEGER NOT NULL,
            jugador_nombre VARCHAR(100) NOT NULL,
            CONSTRAINT fk_turno_jugadores_turno
                FOREIGN KEY (turno_id)
                REFERENCES "TURNOS" (id)
                ON DELETE CASCADE
        )
    """,
    "ALUMNOS": """
        CREATE TABLE IF NOT EXISTS "ALUMNOS" (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            dni VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            fecha_inscripcion DATE NOT NULL,
            profesor_id INTEGER NULL,
            nivel VARCHAR(50),
            activo BOOLEAN NOT NULL DEFAULT TRUE,
            CONSTRAINT fk_alumnos_profesor
                FOREIGN KEY (profesor_id)
                REFERENCES "PROFESORES" (id)
                ON DELETE SET NULL
        )
    """,
    "PAGOS": """
        CREATE TABLE IF NOT EXISTS "PAGOS" (
            id SERIAL PRIMARY KEY,
            tipo VARCHAR(20) NOT NULL,
            monto NUMERIC(10,2) NOT NULL,
            fecha_pago DATE NOT NULL,
            mes INTEGER NOT NULL,
            anio INTEGER NOT NULL,
            socio_id INTEGER NULL,
            alumno_id INTEGER NULL,
            profesor_id INTEGER NULL,
            metodo_pago VARCHAR(50),
            observaciones TEXT,
            CONSTRAINT fk_pagos_socio
                FOREIGN KEY (socio_id)
                REFERENCES "SOCIOS" (id)
                ON DELETE SET NULL,
            CONSTRAINT fk_pagos_alumno
                FOREIGN KEY (alumno_id)
                REFERENCES "ALUMNOS" (id)
                ON DELETE SET NULL,
            CONSTRAINT fk_pagos_profesor
                FOREIGN KEY (profesor_id)
                REFERENCES "PROFESORES" (id)
                ON DELETE SET NULL
        )
    """,
    "PELOTITAS": """
        CREATE TABLE IF NOT EXISTS "PELOTITAS" (
            id SERIAL PRIMARY KEY,
            fecha DATE NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario NUMERIC(10,2) NOT NULL,
            total NUMERIC(10,2) NOT NULL,
            proveedor VARCHAR(200),
            comprador_tipo VARCHAR(20),
            comprador_id INTEGER,
            comprador_nombre VARCHAR(200),
            observaciones TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """,
}


def create_database():
    admin_config = DB_CONFIG | {"dbname": "postgres"}
    with psycopg2.connect(**admin_config) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
            if cursor.fetchone() is None:
                cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
                print(f"Base de datos {DB_NAME} creada correctamente.")
            else:
                print(f"Base de datos {DB_NAME} ya existe.")


def create_tables():
    db_config = DB_CONFIG | {"dbname": DB_NAME}
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            for table_name, ddl in TABLES.items():
                print(f"Creando tabla {table_name}: ", end="")
                cursor.execute(ddl)
                print("OK")

            cursor.execute('DROP TRIGGER IF EXISTS trg_pelotitas_updated_at ON "PELOTITAS"')
            cursor.execute('DROP FUNCTION IF EXISTS set_pelotitas_updated_at()')
            cursor.execute("""
                CREATE OR REPLACE FUNCTION set_pelotitas_updated_at()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql
            """)
            cursor.execute("""
                CREATE TRIGGER trg_pelotitas_updated_at
                BEFORE UPDATE ON "PELOTITAS"
                FOR EACH ROW
                EXECUTE FUNCTION set_pelotitas_updated_at()
            """)
            conn.commit()


if __name__ == "__main__":
    create_database()
    create_tables()