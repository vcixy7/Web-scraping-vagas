import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import streamlit as st

import fontes
from scraper.util import format_brl
from exporter.excel import salvar_excel
from database.db import iniciar_banco, registrar_pesquisa, salvar_vagas
from database import consultas

st.set_page_config(page_title="Coleta de vagas", layout="wide")

iniciar_banco()

st.title("Coleta de vagas")
st.caption("Pesquise um cargo em várias fontes de uma vez. Os resultados ficam guardados no banco.")


def tabela_vagas(vagas):
    return pd.DataFrame([{
        "Título": v.get("titulo"),
        "Empresa": v.get("empresa"),
        "Local": v.get("local"),
        "UF": v.get("estado"),
        "Modalidade": v.get("modalidade"),
        "Salário": v.get("salario_texto"),
        "Tecnologias": ", ".join(v.get("tecnologias", [])),
        "Fonte": v.get("fonte"),
        "Link": v.get("url"),
    } for v in vagas])


# --- pesquisa ---
disponiveis = fontes.nomes()
padrao = [f for f in ("remotive", "remoteok") if f in disponiveis]

col_cargo, col_fontes = st.columns([2, 3])
cargo = col_cargo.text_input("Cargo", placeholder="ex.: desenvolvedor python")
selecionadas = col_fontes.multiselect(
    "Fontes", disponiveis, default=padrao,
    help="O Indeed abre o Chrome; as demais usam API e são mais rápidas.",
)

if st.button("Pesquisar", type="primary") and cargo.strip() and selecionadas:
    with st.spinner("Coletando vagas nas fontes escolhidas..."):
        pesquisa_id = registrar_pesquisa(cargo.strip())
        vagas = fontes.coletar_de(cargo.strip(), selecionadas)

    if vagas:
        novas, duplicadas = salvar_vagas(vagas, pesquisa_id=pesquisa_id)
        salvar_excel(vagas)
        st.success(f"{len(vagas)} vagas coletadas — {novas} novas, {duplicadas} já estavam no banco.")
        st.dataframe(tabela_vagas(vagas), use_container_width=True, hide_index=True)
    else:
        st.warning("Nenhuma vaga encontrada.")

st.divider()

# --- resumo do banco ---
st.header("Resumo do banco")

col1, col2, col3 = st.columns(3)
col1.metric("Vagas no banco", consultas.total_vagas())
col2.metric("Empresas", consultas.total_empresas())
media = consultas.salario_medio()
col3.metric("Salário médio", format_brl(media) if media else "sem dados")

col_esq, col_dir = st.columns(2)

with col_esq:
    por_estado = consultas.vagas_por_estado()
    if por_estado:
        st.subheader("Vagas por estado")
        st.bar_chart(pd.DataFrame(por_estado, columns=["Estado", "Vagas"]).set_index("Estado"))

    por_modalidade = consultas.vagas_por_modalidade()
    if por_modalidade:
        st.subheader("Vagas por modalidade")
        st.bar_chart(pd.DataFrame(por_modalidade, columns=["Modalidade", "Vagas"]).set_index("Modalidade"))

    por_fonte = consultas.vagas_por_fonte()
    if por_fonte:
        st.subheader("Vagas por fonte")
        st.bar_chart(pd.DataFrame(por_fonte, columns=["Fonte", "Vagas"]).set_index("Fonte"))

with col_dir:
    tecnologias = consultas.top_tecnologias(limite=10)
    if tecnologias:
        st.subheader("Tecnologias mais pedidas")
        st.bar_chart(pd.DataFrame(tecnologias, columns=["Tecnologia", "Vagas"]).set_index("Tecnologia"))

    top = consultas.top_empresas(limite=10)
    if top:
        st.subheader("Empresas com mais vagas")
        st.bar_chart(pd.DataFrame(top, columns=["Empresa", "Vagas"]).set_index("Empresa"))

por_dia = consultas.vagas_por_dia()
if por_dia and len(por_dia) > 1:
    st.subheader("Vagas coletadas ao longo do tempo")
    st.line_chart(pd.DataFrame(por_dia, columns=["Dia", "Vagas"]).set_index("Dia"))

st.divider()

# --- histórico de pesquisas ---
st.header("Histórico de pesquisas")

historico = consultas.historico_pesquisas()
if not historico:
    st.write("Nenhuma pesquisa registrada ainda.")
else:
    df_hist = pd.DataFrame(historico, columns=["id", "Cargo", "Quando", "Coletadas", "Novas"])
    st.dataframe(df_hist.drop(columns=["id"]), use_container_width=True, hide_index=True)

    opcoes = {f"{cargo} — {quando}": pid for pid, cargo, quando, _t, _n in historico}
    escolha = st.selectbox("Ver as vagas de uma pesquisa", list(opcoes.keys()))
    if escolha:
        vagas = consultas.vagas_da_pesquisa(opcoes[escolha])
        if vagas:
            df = pd.DataFrame(
                vagas,
                columns=["Título", "Empresa", "Local", "UF", "Modalidade", "Salário", "Fonte", "Link"],
            )
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.write("Essa pesquisa não guardou vagas novas (podem ter sido todas duplicadas).")
