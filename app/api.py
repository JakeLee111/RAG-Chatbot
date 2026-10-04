# Import FastAPI.
from fastapi import FastAPI
# Import Pydantic for JSON validation.
from pydantic import BaseModel, Field
# Import the RAG function we already tested.
from app.rag import answer_question
# Create the web application.
app = FastAPI(title="RAG API", version="1.0.0")
# Define the JSON body for a question.
class AskRequest(BaseModel):
    # Require a useful question and prevent huge input.
    question: str = Field(min_length=2, max_length=2000)
# Add a lightweight health endpoint.
@app.get("/health")
def health():
    # Tell monitoring that the API process is alive.
    return {"status": "ok"}
# Add the chatbot endpoint.

@app.post("/ask")
def ask(request: AskRequest):
    # Reuse the exact RAG function from app/rag.py.
    return answer_question(request.question.strip())