# ============================
# server/handlers.py
# ============================

def aplicar_filtros(query, filtros, Veiculo):
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
    return query