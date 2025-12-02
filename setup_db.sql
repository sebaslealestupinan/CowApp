-- Copia y pega estos comandos en tu SQL Shell (psql) o pgAdmin

-- 1. Crear el usuario (si no existe)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'SebasLealE') THEN

      CREATE ROLE "SebasLealE" LOGIN PASSWORD 'primerDotenv';
   END IF;
END
$do$;

-- 2. Crear la base de datos
-- Nota: Si esto falla porque la base de datos ya existe, ignora el error.
SELECT 'CREATE DATABASE cow_app OWNER "SebasLealE"'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cow_app')\gexec

-- 3. Dar permisos (opcional si ya es dueño)
GRANT ALL PRIVILEGES ON DATABASE cow_app TO "SebasLealE";
