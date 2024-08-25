import os
import pickle
import json
from openai import OpenAI
def pregunta(pregunta):
    # Obtener la ruta del directorio donde se encuentra el archivo .py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Ruta del archivo .pkl
    pkl_path = os.path.join(script_dir, 'knowledge_base.pkl')
    # Cargar el objeto knowledge_base desde el archivo
    with open(pkl_path, 'rb') as f:
        knowledge_base = pickle.load(f)

    #pregunta = "¿Qué es CAPRN?"
    docs = knowledge_base.similarity_search(pregunta, 3)
    doc_contents = [doc.page_content for doc in docs]

    with open('key.json', 'r') as file:
        config = json.load(file)
        api_key = config['api_key']

    cliente = OpenAI(api_key=api_key)
    menssages= [
        {"role":"system", "content": " ".join(doc_contents)}
    ]
    menssages.append({"role":"user","content": pregunta})
    completion = cliente.chat.completions.create(
        model="gpt-4o-mini",
        #model="gpt-3.5-turbo",
        messages= menssages,
    )
    assistant_response= completion.choices[0].message.content
    return assistant_response


def preguntatest(pregunta):
    # Obtener la ruta del directorio donde se encuentra el archivo .py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Ruta del archivo .pkl
    pkl_path = os.path.join(script_dir, 'knowledge_base.pkl')
    # Cargar el objeto knowledge_base desde el archivo
    with open(pkl_path, 'rb') as f:
        knowledge_base = pickle.load(f)

    #pregunta = "¿Qué es CAPRN?"
    docs = knowledge_base.similarity_search(pregunta, 3)
    doc_contents = [doc.page_content for doc in docs]

    with open('key.json', 'r') as file:
        config = json.load(file)
        #api_key = config['api_key']

    #cliente = OpenAI(api_key=api_key)
    menssages= [
        {"role":"system", "content": " ".join(doc_contents)}
    ]
    menssages.append({"role":"user","content": pregunta})


    return "hey todo funciona bien no hay necesidad de detener el audio"

#print(pregunta("¿Qué es CAPRN?"))