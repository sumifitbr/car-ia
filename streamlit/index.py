import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.ai_agent import interpretar_filtros
from client.client import send_filters
from rich import print

st.set_page_config(page_title="Busca Inteligente de Carros", layout="wide")

st.title("Busca Inteligente de Carros com IA")

query = st.text_input(
    "Digite o que está procurando (ex: carro flex, ano mínimo 2018, até 50 mil):"
)

if st.button("Buscar") and query.strip():
    with st.spinner("Interpretando e buscando..."):
        filtros = interpretar_filtros(query)
        if filtros is None:
            st.error("Erro ao interpretar sua busca. Tente novamente.")
        else:
            resultados = send_filters(filtros.dict())
            if not resultados:
                st.warning("Nenhum veículo encontrado com os filtros fornecidos.")
            else:
                st.success(f"Encontrados {len(resultados)} veículos:")
                for r in resultados:
                    st.write(
                        f"**{r['marca']} {r['modelo']}** — {r['ano']} — {r['cor']} — "
                        f"{r['quilometragem']} km — R$ {r['preco']:.2f}"
                    )
