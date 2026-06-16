import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "documents")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")


def get_embeddings():
    """Get embeddings provider (OpenAI or Google)."""
    if OPENAI_API_KEY:
        return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    elif GOOGLE_API_KEY:
        return GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)
    else:
        raise ValueError("No embedding API key configured. Set OPENAI_API_KEY or GOOGLE_API_KEY")


def ingest_pdf():
    """Ingest PDF: load, chunk, embed, and store in pgvector."""
    try:
        # Load PDF
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()

        if not documents:
            print(f"No documents loaded from {PDF_PATH}")
            return

        print(f"✅ Loaded {len(documents)} pages from {PDF_PATH}")

        # Split into chunks (1000 chars, overlap 150)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✅ Split into {len(chunks)} chunks")

        # Get embeddings provider
        embeddings = get_embeddings()
        print("✅ Embeddings provider initialized")

        # Store in pgvector
        vector_store = PGVector.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=PG_VECTOR_COLLECTION_NAME,
            connection=DATABASE_URL
        )
        print(f"✅ Stored {len(chunks)} chunks in pgvector collection '{PG_VECTOR_COLLECTION_NAME}'")

    except FileNotFoundError:
        print(f"❌ Error: PDF file not found at {PDF_PATH}")
        raise
    except Exception as e:
        print(f"❌ Error during ingestion: {str(e)}")
        raise


if __name__ == "__main__":
    ingest_pdf()