# routers/rag_qa.py
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

# 1. Carga las variables de entorno desde .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY no encontrada en las variables de entorno")

# 2. Configura tu router
routerRAG = APIRouter()

# 3. Configura embeddings y carga el vector store persistido
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(
    collection_name="Strategy_articles",
    persist_directory="./Strategy_Chroma_db",  # Ajusta al nombre correcto de tu carpeta
    embedding_function=embeddings,
)

# 4. Configura tu LLM usando la API key (no usar llm(...) directo)
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0,
    max_tokens=600,
    openai_api_key=OPENAI_API_KEY
)

# 5. Prompt que restringe al contexto
prompt = ChatPromptTemplate.from_messages([
    'human','Mi nombre es {name}',
    'system','Acuta cómo un profesor experto en estrategia. Responde de manera sencilla, y pedagógica en cada una de las preguntas. Ejemplifica en caso de que sea necesario. No respondas nada que no tengas en tu base de conociminto que es {context}. Si la respuesta NO esta en tu base de conocimiento, entrega la siguiente respuesta: "No tengo información asociada a este tema, soy un experto en estrategia" NUNCA respondas usando tu conocimiento, ya que no estás programado para ello. Usa el {name} de la persona para dar una respuesta más personalizada',
    'human','{text}'
])



# 6. Crea un LLMChain para ejecutar el prompt
chain = prompt | llm | StrOutputParser()
#chain = LLMChain(llm=llm, prompt=prompt)

@routerRAG.get("/ask", tags=["RAG"])
def ask_question(name: str, question: str):
    """
    Endpoint que responde usando solo la base vectorial.
    Devuelve tanto la respuesta como los documentos fuente.
    """
    try:
        # Debug: imprimir la pregunta recibida
        print(f"[RAG] Query: {question}")

        # 1) Recuperar los top-3 documentos más relevantes
        docs = vectorstore.similarity_search(question, k=3)
        print(f"[RAG] Documentos recuperados: {len(docs)}")
        if not docs:
            return {
                "answer": "Lo siento, no dispongo de esa información en la base de datos.",
                "sources": []
            }

        # 2) Construir el contexto concatenando los contenidos
        context = "\n\n".join(doc.page_content for doc in docs)

        # 3) Generar la respuesta usando Chains
        answer = chain.invoke({'name':name,'context':context, 'text':question})

        # 4) Preparar los metadatos de las fuentes
        sources = []
        for doc in docs:
            meta = doc.metadata or {}
            sources.append({
                "source": meta.get("source", ""),
                "page": meta.get("page", None),
                "snippet": doc.page_content[:200]
            })

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
