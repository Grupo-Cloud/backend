from langchain_community.llms import Ollama  
from app.services.vector import VectorService

class LLMService:
    def __init__(self):
        self.vector_service = VectorService()
        self.llm = Ollama(model="llama3:8b-instruct")

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
