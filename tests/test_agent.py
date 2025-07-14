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
