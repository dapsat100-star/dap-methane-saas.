import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Plataforma de Metano OGMP 2.0 - L5", page_icon="🛰️", layout="wide")

# --- Simple auth (demo only) ---
def do_login(user, pwd):
    return user == "john" and pwd == "dap2025!"

def check_2fa(code):
    return code == "123456"

def login_screen():
    left, right = st.columns([1,1])
    with left:
        st.title("Plataforma de Monitoramento\nde Emissões de Metano OGMP 2.0 - L5")
        st.markdown("Plataforma DAP ATLAS certificada como estratégica de Defesa pelo Ministério da Defesa do Brasil (Portaria GMD-MD nº 5.574, DOU 12/12/2024).")
        with st.form("login"):
            user = st.text_input("Nome de Usuário", help="Usuário de demonstração: john")
            pwd = st.text_input("Senha", type="password", help="Senha demo: dap2025!")
            submitted = st.form_submit_button("Iniciar sessão")
        if submitted:
            if do_login(user, pwd):
                st.session_state["pending_2fa"] = True
                st.session_state["user_tmp"] = user
                st.rerun()
            else:
                st.error("Credenciais inválidas.")
    with right:
        st.subheader("Autenticação de dois fatores")
        with st.form("twofa"):
            code = st.text_input("Código de Verificação", help="Código demo: 123456")
            ok = st.form_submit_button("Verificar")
        if ok:
            if st.session_state.get("pending_2fa") and check_2fa(code):
                st.session_state["auth"] = True
                st.session_state["user"] = st.session_state.get("user_tmp","john")
                st.session_state.pop("pending_2fa", None)
                st.success("Autenticado com sucesso!")
                time.sleep(0.7)
                st.switch_page("pages/1_📊_Estatísticas_Gerais.py")
            else:
                st.error("Código inválido.")

if "auth" not in st.session_state:
    login_screen()
    st.stop()
else:
    st.sidebar.success(f"Bem-vindo, **{st.session_state.get('user','John D.').title()}**")
    st.sidebar.page_link("pages/1_📊_Estatísticas_Gerais.py", label="📊 Estatísticas Gerais")
    st.sidebar.page_link("pages/2_🗺️_Geoportal.py", label="🗺️ Geoportal")
    st.sidebar.page_link("pages/3_📄_Relatório_OGMP.py", label="📄 Relatório OGMP 2.0")
    st.sidebar.page_link("pages/4_🛰️_Agendamento_de_Imagens.py", label="🛰️ Agendamento de Imagens")
    st.sidebar.divider()
    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()
    st.switch_page("pages/1_📊_Estatísticas_Gerais.py")
