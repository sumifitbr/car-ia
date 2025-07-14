### run.py
from agent.main import start_agent

if __name__ == '__main__':
    start_agent()


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


# ============================
# client/client.py
# ============================

def send_filters(filtros):
    from server.server import handle_request
    return handle_request(filtros)


# ============================
# server/server.py
# ============================

from database.db import get_session
from database.models import Veiculo

def handle_request(filtros):
    session = get_session()
    query = session.query(Veiculo)

    if filtros.get('marca'):
        query = query.filter(Veiculo.marca.ilike(f"%{filtros['marca']}%"))
    if filtros.get('modelo'):
        query = query.filter(Veiculo.modelo.ilike(f"%{filtros['modelo']}%"))
    if filtros.get('ano'):
        query = query.filter(Veiculo.ano >= int(filtros['ano']))
    if filtros.get('combustivel'):
        query = query.filter(Veiculo.combustivel.ilike(f"%{filtros['combustivel']}%"))
    if filtros.get('preco_max'):
        query = query.filter(Veiculo.preco <= float(filtros['preco_max']))

    resultados = query.all()
    return [
        {
            "marca": v.marca,
            "modelo": v.modelo,
            "ano": v.ano,
            "cor": v.cor,
            "quilometragem": v.quilometragem,
            "preco": v.preco,
        } for v in resultados
    ]


# ============================
# database/models.py
# ============================

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Veiculo(Base):
    __tablename__ = 'veiculos'

    id = Column(Integer, primary_key=True)
    marca = Column(String)
    modelo = Column(String)
    ano = Column(Integer)
    motorizacao = Column(String)
    combustivel = Column(String)
    cor = Column(String)
    quilometragem = Column(Integer)
    portas = Column(Integer)
    transmissao = Column(String)
    preco = Column(Float)


# ============================
# database/db.py
# ============================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

engine = create_engine('sqlite:///veiculos.db')
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

# Cria as tabelas, se não existirem
def init_db():
    Base.metadata.create_all(engine)


# ============================
# database/seed.py
# ============================

from faker import Faker
import random
from database.db import get_session, init_db
from database.models import Veiculo

init_db()
session = get_session()

faker = Faker()
combustiveis = ['Gasolina', 'Etanol', 'Flex', 'Diesel', 'Elétrico']
cores = ['Preto', 'Branco', 'Cinza', 'Vermelho', 'Azul']
transmissoes = ['Manual', 'Automática']

total_cars = 1000
for _ in range(total_cars):
    v = Veiculo(
        marca=faker.company(),
        modelo=faker.word(),
        ano=random.randint(2000, 2024),
        motorizacao=f"{random.randint(1, 3)}.{random.randint(0, 9)}",
        combustivel=random.choice(combustiveis),
        cor=random.choice(cores),
        quilometragem=random.randint(10000, 200000),
        portas=random.choice([2, 4]),
        transmissao=random.choice(transmissoes),
        preco=round(random.uniform(20000, 150000), 2),
    )
    session.add(v)

session.commit()
print(f"Banco populado com {total_cars} veículo(s).")


# ============================
# tests/test_agent.py
# ============================

def test_montagem_filtros():
    from client.client import send_filters
    filtros = {
        'marca': 'Ford',
        'modelo': '',
        'ano': '2015',
        'combustivel': 'Flex',
        'preco_max': '70000'
    }
    resultado = send_filters(filtros)
    assert isinstance(resultado, list)
    for r in resultado:
        assert r['marca']
        assert r['ano'] >= 2015
        assert r['preco'] <= 70000
