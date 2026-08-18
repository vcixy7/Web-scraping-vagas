import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import streamlit as st

from scraper.coletor import coletar
from scraper.util import format_brl
from exporter.excel import salvar_excel
from database.db import iniciar_banco, registrar_pesquisa, salvar_vagas
from database import consultas

st.set_page_config(page_title="Coleta de vagas", layout="wide")

iniciar_banco()

st.title("Coleta de vagas")
st.caption("Pesquise um cargo e colete as vagas do Indeed. Os resultados ficam guardados no banco.")

cargo = st.text_input("Cargo", placeholder="ex.: desenvolvedor python")

if st.button("Pesquisar", type="primary") and cargo.strip():
    with st.spinner("Coletando vagas... o navegador vai abrir, aguarde."):
        registrar_pesquisa(cargo.strip())
        vagas = coletar(cargo.strip())

    if vagas:
        novas, duplicadas = salvar_vagas(vagas)
        salvar_excel(vagas)
        st.success(f"{len(vagas)} vagas coletadas — {novas} novas, {duplicadas} já estavam no banco.")
        tabela = pd.DataFrame(vagas)[["titulo", "empresa", "local", "estado", "salario_texto", "url"]]
        tabela.columns = ["Título", "Empresa", "Local", "UF", "Salário", "Link"]
        st.dataframe(tabela, use_container_width=True, hide_index=True)
    else:
        st.warning("Nenhuma vaga encontrada.")

st.divider()
st.header("Resumo do banco")

col1, col2, col3 = st.columns(3)
col1.metric("Vagas no banco", consultas.total_vagas())
col2.metric("Empresas", consultas.total_empresas())
media = consultas.salario_medio()
col3.metric("Salário médio", format_brl(media) if media else "sem dados")

por_estado = consultas.vagas_por_estado()
if por_estado:
    st.subheader("Vagas por estado")
    df_estado = pd.DataFrame(por_estado, columns=["Estado", "Vagas"]).set_index("Estado")
    st.bar_chart(df_estado)

top = consultas.top_empresas(limite=10)
if top:
    st.subheader("Empresas com mais vagas")
    df_empresas = pd.DataFrame(top, columns=["Empresa", "Vagas"]).set_index("Empresa")
    st.bar_chart(df_empresas)
