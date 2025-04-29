from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def Vectorizador_func(documents=None):
    if not documents:
        print("No se pasaron documentos válidos para la vectorización.")
        return None
    
    # Verificación de la cantidad de documentos antes de generar los embeddings
    print(f"Generando {len(documents)} embeddings...")

    for i, doc in enumerate(documents):
        doc.metadata['source'] = f'doc_{i+1}'

    # 1) Crea o carga el store persistente
    vector_store = Chroma(
        collection_name="Strategy_articles",
        embedding_function=embeddings,
        persist_directory="./Strategy_Chroma_db",
    )

    # 2) Añade los documentos al store
    vector_store.add_documents(documents)
    # 3) Garantización de la persistencia
    #vector_store.persist()

    return vector_store
