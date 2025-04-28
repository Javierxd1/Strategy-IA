from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def Vectorizador_func(documents=None):
    # Verificación de la cantidad de documentos antes de generar los embeddings
    print(f"Generando {len(documents)} embeddings...")

    if not documents:
        print("No se pasaron documentos válidos para la vectorización.")
        return None

    for i, doc in enumerate(documents[:3]):
        print(f"Documento {i + 1}: {doc.page_content[:200]}...")

    # 1) Crea o carga el store persistente
    vector_store = Chroma(
        collection_name="Strategy_articles",
        embedding_function=embeddings,
        persist_directory="./Strategy_Chroma_db",
    )

    # 2) Añade los documentos al store
    vector_store.add_documents(documents)

    # 3) Fuerza la persistencia en disco
    vector_store.persist()

    return vector_store
