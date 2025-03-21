from typing import final
from app.services.vector import VectorService
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_core_settings


@final
class LLMService:
    def __init__(self):
        self.vector_service = VectorService()
        self.core_settings = get_core_settings()

        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                max_retries=2,
                api_key=self.core_settings.GOOGLE_API_KEY,
            )
            print(
                f"✅ Successfully initialized Google LLM with model: {self.llm.model}"
            )
        except Exception as e:
            print(f"❌ Failed to initialize Google LLM: {str(e)}")
            raise

    def generate_response(self, user_query: str, vector_store):
        documents = self.vector_service.retrieve_documents(
            user_query, vector_store)
        context = "\n\n".join([doc.page_content for doc in documents])

        prompt = f"""
        Usa esta información de referencia para responder la pregunta:

        {context}

        Pregunta: {user_query}

        Respuesta:
        """

        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            print(f"❌ Error generating response: {str(e)}")
            return "Error al generar la respuesta."


service = LLMService()
