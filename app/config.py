# Read environment variables.
import os
# Load values from the local .env file.
from dotenv import load_dotenv
# Load .env now.
load_dotenv()
# Database connection for PostgreSQL.
DATABASE_URL = os.environ["DATABASE_URL"]
# Models used by the chatbot.
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemini-3.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-2")
# Embedding vector size. This must match the database column size.
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "768"))
# Vector table name.
VECTOR_TABLE = os.getenv("VECTOR_TABLE", "rag_chunks")
# Existing PDF settings from the beginner version.
PDF_FOLDER = os.getenv("PDF_FOLDER", "pdfs")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150