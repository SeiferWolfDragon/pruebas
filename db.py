import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        dsn="postgresql://seifer_user:Sgmhes2MczbBDLDkp4OQvdU8GSUnNleI@dpg-ct2li59u0jms738sichg-a.oregon-postgres.render.com/dbalumnos",
        cursor_factory=RealDictCursor  # Devuelve los resultados como diccionarios
    )
