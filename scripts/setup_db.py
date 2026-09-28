# Import the LangChain PostgreSQL engine helper.
from langchain_postgres import PGEngine
# Import our project settings.
from app.config import DATABASE_URL, EMBEDDING_DIMENSIONS, VECTOR_TABLE
# Create a reusable engine connected to PostgreSQL.
engine = PGEngine.from_connection_string(url=DATABASE_URL)
# Create the table only for a fresh database.
engine.init_vectorstore_table(
# Name of the table.
table_name=VECTOR_TABLE,
# PostgreSQL will enforce this embedding size.
vector_size=EMBEDDING_DIMENSIONS,
# Never drop an existing production table automatically.
overwrite_existing=False,
)
# Confirm completion.
print(f"Created vector table: {VECTOR_TABLE}")