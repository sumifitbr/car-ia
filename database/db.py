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
