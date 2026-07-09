from dotenv import load_dotenv
import os
from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


def ask_question(question):
    results = vector_store.similarity_search(
        query=question,
        k=2
    )

    context = "\n\n".join(
        document.page_content for document in results
    )

    prompt = f"""
Answer the user's question using only the context provided below.

If the answer is not present in the context, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    sources = []

    for document in results:
        sources.append({
            "content": document.page_content,
            "source": document.metadata.get("source", "Unknown")
        })

    return response.text, sources