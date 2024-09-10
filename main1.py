from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sqlite3
import moduloPreguntas
from CreaacionEmbedingPDF import creacionEmbeding
from editkey import crearapikey

app = Flask(__name__)
CORS(app)

# Ruta de la carpeta donde se guardarán las imágenes
UPLOAD_FOLDER = 'src'
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
DB_PATH = 'mi_base_de_datos.db'  # Ruta de la base de datos SQLite

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Función para verificar extensión de archivos
def allowed_file_extension(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower() in ALLOWED_EXTENSIONS

# Función para obtener el siguiente ID disponible
def get_next_id():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM objetos')
    max_id = cursor.fetchone()[0]
    conn.close()
    return (max_id + 1) if max_id else 1


# Rutas originales del primer proyecto
@app.route('/')
def root():
    return "root"

@app.route('/crear', methods=['GET'])
def crear_pregunta():
    respuesta = creacionEmbeding()
    return jsonify({"respuesta": respuesta})

@app.route('/pregunta', methods=['POST'])
def recibir_pregunta():
    data = request.get_json()
    pregunta = data.get('pregunta')
    respuestatotal = moduloPreguntas.preguntamod(pregunta)
    respuesta = respuestatotal[0].replace("\n\n", "").replace("\"", "")
    contextoRelacioado = respuestatotal[1]
    return jsonify({"respuesta": respuesta, "contexto": contextoRelacioado})

@app.route('/apikey', methods=['POST'])
def crearkey():
    data = request.get_json()
    key = data.get('api_key')
    afuera = crearapikey(key)
    return jsonify({"respuesta": afuera})


# Funcionalidades de subida y gestión de imágenes/objetos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files or 'name' not in request.form or 'description' not in request.form:
        return jsonify({"error": "Faltan parámetros"}), 400

    file = request.files['image']
    name = request.form['name']
    description = request.form['description']
    password = request.form['password']

    # Verificar la contraseña
    if password != "jasfj123jasdl":
        return jsonify({"error": "Contraseña incorrecta"}), 403
    _, file_extension = os.path.splitext(file.filename)

    if not allowed_file_extension(file.filename):
        return jsonify({"error": "Formato incompatible. Solo se aceptan jpg y png"}), 400

    new_id = get_next_id()
    new_filename = f"{new_id}{file_extension.lower()}"
    filepath = os.path.join(UPLOAD_FOLDER, new_filename)

    file.save(filepath)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO objetos (id, nombre, descripcion, foto) VALUES (?, ?, ?, ?)', 
                   (new_id, name, description, new_filename))
    conn.commit()
    conn.close()

    return jsonify({"message": "Objeto creado y archivo guardado correctamente", "id": new_id}), 200

@app.route('/delete/<int:id>', methods=['POST'])
def delete_object(id):
    # Leer el JSON enviado en la solicitud
    data = request.get_json()

    # Verificar que el parámetro 'password' esté presente en el JSON
    if not data or 'password' not in data:
        return jsonify({"error": "Faltan parámetros"}), 400

    password = data['password']

    # Verificar si la contraseña es correcta
    if password != "jasfj123jasdl":
        return jsonify({"error": "Contraseña incorrecta"}), 403

    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificar si el objeto existe y obtener la foto
    cursor.execute('SELECT foto FROM objetos WHERE id = ?', (id,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return jsonify({"error": "Objeto no encontrado"}), 404

    filename = record[0]
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Si el archivo existe, eliminarlo
    if os.path.exists(filepath):
        os.remove(filepath)

    # Eliminar el registro de la base de datos
    cursor.execute('DELETE FROM objetos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Objeto con id {id} y su imagen han sido eliminados"}), 200



@app.route('/getall', methods=['GET'])
def get_all_objects():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objetos')
    objects = cursor.fetchall()
    conn.close()
    return jsonify(objects), 200

@app.route('/get/<int:id>', methods=['GET'])
def get_object(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objetos WHERE id = ?', (id,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return jsonify({"error": "Objeto no encontrado"}), 404

    foto_path = os.path.join(UPLOAD_FOLDER, record[3])
    conn.close()
    return jsonify({"id": record[0], "nombre": record[1], "descripcion": record[2], "foto": record[3], "foto_url": foto_path}), 200

@app.route('/getpicture/<int:id>', methods=['GET'])
def get_picture(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objetos WHERE id = ?', (id,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return jsonify({"error": "Objeto no encontrado"}), 404

    foto_path = os.path.join(UPLOAD_FOLDER, record[3])
    conn.close()

    if os.path.exists(foto_path):
        return send_file(foto_path, mimetype='image/jpeg', as_attachment=False, download_name=record[3])
    else:
        return jsonify({"error": "Archivo de imagen no encontrado"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
