import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Agendamento de Imagens", page_icon="🛰️", layout="wide")
if "auth" not in st.session_state:
    st.switch_page("app.py")

st.title("🛰️ Agendamento de Imagens")

with st.form("tasking"):
    col1, col2 = st.columns(2)
    site = col1.selectbox("Site", ["FPSO A","FPSO B","UTG Guamaré","RNEST"])
    window = col2.slider("Janela de Aquisição (dias)", min_value=1, max_value=14, value=3)
    col3, col4 = st.columns(2)
    priority = col3.selectbox("Prioridade", ["Alta","Média","Baixa"], index=1)
    cloud = col4.slider("Cobertura de Nuvem Máxima (%)", 0, 100, 20)
    notes = st.text_area("Observações")
    submitted = st.form_submit_button("Solicitar Agendamento")

if submitted:
    st.success(f"Tasking criado para **{site}** (janela {window} dias, prioridade {priority}, nuvem ≤ {cloud}%).")
    st.caption("Este é um placeholder; a integração com provedores (GHGSat, BlackSky etc.) pode ser conectada via API.")

st.caption("Formulário demonstrativo (sem envio real).")
