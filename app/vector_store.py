# Import Gemini embeddings.
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# Import LangChain's current PostgreSQL vector-store helpers.
from langchain_postgres import PGEngine, PGVectorStore
# Import shared settings.
from app.config import (
DATABASE_URL,
EMBEDDING_DIMENSIONS,
EMBEDDING_MODEL,
VECTOR_TABLE,
)
# Create the same kind of embedding model used in Part 1.
embeddings = GoogleGenerativeAIEmbeddings(
# Current embedding model.
model=EMBEDDING_MODEL,
# Make vectors exactly the size expected by PostgreSQL.
output_dimensionality=EMBEDDING_DIMENSIONS,
)
# Connect LangChain to PostgreSQL.
engine = PGEngine.from_connection_string(url=DATABASE_URL)
# Point LangChain at the table created by setup_db.py.
vector_store = PGVectorStore.create_sync(
# Reuse our database engine.
engine=engine,
# Store/search embeddings with this model.
embedding_service=embeddings,
# Use the existing vector table.
table_name=VECTOR_TABLE,
)