import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "documents")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-3.5-turbo")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
GOOGLE_LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def get_embeddings():
    """Get embeddings provider (OpenAI or Google)."""
    if OPENAI_API_KEY:
        return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    elif GOOGLE_API_KEY:
        return GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)
    else:
        raise ValueError("No embedding API key configured. Set OPENAI_API_KEY or GOOGLE_API_KEY")


def get_llm():
    """Get LLM provider (OpenAI or Google)."""
    if OPENAI_API_KEY:
        return ChatOpenAI(model=OPENAI_LLM_MODEL, temperature=0)
    elif GOOGLE_API_KEY:
        return ChatGoogleGenerativeAI(model=GOOGLE_LLM_MODEL, temperature=0)
    else:
        raise ValueError("No LLM API key configured. Set OPENAI_API_KEY or GOOGLE_API_KEY")


def search_prompt(question=None):
    """
    Search in vector DB and return LLM chain response.

    Args:
        question: User question to search for

    Returns:
        A callable chain that takes a question and returns a response
    """
    try:
        # Get embeddings and LLM
        embeddings = get_embeddings()
        llm = get_llm()

        # Connect to pgvector
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=PG_VECTOR_COLLECTION_NAME,
            connection=DATABASE_URL
        )

        # Create RAG chain
        def rag_chain(q):
            # Search for k=10 most relevant results
            results = vector_store.similarity_search_with_score(q, k=10)

            # Build context from results
            contexto = "\n\n".join([doc.page_content for doc, score in results])

            # If no results, use empty context (LLM will say it has no info)
            if not contexto:
                contexto = ""

            # Create prompt
            prompt_template = PromptTemplate(
                input_variables=["contexto", "pergunta"],
                template=PROMPT_TEMPLATE
            )

            # Format prompt and invoke LLM
            formatted_prompt = prompt_template.format(contexto=contexto, pergunta=q)
            response = llm.invoke(formatted_prompt)

            return response.content

        # If question is provided, return the answer directly
        if question:
            return rag_chain(question)

        # Otherwise return the chain for later use
        return rag_chain

    except Exception as e:
        print(f"❌ Error initializing search chain: {str(e)}")
        return None