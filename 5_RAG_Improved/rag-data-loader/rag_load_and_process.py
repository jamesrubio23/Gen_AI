import os

from dotenv import load_dotenv

#from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales y otros valores desde el archivo .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Crear el loader para cargar los documentos PDF
#hemos cambaido ademas la direccion apra que funcione mejor
loader = DirectoryLoader(
    os.path.abspath("../v1-166-part5/pdf-documents"), 
    glob="**/*.pdf",
    use_multithreading=True,
    show_progress=True,
    max_concurrency=50,
    loader_cls=UnstructuredPDFLoader,
)
docs = loader.load()

# Cargar el modelo de OpenAI para embeddings
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)

# Dividir los documentos en chunks semánticos
text_splitter = SemanticChunker(embeddings=embeddings)

flattened_docs = [doc[0] for doc in docs if doc]
chunks = text_splitter.split_documents(flattened_docs)

# Conectar a la base de datos PostgreSQL utilizando pgvector
PGVector.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="collection164",
    connection_string=f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    pre_delete_collection=True,
)