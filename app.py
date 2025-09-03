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

name, auth_status, username = authenticator.login("Login", "sidebar")

if auth_status is False:
    st.error("Usuário ou senha inválidos.")
elif auth_status is None:
    st.info("Entre com suas credenciais para acessar. (Dica demo: cliente1 / senha123)")
elif auth_status:
    st.sidebar.success(f"Logado como: {name}")
    # Optional: logout button
    authenticator.logout("Sair", "sidebar")

    # Toggle Snowflake (opcional)
    use_sf = st.sidebar.checkbox("Conectar Snowflake (read-only)", value=False)

    # Try Snowflake connection if checked
    sf_conn = None
    if use_sf:
        try:
            import snowflake.connector
            sf_conn = snowflake.connector.connect(
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA"),
            )
            st.sidebar.success("Conectado ao Snowflake ✅")
        except Exception as e:
            st.sidebar.error(f"Falha Snowflake: {e}")

    st.sidebar.page_link("pages/1_📊_Estatisticas_Gerais.py", label="Estatísticas Gerais")
    st.sidebar.page_link("pages/2_🗺️_Geoportal.py", label="Geoportal")
    st.sidebar.page_link("pages/3_📄_Relatorio_OGMP_2_0.py", label="Relatório OGMP 2.0")
    st.sidebar.page_link("pages/4_🛰️_Agendamento_de_Imagens.py", label="Agendamento de Imagens")

    st.markdown("> Use o menu à esquerda para navegar nas páginas.")
