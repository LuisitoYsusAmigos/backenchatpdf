from flask import Flask, jsonify, request
from flask_cors import CORS
import moduloPreguntas
from CreaacionEmbedingPDF import creacionEmbeding

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return "root"


@app.route('/crear', methods=['GET'])
def crear_pregunta():
    respuesta =creacionEmbeding()
    
    

    # Respuesta que incluye la pregunta recibida
    

    # Devuelve la respuesta como JSON
    return jsonify({"respuesta": respuesta
                    #,"pregunta": pregunta
                    })



@app.route('/pregunta', methods=['POST'])
def recibir_pregunta():
    # Obtener el string 'pregunta' del cuerpo de la solicitud
    data = request.get_json()  # Si estás enviando un JSON
    pregunta = data.get('pregunta')
    
    # Procesar la pregunta usando tu módulo
    # respuesta = moduloPreguntas.preguntatest(pregunta)
    respuesta = moduloPreguntas.pregunta(pregunta)

    # Respuesta que incluye la pregunta recibida
    respuesta = f"{respuesta}"

    # Devuelve la respuesta como JSON
    return jsonify({"respuesta": respuesta
                    #,"pregunta": pregunta
                    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
