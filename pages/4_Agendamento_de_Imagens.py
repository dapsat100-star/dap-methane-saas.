import streamlit as st
from datetime import date

st.title("🛰️ Agendamento de Imagens")

with st.form("agendar"):
    unidade = st.text_input("Nome da Unidade/Ativo", placeholder="Ex.: Plataforma P-XX")
    janela = st.date_input("Data desejada", value=date.today())
    prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
    observ = st.text_area("Observações (opcional)")
    enviar = st.form_submit_button("Agendar")

if enviar:
    if not unidade:
        st.error("Informe o nome da Unidade/Ativo.")
    else:
        st.success(f"Solicitação registrada para **{unidade}** em **{janela}** (Prioridade: {prioridade}).")
        if observ:
            st.caption(f"Obs.: {observ}")
