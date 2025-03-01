from langchain_qdrant import QdrantVectorStore
from app.core.config import get_qdrant_settings
from langchain_ollama import OllamaEmbeddings

qdrant_settings = get_qdrant_settings()

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=OllamaEmbeddings(
        base_url=qdrant_settings.OLLAMA_URL,
        model="mxbai-embed-large"
    ),
    collection_name=qdrant_settings.QDRANT_COLLECTION_NAME,
    host=qdrant_settings.QDRANT_HOST,
    port=qdrant_settings.QDRANT_PORT
)

def retrieve_documents(query: str, k: int = 3):
    """Busca en Qdrant los documentos más relevantes usando búsqueda de similitud."""
    return vector_store.similarity_search(query, k=k)
