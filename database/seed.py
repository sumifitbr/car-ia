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
