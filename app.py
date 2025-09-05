# app.py
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# =============================================================================
# Configuração básica
# =============================================================================
st.set_page_config(
    page_title="Plataforma de Metano OGMP 2.0 - L5",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_dotenv()

# ---- CSS: esconder cabeçalho superior (Share/Star/GitHub/•••) ----
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] { display: none; }
    div[data-testid="stToolbar"]   { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

PAGES_DIR = Path("pages")

# =============================================================================
# Util: localizar a página de Estatísticas (nomes tolerantes)
# =============================================================================
CANDIDATE_NAMES = [
    "1_📊_Estatisticas_Gerais.py",
    "1_Estatisticas_Gerais.py",
    "1_estatisticas_gerais.py",
    "Estatisticas_Gerais.py",
    "estatisticas.py",
    "estatisticas_gerais.py",
]

def find_stats_page() -> Optional[Path]:
    if not PAGES_DIR.exists():
        return None
    for name in CANDIDATE_NAMES:
        p = PAGES_DIR / name
        if p.exists():
            return p
    for p in PAGES_DIR.glob("*.py"):
        if "estat" in p.name.lower():
            return p
    for p in PAGES_DIR.glob("*.py"):
        return p
    return None

# =============================================================================
# CSS: mostrar/ocultar o nav de páginas na sidebar
# =============================================================================
def _set_nav_visibility(show: bool) -> None:
    st.markdown(
        f"""
        <style>
        div[data-testid="stSidebarNav"] {{
            display: {"flex" if show else "none"} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# =============================================================================
# Autenticação (streamlit-authenticator)
# =============================================================================
def build_authenticator() -> stauth.Authenticate:
    with open("auth_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=SafeLoader)

    return stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

authenticator = build_authenticator()

# =============================================================================
# Tela inicial: Logo + Login lado a lado
# =============================================================================
left, right = st.columns([1, 1], gap="large")

with left:
    logo_candidates = [
        Path("dapatlas.jpeg"),
        Path("assets/dapatlas.jpeg"),
        Path(__file__).parent / "dapatlas.jpeg",
        Path(__file__).parent / "assets/dapatlas.jpeg",
    ]
    logo_path = next((p for p in logo_candidates if p.exists()), None)

    if logo_path:
        st.image(Image.open(logo_path), width=260)
    st.markdown(
        """
        <h1 style="margin-top:12px;font-size:26px;color:#003366;">
            PLATAFORMA DE MONITORAMENTO DE METANO POR SATÉLITE
        </h1>
        """,
        unsafe_allow_html=True,
    )

with right:
    try:
        name, auth_status, username = authenticator.login(location="main")
    except Exception:
        name, auth_status, username = authenticator.login("Login", "main")

# =============================================================================
# Esconde/mostra o menu de páginas conforme status
# =============================================================================
if st.session_state.get("authentication_status") is True:
    _set_nav_visibility(True)
else:
    _set_nav_visibility(False)

# =============================================================================
# Mensagens de login
# =============================================================================
if auth_status is False:
    st.error("Usuário ou senha inválidos.")
elif auth_status is None:
    st.info("Por favor, faça login para continuar.")

# =============================================================================
# Área autenticada
# =============================================================================
if auth_status:
    st.sidebar.success(f"Logado como: {name}")
    try:
        authenticator.logout(location="sidebar")
    except Exception:
        authenticator.logout("Sair", "sidebar")

    # Redirecionar automaticamente para Estatísticas (se existir)
    stats_page = find_stats_page()
    if stats_page and stats_page.exists():
        stats_page_str = str(stats_page).replace("\\", "/")
        try:
            st.switch_page(stats_page_str)
            st.stop()
        except Exception:
            st.success("Login OK. Clique para ir às Estatísticas Gerais.")
            st.sidebar.page_link(stats_page_str, label="Ir para Estatísticas Gerais")
    else:
        st.warning(
            "Não encontrei a página de **Estatísticas** em `pages/`.\n\n"
            "Crie, por exemplo, `pages/1_Estatisticas_Gerais.py`."
        )

    # -------------------------------------------------------------------------
    # (Opcional) Conexão Snowflake via secrets/variáveis de ambiente
    # -------------------------------------------------------------------------
    use_sf = st.sidebar.checkbox("Conectar Snowflake (read-only)", value=False)
    if use_sf:
        try:
            import snowflake.connector  # type: ignore
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
    # Links seguros na sidebar (aparecem só se o arquivo existir)
    # -------------------------------------------------------------------------
    def safe_page_link(path: str, label: str) -> None:
        p = Path(path)
        if p.exists():
            st.sidebar.page_link(str(p).replace("\\", "/"), label=label)

    safe_page_link("pages/1_📊_Estatisticas_Gerais.py", "Estatísticas Gerais")
    safe_page_link("pages/2_🗺️_Geoportal.py", "Geoportal")
    safe_page_link("pages/3_📄_Relatorio_OGMP_2_0.py", "Relatório OGMP 2.0")
    safe_page_link("pages/4_🛰️_Agendamento_de_Imagens.py", "Agendamento de Imagens")

    st.markdown("> Use o menu à esquerda para navegar nas páginas.")
