import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# -----------------------------------------------------------------------------
# Config da página
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Plataforma de Metano OGMP 2.0 - L5", layout="wide")
load_dotenv()  # útil quando rodar fora do Streamlit Cloud

# -----------------------------------------------------------------------------
# Hero (logo + título) apenas na tela de login
# -----------------------------------------------------------------------------
def login_hero():
    logo_candidates = [
        Path("daplogo_upscaled.png"),
        Path("assets/logo.png"),
        Path(__file__).parent / "daplogo_upscaled.png",
        Path(__file__).parent / "assets/logo.png",
    ]
    logo_path = next((p for p in logo_candidates if p.exists()), None)

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
with open("auth_config.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Mostrar hero até logar
hero_placeholder = st.empty()
with hero_placeholder.container():
    login_hero()

# Compat: tenta API nova (>=0.4) e cai para antiga (<=0.3.2)
try:
    name, auth_status, username = authenticator.login(location="main")
except Exception:
    name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("Usuário ou senha inválidos.")
elif auth_status is None:
    st.info("Por favor, faça login para continuar.")
elif auth_status:
    # Remove hero ao autenticar
    hero_placeholder.empty()

    # Sidebar: usuário + logout
    st.sidebar.success(f"Logado como: {name}")
    authenticator.logout("Sair", "sidebar")

    # -------------------------------------------------------------------------
    # Redireciona automaticamente para a 1ª página (Estatísticas Gerais)
    # -------------------------------------------------------------------------
    try:
        st.switch_page("pages/1_📊_Estatisticas_Gerais.py")
        st.stop()
    except Exception:
        # Fallback (versões antigas sem switch_page)
        st.success("Login OK. Clique para ir às Estatísticas Gerais.")
        st.sidebar.page_link("pages/1_📊_Estatisticas_Gerais.py", label="Ir para Estatísticas Gerais")

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
    # Links na sidebar (só se o arquivo existir) — útil no fallback
    # -------------------------------------------------------------------------
    def safe_page_link(path: str, label: str):
        if Path(path).exists():
            st.sidebar.page_link(path, label=label)

    safe_page_link("pages/1_📊_Estatisticas_Gerais.py", "Estatísticas Gerais")
    safe_page_link("pages/2_🗺️_Geoportal.py", "Geoportal")
    safe_page_link("pages/3_📄_Relatorio_OGMP_2_0.py", "Relatório OGMP 2.0")
    safe_page_link("pages/4_🛰️_Agendamento_de_Imagens.py", "Agendamento de Imagens")

    st.markdown("> Use o menu à esquerda para navegar nas páginas.")
