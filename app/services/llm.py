import os
from langchain_community.llms import Ollama  
from app.services.vector import VectorService

class LLMService:
    def __init__(self):
        self.vector_service = VectorService()
        
        ollama_url = os.getenv("OLLAMA_URL")
        
        print(f"Initializing LLM with Ollama URL: {ollama_url}")
        
        if not ollama_url:
            ollama_url = "http://localhost:11434"
            print(f"OLLAMA_URL not found in environment, using default: {ollama_url}")
        
        if not ollama_url.startswith("http://") and not ollama_url.startswith("https://"):
            ollama_url = f"http://{ollama_url}"
            print(f"Added http:// prefix to Ollama URL: {ollama_url}")
        
        try:
            self.llm = Ollama(
                base_url=ollama_url,
                model="llama3:8b"
            )
            print(f"Successfully initialized Ollama LLM with base_url: {ollama_url}")
        except Exception as e:
            print(f"Failed to initialize Ollama LLM: {str(e)}")
            raise

    def generate_response(self, user_query: str, vector_store):
        documents = self.vector_service.retrieve_documents(user_query, vector_store)
        context = "\n\n".join([doc.page_content for doc in documents])

        prompt = f"""
        Usa esta información de referencia para responder la pregunta:

        {context}

        Pregunta: {user_query}

        Respuesta:
        """

        return self.llm.invoke(prompt)

service = LLMService()