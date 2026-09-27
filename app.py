import glob
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.vectorstores import InMemoryVectorStore

load_dotenv()

PDF_FOLDER = "pdfs"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")
model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash",
    temperature=0,
    )

def load_and_split_documents(folder: str):
    pdf_paths = glob.glob(f"{folder}/*.pdf")
    documents = []
    for path in pdf_paths:
        print(f"Loading {path} ...")
        documents.extend(PyPDFLoader(path).load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"Loaded {len(documents)} page(s), split into {len(chunks)} chunk(s).")
    return chunks

def build_vector_store(chunks):
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(chunks)
    return vector_store

def retrieve_context(vector_store, question: str):
    docs = vector_store.similarity_search(question, k=4)
    context = "\n\n".join(doc.page_content for doc in docs)
    return context

def answer_question(vector_store, question: str):
    context = retrieve_context(vector_store, question)
    prompt = f""""
You are a helpful RAG chatbot.
Answer the question using only the context below.
If the answer is not in the context, say: "I don't know from the PDF."
Keep the answer simple and short.
Context:
{context}
Question:
{question}
"""
    response = model.invoke(prompt)
    return response.text

def main():
    chunks = load_and_split_documents(PDF_FOLDER)
    if not chunks:
        print("No PDF found. Add a PDF to the pdfs folder.")
        return
    vector_store = build_vector_store(chunks)
    print("RAG chatbot is ready. Type 'exit' to stop.")

    while True:
        question = input("\nYou: ").strip()
        if question.lower() == "exit":
            print("Bot: Bye!")
            break

        answer = answer_question(vector_store,question)
        print(f"Bot: {answer}")

if __name__ == "__main__":
    main()