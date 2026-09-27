# Find PDF files.
import glob
# Load PDF pages.
from langchain_community.document_loaders import PyPDFLoader
# Split long text into chunks.
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Import the same chunk settings from Part 1.
from app.config import PDF_FOLDER, CHUNK_SIZE, CHUNK_OVERLAP
# Import the new persistent vector store.
from app.vector_store import vector_store
# Load and split PDFs exactly like the beginner version.
def load_and_split_documents(folder: str):
    # Find all PDFs.
    pdf_paths = glob.glob(f"{folder}/*.pdf")
    # Hold all PDF pages.
    documents = []
    # Read each PDF.
    for path in pdf_paths:
        # Show progress.
        print(f"Loading {path} ...")
        # Add all pages to the list.
        documents.extend(PyPDFLoader(path).load())
    # Create the same splitter used before.
    splitter = RecursiveCharacterTextSplitter(
        # Same chunk size from Part 1.
        chunk_size=CHUNK_SIZE,
        # Same overlap from Part 1.
        chunk_overlap=CHUNK_OVERLAP,
    )
    # Split pages into chunks.
    return splitter.split_documents(documents)
    # Run the ingestion job.
def main():
    # Load and split PDFs.
    chunks = load_and_split_documents(PDF_FOLDER)
    # Stop if there is nothing to store.
    if not chunks:
        # Explain the problem.
        print("No PDF text found.")
        # Exit the function.
        return
    # Embed the chunks and save them into PostgreSQL.
    vector_store.add_documents(chunks)
    # Show the result.
    print(f"Stored {len(chunks)} chunks in PostgreSQL.")
    # Start only when this script is run directly.
if __name__ == "__main__":
    # Run ingestion.
    main()