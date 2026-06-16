# Desafio MBA Engenharia de Software com IA - Full Cycle

## Sobre o Projeto

Este é um projeto de **RAG (Retrieval-Augmented Generation)** que implementa um pipeline completo de ingestão e busca de documentos PDF usando embeddings vetoriais e busca por similaridade semântica.

### Arquitetura

O projeto é composto por 3 etapas principais:

1. **Ingest** (`src/ingest.py`): Carrega um PDF, divide o texto em chunks, gera embeddings via API OpenAI ou Google, e armazena em PostgreSQL com pgvector.

2. **Search** (`src/search.py`): Realiza busca de similaridade vetorial contra os embeddings armazenados e passa o contexto recuperado para uma LLM com um prompt em português.

3. **Chat** (`src/chat.py`): Interface REPL interativa que permite fazer perguntas e receber respostas baseadas no documento ingerido.

---

## Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+
- Uma chave de API (OpenAI ou Google Gemini)
- Um arquivo PDF para ingerir

---

## Instalação e Configuração

### 1. Clonar o repositório

```bash
git clone <seu-repo>
cd mba-ia-desafio-ingestao-busca
```

### 2. Criar arquivo `.env`

Copie o arquivo de exemplo e configure com suas credenciais:

```bash
cp .env.example .env
```

**Edite `.env` e configure:**

```env
# Banco de Dados
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=document_chunks

# Caminho do PDF a ser ingerido
PDF_PATH=document.pdf

# Escolha UMA opção de embedding provider:

# Opção 1: OpenAI
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Opção 2: Google Gemini
# GOOGLE_API_KEY=AIza...
# GOOGLE_EMBEDDING_MODEL=models/embedding-001
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Como Executar

### Passo 1: Iniciar a infraestrutura (PostgreSQL + pgvector)

```bash
docker compose up -d
```

Verifique se o banco está rodando:

```bash
docker compose logs postgres
```

### Passo 2: Ingerir o documento PDF

Coloque o arquivo `document.pdf` na raiz do projeto, depois execute:

```bash
python src/ingest.py
```

Isso irá:
- Ler o PDF
- Dividir o texto em chunks
- Gerar embeddings via API configurada
- Armazenar os embeddings no PostgreSQL/pgvector

### Passo 3: Usar o chat interativo

```bash
python src/chat.py
```

Digite suas perguntas em português e o sistema retornará respostas baseadas no documento ingerido.

Exemplo:
```
> Qual é o tema principal do documento?
> Quais são os principais conceitos abordados?
> Sair (ou Ctrl+C para encerrar)
```

---

## Variáveis de Ambiente Detalhadas

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | String de conexão PostgreSQL | `postgresql://postgres:postgres@localhost:5432/rag` |
| `PG_VECTOR_COLLECTION_NAME` | Nome da coleção para armazenar chunks | `document_chunks` |
| `PDF_PATH` | Caminho do arquivo PDF a ingerir | `document.pdf` |
| `OPENAI_API_KEY` | Chave API OpenAI (se usar OpenAI) | `sk-...` |
| `OPENAI_EMBEDDING_MODEL` | Modelo de embedding OpenAI | `text-embedding-3-small` |
| `GOOGLE_API_KEY` | Chave API Google (se usar Gemini) | `AIza...` |
| `GOOGLE_EMBEDDING_MODEL` | Modelo de embedding Google | `models/embedding-001` |

---

## Estrutura do Projeto

```
.
├── src/
│   ├── ingest.py       # Script de ingestão de PDFs
│   ├── search.py       # Lógica de busca vetorial
│   └── chat.py         # Interface REPL interativa
├── tests/
│   ├── features/       # Cenários BDD (Gherkin)
│   └── step_defs/      # Implementação dos steps BDD
├── docker-compose.yml  # Configuração dos serviços
├── requirements.txt    # Dependências Python
├── .env.example        # Template de variáveis de ambiente
└── CLAUDE.md          # Instruções para Claude Code
```

---

## Rodando Testes

### Executar todos os testes com cobertura

```bash
pytest tests/ --cov=src --cov-report=html
```

### Executar apenas testes BDD

```bash
pytest tests/features/ -v
```

---

## Troubleshooting

### "Connection refused" ao tentar conectar ao PostgreSQL

Verifique se o container está rodando:

```bash
docker compose ps
```

Se não estiver, inicie:

```bash
docker compose up -d
```

### "ModuleNotFoundError" ao executar scripts

Certifique-se de que o virtual environment está ativado e as dependências instaladas:

```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### Erros de API (OpenAI/Google)

- Verifique se a chave de API está correta no `.env`
- Verifique se a chave tem créditos/permissões
- Verifique a conexão com a internet

### O PDF não está sendo carregado

- Certifique-se de que `PDF_PATH` aponta para um arquivo existente
- Verifique se o arquivo está no diretório correto
- Verifique se o PDF não está corrompido

---

## Parar os serviços

```bash
docker compose down
```

Para parar e remover dados:

```bash
docker compose down -v
```

---

## Dependências Principais

- **LangChain**: Framework para RAG
- **pgvector**: Extensão PostgreSQL para busca vetorial
- **pypdf**: Parsing de PDFs
- **SQLAlchemy**: ORM para banco de dados
- **asyncpg/psycopg**: Drivers PostgreSQL
- **OpenAI/Google SDK**: Para geração de embeddings

---

## Autor

Desenvolvido como parte do desafio do MBA em Engenharia de Software com IA.
