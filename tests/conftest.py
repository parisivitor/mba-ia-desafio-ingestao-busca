import os
import pytest
from unittest.mock import MagicMock, patch
import tempfile


@pytest.fixture
def mock_pdf_path():
    """Provide a temporary PDF path for testing."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        # Create a minimal valid PDF
        tmp.write(b"%PDF-1.4\n%\xE2\xE3\xCF\xD3\n")
        tmp.write(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
        tmp.write(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
        tmp.write(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> >>\nendobj\n")
        tmp.write(b"4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 12 Tf 100 700 Td (Test PDF) Tj ET\nendstream\nendobj\n")
        tmp.write(b"xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000262 00000 n\n")
        tmp.write(b"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n355\n%%EOF\n")
        tmp_path = tmp.name
    yield tmp_path
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rag")
    monkeypatch.setenv("PG_VECTOR_COLLECTION_NAME", "test_collection")
    monkeypatch.setenv("PDF_PATH", "document.pdf")


@pytest.fixture
def mock_pgvector():
    """Mock PGVector database operations."""
    with patch("langchain_postgres.PGVector") as mock_vec:
        yield mock_vec


@pytest.fixture
def mock_embeddings():
    """Mock embeddings provider."""
    with patch("langchain_openai.OpenAIEmbeddings") as mock_emb:
        yield mock_emb


@pytest.fixture
def mock_llm():
    """Mock LLM provider."""
    with patch("langchain_openai.ChatOpenAI") as mock_llm_obj:
        yield mock_llm_obj


@pytest.fixture
def mock_pdf_loader():
    """Mock PDF loader."""
    with patch("langchain_community.document_loaders.PyPDFLoader") as mock_loader:
        yield mock_loader


@pytest.fixture
def sample_documents():
    """Sample documents that would come from PDF parsing."""
    return [
        {
            "page_content": "A Empresa SuperTechIABrazil teve um faturamento de 10 milhões de reais em 2023.",
            "metadata": {"source": "document.pdf", "page": 0},
        },
        {
            "page_content": "Os clientes principais são: TechCorp, DataSys e CloudNet.",
            "metadata": {"source": "document.pdf", "page": 1},
        },
        {
            "page_content": "O custo operacional foi de 3 milhões de reais.",
            "metadata": {"source": "document.pdf", "page": 2},
        },
    ]


@pytest.fixture
def sample_search_results():
    """Sample results from vector similarity search."""
    return [
        (
            {
                "page_content": "A Empresa SuperTechIABrazil teve um faturamento de 10 milhões de reais em 2023.",
                "metadata": {"source": "document.pdf", "page": 0},
            },
            0.95,
        ),
        (
            {
                "page_content": "Os clientes principais são: TechCorp, DataSys e CloudNet.",
                "metadata": {"source": "document.pdf", "page": 1},
            },
            0.87,
        ),
    ]
