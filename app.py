from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Configuración de la conexión a la base de datos
def get_connection():
    return pymysql.connect(
        host='157.230.225.207',
        user='root',
        password='chuleta',
        database='CETECH',
        port=3308,
        cursorclass=pymysql.cursors.DictCursor
    )

# Rutas de la API
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos")
            alumnos = cursor.fetchall()
        return jsonify(alumnos)
    finally:
        connection.close()

@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos WHERE id = %s", (id,))
            alumno = cursor.fetchone()
        if alumno:
            return jsonify(alumno)
        else:
            return jsonify({"message": "Alumno no encontrado"}), 404
    finally:
        connection.close()

@app.route('/alumnos', methods=['POST'])
def create_alumno():
    data = request.get_json()
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO alumnos (no_control, nombre, apeP, apeM, semestre) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (data['no_control'], data['nombre'], data['apeP'], data['apeM'], data['semestre']))
            connection.commit()
        return jsonify({"message": "Alumno creado correctamente"}), 201
    finally:
        connection.close()

@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    data = request.get_json()
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
            UPDATE alumnos 
            SET no_control = %s, nombre = %s, apeP = %s, apeM = %s, semestre = %s 
            WHERE id = %s
            """
            cursor.execute(sql, (data['no_control'], data['nombre'], data['apeP'], data['apeM'], data['semestre'], id))
            connection.commit()
        return jsonify({"message": "Alumno actualizado correctamente"})
    finally:
        connection.close()

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM alumnos WHERE id = %s", (id,))
            connection.commit()
        return jsonify({"message": "Alumno eliminado correctamente"})
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
