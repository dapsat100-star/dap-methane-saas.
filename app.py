# app.py
# -*- coding: utf-8 -*-

# =============================================================================
# Imports
# =============================================================================
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
# Config inicial
# =============================================================================
st.set_page_config(
    page_title="Plataforma de Metano OGMP 2.0 - L5",
    page_icon="assets/favicon.png",     # PNG 32x32 em assets/
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_dotenv()

# =============================================================================
# Forçar embed=true (sem API experimental)
# =============================================================================
st.markdown(
    """
    <script>
    (function () {
      try {
        var url = new URL(window.location.href);
        if (url.hostname.endsWith("streamlit.app") && url.searchParams.get("embed") !== "true") {
          url.searchParams.set("embed", "true");
          window.location.replace(url.toString());
        }
      } catch (e) { }
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# Estilos globais
# =============================================================================
st.markdown(
    """
    <style>
    header[data-testid="stHeader"]{display:none;}
    div[data-testid="stToolbar"]{display:none !important;}
    #MainMenu{visibility:hidden;}
    button[kind="header"]{display:none !important;}

    :root{
      --dap-primary:#003366;
      --dap-accent:#0ea5e9;
      --border:#eef0f3;
      --card-shadow:0 8px 30px rgba(0,0,0,.08);
    }
    .login-card{
      padding:28px;border-radius:18px;background:#fff;
      box-shadow:var(--card-shadow);border:1px solid var(--border);
    }
    .login-title{
      font-size:18px;margin:0 0 16px 0;color:#0f172a;font-weight:600
    }
    .footer{
      position:fixed;left:0;right:0;bottom:0;padding:6px 16px;
      background:rgba(255,255,255,.85);backdrop-filter:saturate(180%) blur(8px);
      border-top:1px solid var(--border);font-size:12px;color:#334155;
      display:flex;gap:12px;justify-content:space-between;align-items:center;
      z-index:9999;
    }
    .footer a{color:var(--dap-accent);text-decoration:none}
    </style>
    """,
    unsafe_allow_html=True,
)

PAGES_DIR = Path("pages")
APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")
ENV = os.getenv("APP_ENV", "producao").lower()
ENV_LABEL = "Produção" if ENV == "producao" else "Homologação"

# =============================================================================
# i18n (PT/EN)
# =============================================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"
lang_toggle = st.toggle("English", value=(st.session_state.lang == "en"))
st.session_state.lang = "en" if lang_toggle else "pt"

TXT = {
    "pt": {
        "title": "PLATAFORMA DE MONITORAMENTO DE METANO POR SATÉLITE",
        "secure_access": "Acesso Seguro",
        "login_hint": "Por favor, faça login para continuar.",
        "bad_credentials": "Usuário ou senha inválidos.",
        "stats_missing": "Não encontrei a página de **Estatísticas** em `pages/`.\n\nCrie, por exemplo, `pages/1_Estatisticas_Gerais.py`.",
        "go_stats": "Ir para Estatísticas Gerais",
        "nav_hint": "Use o menu à esquerda para navegar nas páginas.",
        "confidential": "Acesso restrito. Conteúdo confidencial. Ao prosseguir, você concorda com os Termos de Uso e a Política de Privacidade.",
        "sf_connect": "Conectar Snowflake (read-only)",
        "sf_ok": "Conectado ao Snowflake ✅",
        "sf_err": "Falha na conexão Snowflake",
        "logged_as": "Logado como",
        "support": "Suporte",
        "privacy": "Privacidade",
        "internal_use": "Uso interno",
    },
    "en": {
        "title": "SATELLITE METHANE MONITORING PLATFORM",
        "secure_access": "Secure Access",
        "login_hint": "Please sign in to continue.",
        "bad_credentials": "Invalid username or password.",
        "stats_missing": "Could not find the **Statistics** page in `pages/`.\n\nCreate e.g. `pages/1_Estatisticas_Gerais.py`.",
        "go_stats": "Go to General Statistics",
        "nav_hint": "Use the left menu to navigate between pages.",
        "confidential": "Restricted access. Confidential content. By proceeding, you agree to the Terms of Use and Privacy Policy.",
        "sf_connect": "Connect Snowflake (read-only)",
        "sf_ok": "Connected to Snowflake ✅",
        "sf_err": "Snowflake connection failed",
        "logged_as": "Signed in as",
        "support": "Support",
        "privacy": "Privacy",
        "internal_use": "Internal use",
    },
}
t = TXT[st.session_state.lang]

# =============================================================================
# Util
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
# Autenticação
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
# Tela inicial
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
        f'<h1 style="margin-top:12px;font-size:26px;color:var(--dap-primary);">{t["title"]}</h1>',
        unsafe_allow_html=True,
    )
    if not st.session_state.get("authentication_status"):
        st.info(t["confidential"])

with right:
    st.markdown(f'<div class="login-card"><div class="login-title">{t["secure_access"]}</div>', unsafe_allow_html=True)
    try:
        name, auth_status, username = authenticator.login(location="main")
    except Exception:
        name, auth_status, username = authenticator.login("Login", "main")
    st.markdown("</div>", unsafe_allow_html=True)

_set_nav_visibility(bool(st.session_state.get("authentication_status")))

if auth_status is False:
    st.error(t["bad_credentials"])
elif auth_status is None:
    st.info(t["login_hint"])

# =============================================================================
# Área autenticada
# =============================================================================
if auth_status:
    st.sidebar.success(f'{t["logged_as"]}: {name}')
    try:
        authenticator.logout(location="sidebar")
    except Exception:
        authenticator.logout("Sair", "sidebar")

    stats_page = find_stats_page()
    if stats_page and stats_page.exists():
        target = str(stats_page).replace("\\", "/")
        try:
            st.switch_page(target)
            st.stop()
        except Exception:
            st.success("Login OK.")
            st.sidebar.page_link(target, label=t["go_stats"])
    else:
        st.warning(t["stats_missing"])

    # Snowflake (opcional)
    use_sf = st.sidebar.checkbox(t["sf_connect"], value=False)
    if use_sf:
        try:
            import snowflake.connector  # type: ignore
            _conn = snowflake.connector.connect(
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA"),
            )
            st.sidebar.success(t["sf_ok"])
        except Exception as e:
            st.sidebar.error(f'{t["sf_err"]}: {e}')

    def safe_page_link(path: str, label: str) -> None:
        p = Path(path)
        if p.exists():
            st.sidebar.page_link(str(p).replace("\\", "/"), label=label)

    safe_page_link("pages/1_📊_Estatisticas_Gerais.py", "Estatísticas Gerais")
    safe_page_link("pages/2_🗺️_Geoportal.py", "Geoportal")
    safe_page_link("pages/3_📄_Relatorio_OGMP_2_0.py", "Relatório OGMP 2.0")
    safe_page_link("pages/4_🛰️_Agendamento_de_Imagens.py", "Agendamento de Imagens")

    st.markdown(f'> {t["nav_hint"]}')

# =============================================================================
# Rodapé customizado
# =============================================================================
st.markdown(
    f"""
    <div class="footer">
      <div>📦 DAP ATLAS · {APP_VERSION} · Ambiente: {ENV_LABEL}</div>
      <div>🔒 {t["internal_use"]} · <a href="mailto:support@dapsistemas.com">{t["support"]}</a> · <a href="https://example.com/privacidade" target="_blank">{t["privacy"]}</a></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# CSS extra (fallback para esconder "Manage app"/badges)
# =============================================================================
st.markdown("""
<style>
footer, [data-testid="stFooter"]{display:none !important;visibility:hidden !important;}
.stApp a[href*="streamlit.io"], .stApp a[href*="share.streamlit.io"],
.stApp a[href*="cloud"], .stApp a[href*="manage"],
.stApp a[aria-label*="Manage app"], .stApp a[title*="Manage app"]{
  display:none !important; visibility:hidden !important; pointer-events:none !important;
}
div[class*="stDeployButton"], [data-testid="stStatusWidget"], [data-testid="stDecoration"]{
  display:none !important; visibility:hidden !important; pointer-events:none !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
footer, [data-testid="stFooter"] {
    display: none !important;
    visibility: hidden !important;
}
</style>
""", unsafe_allow_html=True)
