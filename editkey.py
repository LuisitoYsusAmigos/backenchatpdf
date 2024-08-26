import os
import json

# Nombre del archivo JSON
def crearapikey(key):

    filename = 'key.json'

    # Verifica si el archivo ya existe y lo elimina
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} eliminado.")

    # Datos a escribir en el archivo JSON
    data = {
        "api_key": key
    }

    # Crea y escribe el archivo JSON
    with open(filename, 'w') as file:
        json.dump(data, file)
        print(f"{filename} creado con éxito.")
        return "creado con éxito"


