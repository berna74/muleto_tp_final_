# Django backend

Este directorio contiene un esqueleto Django sobre PostgreSQL y un script para migrar datos desde MySQL.

Pasos básicos:

1. Copiar `.env.example` a `.env` y completar credenciales.
2. Crear la base PostgreSQL con `python db_init.py` desde la raíz del proyecto.
3. Migrar los datos con `python backend/migrate_mysql_to_postgres.py`.
4. Validar el proyecto Django con `python backend/manage.py check`.