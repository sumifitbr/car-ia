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
