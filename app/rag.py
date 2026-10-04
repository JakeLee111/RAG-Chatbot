# Import the Gemini chat model.
from langchain_google_genai import ChatGoogleGenerativeAI
# Import the selected chat model name.
from app.config import CHAT_MODEL
# Import our PostgreSQL-backed vector store.
from app.vector_store import vector_store
# Create the answer model once.
model = ChatGoogleGenerativeAI(
    # Use our configured model.
    model=CHAT_MODEL,
    # Keep factual answers steady.
    temperature=0,
    )
# Retrieve context from PostgreSQL.
def retrieve_context(question: str):
    # Ask pgvector for the four closest chunks.
    docs = vector_store.similarity_search(question, k=4)
    # Join the chunk text for the prompt.
    context = "\n\n".join(doc.page_content for doc in docs)
    # Return both text and documents so we can show sources.
    return context, docs
# Answer one question using retrieved evidence.
def answer_question(question: str):
    # Search the vector database first.
    context, docs = retrieve_context(question)
    # Build a strict RAG prompt.
    prompt = f"""
You are a helpful health education assistant.
Answer in simple English, be casual and brief.

For readability:
- Use short paragraphs.
- Use bullet points when listing symptoms or causes.
- Start with a short direct answer.
- Then give 3 to 6 clear key points.
- If relevant, end with a short note.
- Do not make up information outside the provided context.
- If no context provided, say you don't have that in the database.

Context:
{context}
Question:
{question}
"""
    # Ask Gemini to write the final answer.
    response = model.invoke(prompt)
    # Return the answer plus simple source metadata.
    return {
    "answer": response.text,
    "sources": [doc.metadata for doc in docs],
    }