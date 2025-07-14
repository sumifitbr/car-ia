from client.client import send_filters
from rich import print
from agent.ai_agent import interpretar_filtros

def start_agent():
    print("[bold green]Olá! Sou seu assistente de busca de carros por IA.[/bold green]")
    user_text = input("Digite o que está procurando (ex: carro vermelho até 50 mil):\n> ")

    try:
        filtros = interpretar_filtros(user_text)
        filtros_dict = {k: v for k, v in filtros.dict().items() if v is not None}

        resultados = send_filters(filtros_dict)

        if not resultados:
            print("[bold red]Nenhum veículo encontrado com os critérios fornecidos.[/bold red]")
        else:
            print("[bold blue]\nVeículos encontrados:[/bold blue]")
            for r in resultados:
                print(f"{r['marca']} {r['modelo']} - {r['ano']} - {r['cor']} - {r['quilometragem']} km - R$ {r['preco']}")
    except Exception as e:
        print("[bold red]Erro ao interpretar sua busca.[/bold red]")
        print(e)
