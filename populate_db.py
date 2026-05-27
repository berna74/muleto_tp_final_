#!/usr/bin/env python3
import os
import random
from pathlib import Path

import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
BACKEND_ENV = BASE_DIR / "backend" / ".env"
if BACKEND_ENV.exists():
    load_dotenv(BACKEND_ENV)
else:
    load_dotenv(BASE_DIR / ".env-dev")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "tienda"),
}

# Datos para generar registros realistas
nombres = ["Juan", "Carlos", "María", "Antonio", "Rosa", "Pedro", "Ana", "Javier", "Diego", "Elena",
           "Fernando", "Isabel", "Alejandro", "Martín", "Roberto", "Patricia", "Francisco", "Marta", "Manuel", "Beatriz",
           "José", "Carmen", "Miguel", "Francisca", "Rafael", "Amparo", "Andrés", "Dolores", "Luis", "Cecilia",
           "Jorge", "Encarnación", "Ramón", "Esperanza", "Guillermo", "Natividad", "Sergio", "Matilde", "Eduardo", "Herminia",
           "Víctor", "Rosario", "Pablo", "Soledad", "Enrique", "Virtudes", "Arturo", "Milagros", "Jesús", "Pascuala"]

apellidos = ["García", "Rodríguez", "Martínez", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores",
             "Rivera", "Gómez", "Díaz", "Reyes", "Cruz", "Morales", "Gutierrez", "Ortiz", "Jiménez", "Herrera",
             "Campos", "Romero", "Fuentes", "Rojas", "Cabrera", "Ocampo", "Vargas", "Castro", "Medina", "Vega",
             "Salas", "Parra", "Bravo", "Valenzuela", "Duran", "Pino", "Salazar", "Quintanilla", "Briones", "Valencia"]

categorias_nombres = ["Principiante", "Intermedio", "Avanzado", "Profesional", "Élite",
                      "Categoría A", "Categoría B", "Categoría C", "Categoría D", "Máster"]

canchas = ["Cancha 1", "Cancha 2", "Cancha 3", "Cancha 4", "Cancha 5"]

tipos_pelota = ["Práctica", "Competición", "Premium", "Importada", "Nacional"]

metodos_pago = ["Efectivo", "Tarjeta Débito", "Tarjeta Crédito", "Transferencia Bancaria", "Cheque"]

def random_nombre():
    return random.choice(nombres)

def random_apellido():
    return random.choice(apellidos)

def random_email(nombre, apellido, suffix=""):
    domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "example.com"]
    local_part = f"{nombre.lower()}.{apellido.lower()}"
    if suffix:
        local_part = f"{local_part}.{suffix}"
    return f"{local_part}@{random.choice(domains)}"

def random_telefono():
    return f"29{random.randint(10000000, 99999999)}"

def unique_dni(prefix, index):
    return f"{prefix}{index:05d}"

def random_date(start_year=2020, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def populate_categorias(conn):
    print("Insertando categorías...")
    cursor = conn.cursor()
    for i, nombre in enumerate(categorias_nombres[:10]):
        descripcion = f"Descripción de {nombre}"
        cursor.execute(
            'INSERT INTO "CATEGORIAS" (nombre, descripcion) VALUES (%s, %s)',
            (nombre, descripcion)
        )
    
    # Agregar 40 más
    for i in range(40):
        nombre = f"Categoría Especial {i+1}"
        descripcion = f"Descripción de categoría especial {i+1}"
        cursor.execute(
            'INSERT INTO "CATEGORIAS" (nombre, descripcion) VALUES (%s, %s)',
            (nombre, descripcion)
        )
    
    conn.commit()
    print("✓ 50 categorías insertadas")

def populate_profesores(conn):
    print("Insertando profesores...")
    cursor = conn.cursor()
    profesores_ids = []
    
    for i in range(50):
        nombre = random_nombre()
        apellido = random_apellido()
        dni = unique_dni("PROF", i + 1)
        email = random_email(nombre, apellido, f"prof{i + 1}")
        telefono = random_telefono()
        horarios = f"Lunes a Viernes, 10:00-18:00"
        
        cursor.execute(
            'INSERT INTO "PROFESORES" (nombre, apellido, dni, email, telefono, horarios_clases) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            (nombre, apellido, dni, email, telefono, horarios)
        )
        prof_id = cursor.fetchone()[0]
        profesores_ids.append(prof_id)
    
    conn.commit()
    print(f"✓ 50 profesores insertados")
    return profesores_ids

def populate_socios(conn, profesores_ids):
    print("Insertando socios...")
    cursor = conn.cursor()
    socios_ids = []
    
    for i in range(50):
        nombre = random_nombre()
        apellido = random_apellido()
        dni = unique_dni("SOC", i + 1)
        email = random_email(nombre, apellido, f"socio{i + 1}")
        telefono = random_telefono()
        fecha_inscripcion = random_date().date()
        profesor_id = random.choice(profesores_ids) if profesores_ids else None
        registra_deuda = random.choice([True, False])
        
        cursor.execute(
            'INSERT INTO "SOCIOS" (nombre, apellido, dni, email, telefono, fecha_inscripcion, profesor_id, registra_deuda) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
            (nombre, apellido, dni, email, telefono, fecha_inscripcion, profesor_id, registra_deuda)
        )
        socio_id = cursor.fetchone()[0]
        socios_ids.append(socio_id)
    
    conn.commit()
    print(f"✓ 50 socios insertados")
    return socios_ids

def populate_socio_categoria(conn, socios_ids):
    print("Insertando relaciones socio-categoría...")
    cursor = conn.cursor()
    
    # Obtener todas las categorías
    cursor.execute('SELECT id FROM "CATEGORIAS"')
    categorias_ids = [row[0] for row in cursor.fetchall()]
    
    count = 0
    for index, socio_id in enumerate(socios_ids):
        if not categorias_ids:
            break
        categoria_id = categorias_ids[index % len(categorias_ids)]
        cursor.execute(
            'INSERT INTO "SOCIO_CATEGORIA" (socio_id, categoria_id) VALUES (%s, %s)',
            (socio_id, categoria_id)
        )
        count += 1
    
    conn.commit()
    print(f"✓ {count} relaciones socio-categoría insertadas")

def populate_alumnos(conn, profesores_ids):
    print("Insertando alumnos...")
    cursor = conn.cursor()
    alumnos_ids = []
    
    for i in range(50):
        nombre = random_nombre()
        apellido = random_apellido()
        dni = unique_dni("ALU", i + 1)
        email = random_email(nombre, apellido, f"alumno{i + 1}")
        telefono = random_telefono()
        fecha_inscripcion = random_date().date()
        profesor_id = random.choice(profesores_ids) if profesores_ids else None
        nivel = random.choice(["Principiante", "Intermedio", "Avanzado"])
        activo = random.choice([True, False])
        
        cursor.execute(
            'INSERT INTO "ALUMNOS" (nombre, apellido, dni, email, telefono, fecha_inscripcion, profesor_id, nivel, activo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
            (nombre, apellido, dni, email, telefono, fecha_inscripcion, profesor_id, nivel, activo)
        )
        alumno_id = cursor.fetchone()[0]
        alumnos_ids.append(alumno_id)
    
    conn.commit()
    print(f"✓ 50 alumnos insertados")
    return alumnos_ids

def populate_turnos(conn, socios_ids):
    print("Insertando turnos...")
    cursor = conn.cursor()
    turnos_ids = []
    
    for i in range(50):
        cancha = random.choice(canchas)
        fecha = (datetime.now() + timedelta(days=random.randint(1, 30))).date()
        hora_inicio = f"{random.randint(9, 18):02d}:00:00"
        hora_fin = f"{random.randint(10, 19):02d}:00:00"
        socio_reserva_id = random.choice(socios_ids) if socios_ids else None
        estado = random.choice(["disponible", "reservado", "ocupado", "cancelado"])
        
        cursor.execute(
            'INSERT INTO "TURNOS" (cancha, fecha, hora_inicio, hora_fin, socio_reserva_id, estado) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            (cancha, fecha, hora_inicio, hora_fin, socio_reserva_id, estado)
        )
        turno_id = cursor.fetchone()[0]
        turnos_ids.append(turno_id)
    
    conn.commit()
    print(f"✓ 50 turnos insertados")
    return turnos_ids

def populate_turno_jugadores(conn, turnos_ids):
    print("Insertando jugadores en turnos...")
    cursor = conn.cursor()
    
    count = 0
    
    for index, turno_id in enumerate(turnos_ids):
        jugador_nombre = f"{random_nombre()} {random_apellido()} {index + 1}"
        cursor.execute(
            'INSERT INTO "TURNO_JUGADORES" (turno_id, jugador_nombre) VALUES (%s, %s)',
            (turno_id, jugador_nombre)
        )
        count += 1
    
    conn.commit()
    print(f"✓ {count} jugadores en turnos insertados")

def populate_pagos(conn, socios_ids, alumnos_ids, profesores_ids):
    print("Insertando pagos...")
    cursor = conn.cursor()
    
    for i in range(50):
        tipo = random.choice(["Cuota", "Clase", "Torneo", "Alquiler"])
        monto = round(random.uniform(100, 5000), 2)
        fecha_pago = random_date().date()
        mes = random.randint(1, 12)
        anio = random.randint(2023, 2026)
        socio_id = random.choice(socios_ids) if socios_ids else None
        alumno_id = random.choice(alumnos_ids) if alumnos_ids else None
        profesor_id = random.choice(profesores_ids) if profesores_ids else None
        metodo_pago = random.choice(metodos_pago)
        observaciones = f"Pago de {tipo} de {mes}/{anio}"
        
        cursor.execute(
            'INSERT INTO "PAGOS" (tipo, monto, fecha_pago, mes, anio, socio_id, alumno_id, profesor_id, metodo_pago, observaciones) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (tipo, monto, fecha_pago, mes, anio, socio_id, alumno_id, profesor_id, metodo_pago, observaciones)
        )
    
    conn.commit()
    print(f"✓ 50 pagos insertados")

def populate_pelotitas(conn):
    print("Insertando pelotitas...")
    cursor = conn.cursor()
    
    for i in range(50):
        fecha = random_date().date()
        tipo = random.choice(tipos_pelota)
        cantidad = random.randint(1, 100)
        precio_unitario = round(random.uniform(50, 500), 2)
        total = round(cantidad * precio_unitario, 2)
        proveedor = random.choice(["Proveedor A", "Proveedor B", "Proveedor C", "Importadora Local"])
        comprador_tipo = random.choice(["socio", "alumno", "profesor", "admin"])
        comprador_id = random.randint(1, 50)
        comprador_nombre = f"{random_nombre()} {random_apellido()}"
        observaciones = f"Compra de {cantidad} pelotitas {tipo}"
        
        cursor.execute(
            'INSERT INTO "PELOTITAS" (fecha, tipo, cantidad, precio_unitario, total, proveedor, comprador_tipo, comprador_id, comprador_nombre, observaciones, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (fecha, tipo, cantidad, precio_unitario, total, proveedor, comprador_tipo, comprador_id, comprador_nombre, observaciones, datetime.now(), datetime.now())
        )
    
    conn.commit()
    print(f"✓ 50 pelotitas insertadas")

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conectado a la base de datos")
        
        # Vaciar las tablas para empezar de cero
        cursor = conn.cursor()
        cursor.execute(
            'TRUNCATE TABLE "TURNO_JUGADORES", "SOCIO_CATEGORIA", "PAGOS", "TURNOS", "ALUMNOS", "SOCIOS", "PROFESORES", "PELOTITAS", "CATEGORIAS" RESTART IDENTITY CASCADE'
        )
        conn.commit()
        print("✓ Tablas vaciadas")
        
        # Poblar tablas en orden de dependencias
        populate_categorias(conn)
        profesores_ids = populate_profesores(conn)
        socios_ids = populate_socios(conn, profesores_ids)
        populate_socio_categoria(conn, socios_ids)
        alumnos_ids = populate_alumnos(conn, profesores_ids)
        turnos_ids = populate_turnos(conn, socios_ids)
        populate_turno_jugadores(conn, turnos_ids)
        populate_pagos(conn, socios_ids, alumnos_ids, profesores_ids)
        populate_pelotitas(conn)
        
        print("\n✓ ¡Base de datos completamente poblada con 50 ejemplos en cada tabla!")
        
        conn.close()
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
