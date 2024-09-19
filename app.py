from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://seiferwolfdragon_user:2AEhHHC8WUkMrN4U7NZvInl8HPkVIKUj@dpg-crd2t0rv2p9s73det5i0-a.oregon-postgres.render.com/seiferwolfdragon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo de la tabla 'estudiantes'
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=True)
    ap_paterno = db.Column(db.String, nullable=True)
    ap_materno = db.Column(db.String, nullable=True)
    semestre = db.Column(db.Integer, nullable=True)

# Verificar si la tabla 'estudiantes' existe y crearla si no existe
with app.app_context():
    # Crea la tabla si no existe
    db.create_all()

# Endpoint para obtener todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    estudiantes = Estudiante.query.all()
    lista_estudiantes = []
    for estudiante in estudiantes:
        lista_estudiantes.append({
            'no_control': estudiante.no_control,
            'nombre': estudiante.nombre,
            'ap_paterno': estudiante.ap_paterno,
            'ap_materno': estudiante.ap_materno,
            'semestre': estudiante.semestre
        })
    return jsonify(lista_estudiantes)

@app.route("/", methods=['GET'])
def holamundo():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
# Endpoint para agregar un nuevo estudiante
@app.route('/estudiantes', methods=['POST'])
def agregar_estudiante():
    data = request.get_json()
    nuevo_estudiante = Estudiante(
        no_control=data['no_control'],
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        semestre=data['semestre']
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante agregado exitosamente'}), 201

# Endpoint para obtener un estudiante por no_control
@app.route('/estudiantes/<no_control>', methods=['GET'])
def obtener_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    return jsonify({
        'no_control': estudiante.no_control,
        'nombre': estudiante.nombre,
        'ap_paterno': estudiante.ap_paterno,
        'ap_materno': estudiante.ap_materno,
        'semestre': estudiante.semestre
    })

# Endpoint para actualizar un estudiante
@app.route('/estudiantes/<no_control>', methods=['PUT'])
def actualizar_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    data = request.get_json()
    estudiante.nombre = data['nombre']
    estudiante.ap_paterno = data['ap_paterno']
    estudiante.ap_materno = data['ap_materno']
    estudiante.semestre = data['semestre']
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante actualizado exitosamente'})

# Endpoint para eliminar un estudiante
@app.route('/estudiantes/<no_control>', methods=['DELETE'])
def eliminar_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    db.session.delete(estudiante)
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante eliminado exitosamente'})

if __name__ == '__main__':
    app.run(debug=True)
