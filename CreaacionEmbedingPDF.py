from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores.faiss import FAISS

def creacionEmbeding():
    pdf_file_obj = open('museo.pdf', 'rb')
    #pdf_file_obj = open('museo.pdf', 'rb')
    pdf_reader = PdfReader(pdf_file_obj)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    #print(text[8000:10000])

    #crear chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=70,
        length_function=len
        )
    chunks = text_splitter.split_text(text)
    print(len(chunks))
    # descargar modelo de embedding
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    print("llego bien")

    #pruebas de embddings
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    # fin de la prueba
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    #print(docs)


    import os
    import pickle

    # Obtener la ruta del directorio donde se encuentra el archivo .py
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Ruta del archivo .pkl
    pkl_path = os.path.join(script_dir, 'knowledge_base.pkl')

    # Guardar el objeto knowledge_base en un archivo
    with open(pkl_path, 'wb') as f:
        pickle.dump(knowledge_base, f)
    return 'knowledge_base.pkl'

