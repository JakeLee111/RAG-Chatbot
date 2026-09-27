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
You are a helpful RAG assistant.
Answer using only the context below.
If the answer is not in the context, say you do not know from the knowledge base.
Keep the answer short and clear.
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