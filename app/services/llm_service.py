from langchain.llms import Ollama
from app.services.retriever import retrieve_documents

def generate_response(user_query: str):
    documents = retrieve_documents(user_query)
    context = "\n\n".join([doc.page_content for doc in documents])

    llm = Ollama(model="llama3:8b-instruct")
    prompt = f"""
    Usa esta informacion de referencia para responder la pregunta:

    {context}

    Pregunta: {user_query}

    Respuesta:
    """
    
    return llm.invoke(prompt)
