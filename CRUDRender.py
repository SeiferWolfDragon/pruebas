import psycopg2
from psycopg2 import sql

# Credenciales para la base de datos
DB_HOST = "dpg-crd2t0rv2p9s73det5i0-a.oregon-postgres.render.com"
DB_NAME = "seiferwolfdragon"
DB_USER = "seiferwolfdragon_user"
DB_PASS = "2AEhHHC8WUkMrN4U7NZvInl8HPkVIKUj"

def connect():
    """Conecta a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None

def create_table():
    """Crea una tabla si no existe"""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100),
                    cargo VARCHAR(100)
                )
                """)
                conn.commit()
                print("Tabla creada o ya existe.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            conn.close()

def create_empleado(nombre, cargo):
    """Inserta un nuevo empleado"""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO empleados (nombre, cargo) VALUES (%s, %s)
                """, (nombre, cargo))
                conn.commit()
                print("Empleado agregado.")
        except Exception as e:
            print(f"Error al agregar el empleado: {e}")
        finally:
            conn.close()

def read_empleados():
    """Lee todos los empleados"""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM empleados")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        except Exception as e:
            print(f"Error al leer los empleados: {e}")
        finally:
            conn.close()

def update_empleado(id, nombre, cargo):
    """Actualiza un empleado"""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE empleados SET nombre=%s, cargo=%s WHERE id=%s
                """, (nombre, cargo, id))
                conn.commit()
                print("Empleado actualizado.")
        except Exception as e:
            print(f"Error al actualizar el empleado: {e}")
        finally:
            conn.close()

def delete_empleado(id):
    """Elimina un empleado"""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM empleados WHERE id=%s", (id,))
                conn.commit()
                print("Empleado eliminado.")
        except Exception as e:
            print(f"Error al eliminar el empleado: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    # Ejemplo de uso
    #create_table()  # Crea la tabla si no existe
    create_empleado("Seifer", "Ingeniero")
    create_empleado("Were", "guardaespaldas")
    create_empleado("Rufus", "ingeniero")
    read_empleados()
    #delete_empleado(1)
