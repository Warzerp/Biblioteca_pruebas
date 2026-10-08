import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(user='postgres', password='Mauro_1906', host='localhost', port='5432')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Force disconnect other clients to drop it
    cursor.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'LibreriaDesarrolloDB'
          AND pid <> pg_backend_pid();
    """)
    
    cursor.execute('DROP DATABASE IF EXISTS "LibreriaDesarrolloDB"')
    cursor.execute('CREATE DATABASE "LibreriaDesarrolloDB"')
    
    cursor.close()
    conn.close()
    print('Database recreated successfully.')
except Exception as e:
    print('Error:', e)

