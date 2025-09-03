import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# -----------------------------------------------------------------------------
# Configuração básica
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Plataforma de Metano OGMP 2.0 - L5", layout="wide")
load_dotenv()  # útil quando hospedar fora do Streamlit Cloud

# -----------------------------------------------------------------------------
# Hero (logo + título) mostrado SOMENTE na tela de login
# -----------------------------------------------------------------------------
def login_hero():
    # tenta achar o logo em dois lugares
    logo_candidates = [
        Path("dapatlas.jpeg"),
        Path("assets/logo.png"),
        Path(__file__).parent / "daplogo_upscaled.png",
        Path(__file__).parent / "assets/logo.png",
    ]
    logo_path = next((p for p in logo_candidates if p.exists()), None)

    # container central
    st.markdown(
        """
        <div style="display:flex;flex-direction:column;justify-content:center;
                    align-items:center;height:60vh;text-align:center;">
        """,
        unsafe_allow_html=True
    )

    if logo_path:
        st.image(Image.open(logo_path), width=220)
    else:
        st.warning("Logo não encontrado (envie 'daplogo_upscaled.png' na raiz "
                   "ou 'assets/logo.png').")

    st.markdown(
        """
            <h1 style="margin-top:16px;font-size:28px;color:#003366;">
                PLATAFORMA DE MONITORAMENTO DE METANO POR SATÉLITE
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# Autenticação (streamlit-authenticator)
# -----------------------------------------------------------------------------
# Espera 'auth_config.yaml' na raiz do repositório
with open("auth_config.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Mostra o HERO antes do login
hero_placeholder = st.empty()
with hero_placeholder.container():
    login_hero()

# Formulário de login (API nova usa location)
name, auth_status, username = authenticator.login("Login", "main")


if auth_status is False:
    st.error("Usuário ou senha inválidos.")
elif auth_status is None:
    st.info("Por favor, faça login para continuar.")
elif auth_status:
    # remove o hero ao autenticar
    hero_placeholder.empty()

    # Sidebar: usuário + logout
    st.sidebar.success(f"Logado como: {name}")
    authenticator.logout("Sair", "sidebar")

    # -------------------------------------------------------------------------
    # (Opcional) Conexão Snowflake via variáveis de ambiente / secrets
    # -------------------------------------------------------------------------
    use_sf = st.sidebar.checkbox("Conectar Snowflake (read-only)", value=False)
    if use_sf:
        try:
            import snowflake.connector
            conn = snowflake.connector.connect(
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA"),
            )
            st.sidebar.success("Conectado ao Snowflake ✅")
        except Exception as e:
            st.sidebar.error(f"Falha na conexão Snowflake: {e}")

    # -------------------------------------------------------------------------
    # Navegação entre páginas (arquivos em pages/)
    # -------------------------------------------------------------------------
    st.sidebar.page_link("pages/1_📊_Estatisticas_Gerais.py", label="Estatísticas Gerais")
    st.sidebar.page_link("pages/2_🗺️_Geoportal.py", label="Geoportal")
    st.sidebar.page_link("pages/3_📄_Relatorio_OGMP_2_0.py", label="Relatório OGMP 2.0")
    st.sidebar.page_link("pages/4_🛰️_Agendamento_de_Imagens.py", label="Agendamento de Imagens")

    st.markdown("> Use o menu à esquerda para navegar nas páginas.")
