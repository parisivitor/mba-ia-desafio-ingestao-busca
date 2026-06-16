from search import search_prompt


def main():
    """Interactive chat CLI for semantic search."""
    try:
        chain = search_prompt()

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return

        print("\n" + "=" * 60)
        print("Chat de Busca Semântica - Digite 'exit' para sair")
        print("=" * 60 + "\n")

        while True:
            try:
                question = input("Faça sua pergunta: ").strip()

                # Exit command
                if question.lower() == "exit":
                    print("Encerrando chat...")
                    break

                # Ignore empty input
                if not question:
                    print("Por favor, digite uma pergunta.\n")
                    continue

                # Get response
                response = chain(question)
                print(f"\nRESPOSTA: {response}\n")

            except KeyboardInterrupt:
                print("\n\nEncerrando chat...")
                break
            except Exception as e:
                print(f"❌ Erro ao processar pergunta: {str(e)}\n")
                continue

    except Exception as e:
        print(f"Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        print(f"Detalhes: {str(e)}")
        return


if __name__ == "__main__":
    main()