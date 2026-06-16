# Test Suite - MBA IA Desafio Ingestão e Busca

## Overview

Este diretório contém os testes BDD (Behavior-Driven Development) para o desafio de ingestão de PDF e busca semântica usando LangChain e PostgreSQL/pgvector.

A estratégia de testes segue **TDD (Test-Driven Development)** com **BDD (Behavior-Driven Development)**, focando em cenários de uso reais e requisitos explícitos do exercício.

## Estrutura

```
tests/
├── conftest.py                    # Fixtures compartilhadas de pytest
├── pytest.ini                     # Configuração do pytest e pytest-bdd
├── README.md                      # Este arquivo
├── features/                      # Definições BDD em Gherkin
│   ├── ingest.feature            # Cenários de ingestão do PDF
│   ├── search.feature            # Cenários de busca semântica
│   └── chat.feature              # Cenários de interação CLI
└── step_defs/                    # Implementações dos steps
    ├── test_ingest_steps.py      # Steps para ingestão
    ├── test_search_steps.py      # Steps para busca
    └── test_chat_steps.py        # Steps para chat
```

## Instalação de Dependências de Teste

```bash
pip install pytest pytest-bdd pytest-mock pytest-asyncio
```

Ou adicione ao `requirements.txt`:
```
pytest==7.4.x
pytest-bdd==6.1.x
pytest-mock==3.12.x
pytest-asyncio==0.23.x
```

## Rodando os Testes

### Todos os testes
```bash
pytest tests/
```

### Apenas BDD
```bash
pytest tests/ -m bdd --gherkin-terminal-reporter
```

### Teste específico
```bash
pytest tests/step_defs/test_ingest_steps.py::test_successful_pdf_ingestion -v
```

### Com cobertura
```bash
pytest tests/ --cov=src --cov-report=html
```

## Cenários Cobertos

### 1. **Ingestão (ingest.feature)** - 5 cenários

- ✅ **Ingestão bem-sucedida do PDF**: Valida o fluxo completo de carregamento, chunking, embedding e armazenamento
- ✅ **Validação de tamanho de chunk**: Garante chunks de 1000 caracteres com overlap de 150
- ✅ **Falha ao encontrar arquivo PDF**: Testa FileNotFoundError quando o caminho é inválido
- ✅ **Falha de conexão ao banco de dados**: Testa erros de conexão PostgreSQL
- ✅ **Múltiplos chunks processados**: Valida processamento de PDFs multi-página sem perda de dados

### 2. **Busca (search.feature)** - 6 cenários

- ✅ **Busca bem-sucedida com contexto**: Resposta baseada no documento (exemplo: faturamento)
- ✅ **Pergunta fora do contexto**: Resposta padrão quando info não existe
- ✅ **Múltiplos resultados relevantes**: Consolidação correta de múltiplos chunks
- ✅ **Similaridade semântica correta**: Score > 0.85 para chunks relevantes
- ✅ **Ordem correta dos resultados**: Resultados ordenados por relevância decrescente
- ✅ **Contexto vazio**: Tratamento de busca sem resultados

### 3. **Chat (chat.feature)** - 7 cenários

- ✅ **Iniciação com sucesso**: Chat inicia sem erros de configuração
- ✅ **Pergunta e resposta completa**: Fluxo pergunta → busca → resposta
- ✅ **Comando exit**: Saída limpa do programa
- ✅ **Pergunta vazia**: Entrada vazia é ignorada
- ✅ **Erro de inicialização**: Mensagem de erro quando cadeia não inicia
- ✅ **Múltiplas perguntas em sequência**: 3+ perguntas sem contaminação de estado
- ✅ **Entrada muito longa**: Pergunta > 500 caracteres processada corretamente

## Fixtures Disponíveis (conftest.py)

| Fixture | Propósito |
|---------|-----------|
| `mock_pdf_path` | Arquivo PDF temporário para testes |
| `mock_env_vars` | Variáveis de ambiente pré-configuradas |
| `mock_pgvector` | Mock do PGVector (banco vetorial) |
| `mock_embeddings` | Mock do provedor de embeddings |
| `mock_llm` | Mock do LLM (ChatOpenAI) |
| `mock_pdf_loader` | Mock do carregador de PDF |
| `sample_documents` | Documentos de exemplo com metadados |
| `sample_search_results` | Resultados de busca com scores |

## Padrão BDD (Gherkin)

Os cenários seguem o padrão:
```gherkin
Cenário: Descrição clara do comportamento esperado
  Dado que [situação inicial]
  Quando [ação tomada]
  Então [resultado esperado]
```

Exemplo:
```gherkin
Cenário: Busca bem-sucedida com resposta dentro do contexto
  Dado que o banco de dados vetorial está populado com embeddings
  E que o usuário faz a pergunta "Qual o faturamento da Empresa SuperTechIABrazil?"
  Quando a pergunta é vetorizada
  E os 10 resultados mais relevantes são recuperados
  E o LLM processa o prompt com o contexto
  Então a resposta deve ser "O faturamento foi de 10 milhões de reais."
  E a resposta deve estar contida no contexto
```

## Conceitos-Chave dos Testes

### 1. **TDD (Test-Driven Development)**
- Testes escritos ANTES da implementação
- Garante que o código atende aos requisitos
- Facilita refatoração futura

### 2. **BDD (Behavior-Driven Development)**
- Testes em linguagem natural (Gherkin)
- Alinha testes com requisitos de negócio
- Facilita comunicação entre dev e stakeholders

### 3. **Mocking**
- Isolamento de dependências (LLM, banco de dados, API)
- Testes mais rápidos e determinísticos
- Sem necessidade de infra real durante testes

### 4. **Cobertura de Casos de Uso**
- Caminho feliz (happy path): tudo funciona
- Caminhos de erro: exceções e erros são tratados
- Casos extremos: entrada vazia, muito grande, etc.

## Próximos Passos

1. **Implementar os módulos** (`src/ingest.py`, `src/search.py`, `src/chat.py`)
2. **Rodar os testes** para validar a implementação
3. **Melhorar testes** conforme novos requisitos surgem
4. **Adicionar testes de integração** quando a infra estiver pronta

## Referências

- [pytest documentation](https://docs.pytest.org/)
- [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [Gherkin syntax](https://cucumber.io/docs/gherkin/)
- [BDD & TDD best practices](https://en.wikipedia.org/wiki/Behavior-driven_development)
