from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clave secreta para mensajes flash

# Credenciales de la base de datos (puedes ajustarlas para usar variables de entorno)
DB_HOST = os.getenv("DB_HOST", "dpg-crd2t0rv2p9s73det5i0-a.oregon-postgres.render.com")
DB_NAME = os.getenv("DB_NAME", "seiferwolfdragon")
DB_USER = os.getenv("DB_USER", "seiferwolfdragon_user")
DB_PASS = os.getenv("DB_PASS", "2AEhHHC8WUkMrN4U7NZvInl8HPkVIKUj")

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

@app.route('/')
def index():
    """Página principal que lista todos los empleados"""
    conn = connect()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM empleados")
            empleados = cur.fetchall()
        conn.close()
        return render_template('index.html', empleados=empleados)
    return "Error al conectar a la base de datos."

@app.route('/create', methods=['POST'])
def create():
    """Crear un nuevo empleado"""
    nombre = request.form['nombre']
    cargo = request.form['cargo']
    conn = connect()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO empleados (nombre, cargo) VALUES (%s, %s)
            """, (nombre, cargo))
            conn.commit()
        conn.close()
        flash("Empleado creado exitosamente.")
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    """Actualizar un empleado"""
    nombre = request.form['nombre']
    cargo = request.form['cargo']
    conn = connect()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE empleados SET nombre=%s, cargo=%s WHERE id=%s
            """, (nombre, cargo, id))
            conn.commit()
        conn.close()
        flash("Empleado actualizado exitosamente.")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Eliminar un empleado"""
    conn = connect()
    if conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM empleados WHERE id=%s", (id,))
            conn.commit()
        conn.close()
        flash("Empleado eliminado exitosamente.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
