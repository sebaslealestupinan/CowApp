import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

# Get credentials from .env
# We need to connect to 'postgres' db first to create the new db
user = os.getenv("DATABASE_USER", "SebasLealE") # Fallback or parse from URL
password = os.getenv("DATABASE_PASSWORD", "primerDotenv")
host = os.getenv("DATABASE_HOST", "localhost")
port = os.getenv("DATABASE_PORT", "5432")
dbname = "cow_app"

# Parse DATABASE_URL if available
database_url = os.getenv("DATABASE_URL")
if database_url:
    # Basic parsing logic or just use the hardcoded ones if they match
    pass

try:
    # Connect to default 'postgres' database
    con = psycopg2.connect(dbname='postgres', user='SebasLealE', host='localhost', password='primerDotenv')
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    
    # Check if db exists
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
    exists = cur.fetchone()
    
    if not exists:
        cur.execute(f"CREATE DATABASE {dbname}")
        print(f"Database {dbname} created successfully.")
    else:
        print(f"Database {dbname} already exists.")
        
    cur.close()
    con.close()
except Exception as e:
    print(f"Error creating database: {e}")
