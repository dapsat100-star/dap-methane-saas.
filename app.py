import os, pathlib
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from dotenv import load_dotenv

st.set_page_config(page_title="Plataforma de Metano OGMP 2.0 - L5", layout="wide")

# ---------- Header with logo (right aligned) ----------
logo_file = pathlib.Path("assets/logo.png")
if logo_file.exists():
    c1, c2 = st.columns([6,1])
    with c2:
        st.image(str(logo_file), width=140)

# ---------- Load .env (optional for local dev) ----------
load_dotenv()

# ---------- Auth: streamlit-authenticator ----------
with open("auth_config.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# FIX: remover o parâmetro problemático; funciona em todas as versões
name, auth_status, username = authenticator.login(location="main")


if auth_status is False:
    st.error("Usuário ou senha inválidos.")
elif auth_status is None:
    st.warning("Por favor, faça login para continuar.")
else:
    authenticator.logout("Logout", "sidebar")
    st.success(f"Bem-vindo, {name}!")
    st.title("Dashboard de Metano (demo)")
    st.write("Aqui vai o conteúdo da sua aplicação (gráficos, tabelas, integrações, etc.).")
