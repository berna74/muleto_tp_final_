import os

import mysql.connector
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql


load_dotenv()

SOURCE_CONFIG = {
    "host": os.getenv("SOURCE_DB_HOST", os.getenv("DB_HOST", "localhost")),
    "user": os.getenv("SOURCE_DB_USER", os.getenv("DB_USER", "root")),
    "password": os.getenv("SOURCE_DB_PASSWORD", os.getenv("DB_PASSWORD", "")),
    "database": os.getenv("SOURCE_DB_NAME", os.getenv("MYSQL_DB_NAME", "tienda")),
    "port": int(os.getenv("SOURCE_DB_PORT", os.getenv("DB_PORT", 3306))),
}

TARGET_CONFIG = {
    "host": os.getenv("TARGET_DB_HOST", os.getenv("DB_HOST", "localhost")),
    "user": os.getenv("TARGET_DB_USER", os.getenv("DB_USER", "postgres")),
    "password": os.getenv("TARGET_DB_PASSWORD", os.getenv("DB_PASSWORD", "")),
    "dbname": os.getenv("TARGET_DB_NAME", os.getenv("DB_NAME", "tienda")),
    "port": int(os.getenv("TARGET_DB_PORT", os.getenv("DB_PORT", 5432))),
}

TABLE_ORDER = [
    ("CATEGORIAS", ["id", "nombre", "descripcion"]),
    ("PROFESORES", ["id", "nombre", "apellido", "horarios_clases", "telefono", "email"]),
    ("SOCIOS", ["id", "nombre", "apellido", "dni", "email", "telefono", "fecha_inscripcion", "profesor_id", "registra_deuda"]),
    ("ALUMNOS", ["id", "nombre", "apellido", "dni", "email", "telefono", "fecha_inscripcion", "profesor_id", "nivel", "activo"]),
    ("TURNOS", ["id", "cancha", "fecha", "hora_inicio", "hora_fin", "socio_reserva_id", "estado"]),
    ("TURNO_JUGADORES", ["id", "turno_id", "jugador_nombre"]),
    ("PAGOS", ["id", "tipo", "monto", "fecha_pago", "mes", "anio", "socio_id", "alumno_id", "profesor_id", "metodo_pago", "observaciones"]),
    ("PELOTITAS", ["id", "fecha", "tipo", "cantidad", "precio_unitario", "total", "proveedor", "comprador_tipo", "comprador_id", "comprador_nombre", "observaciones", "created_at", "updated_at"]),
    ("SOCIO_CATEGORIA", ["socio_id", "categoria_id"]),
]


def copy_table(source_cursor, target_cursor, table_name, columns):
    source_cursor.execute(f'SELECT {", ".join(columns)} FROM `{table_name}`')
    rows = source_cursor.fetchall()
    if not rows:
        print(f"{table_name}: sin registros")
        return

    insert_sql = sql.SQL(
        "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
    ).format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(", ").join(sql.Identifier(column) for column in columns),
        placeholders=sql.SQL(", ").join(sql.Placeholder() for _ in columns),
    )

    for row in rows:
        target_cursor.execute(insert_sql, row)

    if "id" in columns:
        target_cursor.execute(
            sql.SQL(
                "SELECT setval(pg_get_serial_sequence(%s, 'id'), COALESCE((SELECT MAX(id) FROM {table}), 1), true)"
            ).format(table=sql.Identifier(table_name)),
            (table_name,),
        )

    print(f"{table_name}: {len(rows)} registros copiados")


def main():
    source_conn = mysql.connector.connect(**SOURCE_CONFIG)
    target_conn = psycopg2.connect(**TARGET_CONFIG)

    try:
        source_cursor = source_conn.cursor()
        target_cursor = target_conn.cursor()

        for table_name, columns in TABLE_ORDER:
            copy_table(source_cursor, target_cursor, table_name, columns)

        target_conn.commit()
        print("Migración completada")
    except Exception:
        target_conn.rollback()
        raise
    finally:
        source_conn.close()
        target_conn.close()


if __name__ == "__main__":
    main()