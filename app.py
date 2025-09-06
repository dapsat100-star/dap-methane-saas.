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
    page_icon="favicon.png",       # <-- favicon na MESMA pasta
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_dotenv()

# =============================================================================
# Forçar embed=true com JS (oculta chrome do Streamlit Cloud)
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
      } catch (e) {}
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# Estilos globais (visual premium)
# =============================================================================
st.markdown(
    """
    <style>
    header[data-testid="stHeader"]{display:none;}
    div[data-testid="stToolbar"]{display:none !important;}
    #MainMenu{visibility:hidden;}
    button[kind="header"]{display:none !important;}

    :root{
      --dap-primary:#0b2b5c;
      --dap-accent:#2b8cff;
      --ink:#0f172a;
      --muted:#475569;
      --card:#ffffffdd;
      --border:#e6ebf2;
      --shadow:0 18px 60px rgba(20,40,120,.18);
      --radius:20px;
    }

    .stApp{
      background: linear-gradient(140deg,#0f2d55 0%, #123a6e 45%, #144180 100%);
      color:#e5eefc;
    }
    .block-container{padding-top:2.2rem; max-width:1200px;}

    .hero-eyebrow{
      display:inline-block; font-size:13px; letter-spacing:.18em; text-transform:uppercase;
      padding:6px 10px; border:1px solid #2a4f86; border-radius:999px;
      background:rgba(255,255,255,.06);
    }
    .hero-title{margin:14px 0 8px 0; line-height:1.1; font-size:44px; font-weight:800; color:#fff;}
    .hero-sub{font-size:17px; color:#d6e3ff; max-width:600px}
    .hero-bullets{margin:16px 0 24px 0; padding:0; list-style:none}
    .hero-bullets li{margin:6px 0; color:#d6e3ff}
    .hero-bullets li::before{content:"•"; margin-right:8px; color:#8ec1ff; font-weight:700}

    .cta-row{display:flex; gap:12px; margin:18px 0 0 0}
    .btn-primary{display:inline-block; padding:10px 16px; border-radius:12px;
      background:var(--dap-accent); color:#fff; font-weight:700; text-decoration:none;
      box-shadow:0 8px 24px rgba(43,140,255,.35);}
    .btn-ghost{display:inline-block; padding:10px 16px; border-radius:12px;
      background:transparent; color:#cfe2ff; border:1px solid rgba(255,255,255,.28); text-decoration:none;}

    .login-card{
      padding:28px; border-radius:var(--radius);
      background: var(--card);
      -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
      border:1px solid var(--border); box-shadow: var(--shadow);
      color:#0f172a;
    }
    .login-title{font-size:18px; margin:0 0 14px 0; color:#0f172a; font-weight:700}
    .login-note{font-size:12px; color:#475569; margin-top:6px}

    .lang-row{position:absolute; top:16px; left:16px; opacity:.85}

    .footer{
      position:fixed; left:0; right:0; bottom:0; padding:8px 16px;
      background:rgba(15,25,50,.6); backdrop-filter: blur(8px);
      border-top:1px solid rgba(255,255,255,.12);
      font-size:12px; color:#d7e6ff; display:flex; gap:12px;
      justify-content:space-between; align-items:center; z-index:9999;
    }
    .footer a{color:#9fd0ff; text-decoration:none}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- background image opcional (MESMA pasta do app) ---
for cand in ("hero-bg.jpg", "hero-bg.png", "fundo.jpg", "fundo.png"):
    if Path(cand).exists():
        st.markdown(
            f"""
            <style>
            .stApp {{
              background-image:url('{cand}');
              background-size:cover; background-position:center; background-attachment:fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        break

# =============================================================================
# Variáveis globais
# =============================================================================
PAGES_DIR = Path("pages")
APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")
ENV = os.getenv("APP_ENV", "producao").lower()
ENV_LABEL = "Produção" if ENV == "producao" else "Homologação"

# =============================================================================
# i18n (PT/EN)
# =============================================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

st.markdown('<div class="lang-row">', unsafe_allow_html=True)
lang_toggle = st.toggle("English", value=(st.session_state.lang == "en"), key="lang_toggle")
st.markdown('</div>', unsafe_allow_html=True)
st.session_state.lang = "en" if lang_toggle else "pt"

TXT = {
    "pt": {
        "eyebrow": "Plataforma OGMP 2.0 – L5",
        "title": "PLATAFORMA DE MONITORAMENTO DE METANO POR SATÉLITE",
        "subtitle": "Detecção, quantificação e insights acionáveis a partir de dados multissatélite. Confiabilidade de nível industrial.",
        "bul1": "Detecção e priorização de eventos",
      
        "cta_login": "Login",
        "cta_about": "Saiba mais",
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
        "eyebrow": "OGMP 2.0 Platform – L5",
        "title": "SATELLITE METHANE MONITORING PLATFORM",
        "subtitle": "Detection, quantification, and actionable insights from multi-satellite data. Industrial-grade reliability.",
        "bul1": "Event detection & prioritization",
        "bul2": "OGMP 2.0 reporting & audit",
        "bul3": "Geoportal with maps, KPIs, time series",
        "cta_login": "Login",
        "cta_about": "Learn more",
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
# Utils
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
# Layout principal (split-screen)
# =============================================================================
left, right = st.columns([1.25, 1], gap="large")

with left:
    # Logo da MESMA pasta
    logo = None
    for cand in ("dapatlas.jpeg", "dapatlas.png", "logo.png", "logo.jpeg"):
        if Path(cand).exists():
            logo = Image.open(cand)
            break
    if logo:
        st.image(logo, width=200)

    st.markdown('<div class="hero-eyebrow">'+t["eyebrow"]+'</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{t["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <ul class="hero-bullets">
          <li>{t["bul1"]}</li>
          <li>{t["bul2"]}</li>
          <li>{t["bul3"]}</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="cta-row">
          <a class="btn-primary" href="#login">{t["cta_login"]}</a>
          <a class="btn-ghost" href="mailto:support@dapsistemas.com">{t["cta_about"]}</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(f'<div id="login" class="login-card"><div class="login-title">{t["secure_access"]}</div>', unsafe_allow_html=True)
    name, auth_status, username = authenticator.login("main")   # versão atual do streamlit_authenticator
    st.markdown(f'<div class="login-note">{t["confidential"]}</div></div>', unsafe_allow_html=True)

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

    # Links seguros (se existirem)
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
# Rodapé
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
# Remover branding do Streamlit (defensivo)
# =============================================================================
st.markdown("""
<style>
footer, [data-testid="stFooter"], .section-footer,
.viewerBadge_container__, .viewerBadge_link__,
[data-testid="stStatusWidget"], [data-testid="stDecoration"],
div[class*="stDeployButton"], div[class*="floating"] {
  display: none !important; visibility: hidden !important; opacity: 0 !important;
  pointer-events: none !important;
}
html, body, .stApp { padding-bottom: 0 !important; margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)

