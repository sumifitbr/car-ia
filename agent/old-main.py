# ============================
# agent/main.py
# ============================

import sys
from client.client import send_filters
from rich import print

def start_agent():
    print("[bold green]Olá! Sou seu assistente de busca de carros.[/bold green]")
    filtros = {}

    filtros['marca'] = input("Qual a marca desejada? ")
    filtros['modelo'] = input("Tem algum modelo em mente? ")
    filtros['ano'] = input("Ano mínimo do carro? ")
    filtros['combustivel'] = input("Tipo de combustível? ")
    filtros['preco_max'] = input("Qual o preço máximo? ")

    resultados = send_filters(filtros)

    if not resultados:
        print("[bold red]Nenhum veículo encontrado com os filtros fornecidos.[/bold red]")
    else:
        print("[bold blue]\nVeículos encontrados:[/bold blue]")
        for r in resultados:
            print(f"{r['marca']} {r['modelo']} - {r['ano']} - {r['cor']} - {r['quilometragem']} km - R$ {r['preco']}")