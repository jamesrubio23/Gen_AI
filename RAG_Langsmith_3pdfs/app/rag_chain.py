import os
from operator import itemgetter
from typing import TypedDict

from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Configurar el vector store utilizando las variables de entorno
vector_store = PGVector(
    collection_name="collection164",
    connection_string=f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    embedding_function=OpenAIEmbeddings()
)

template = """
Answer given the following context:
{context}

Question: {question}
"""

ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

# Utilizando el modelo GPT con la configuración de temperatura y el modelo gpt-4-1106-preview
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', streaming=True)

class RagInput(TypedDict):
    question: str

# Definir la cadena final del proceso RAG
final_chain = (
    {
    "context": (itemgetter("question") | vector_store.as_retriever()),
    "question": itemgetter("question")
    }
    | ANSWER_PROMPT
    | llm
    | StrOutputParser()
).with_types(input_type=RagInput)