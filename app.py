# -*- coding: utf-8 -*-
import os
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import streamlit_authenticator as stauth

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
st.set_page_config(
    page_title="Plataforma de Metano OGMP 2.0 - L5",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_dotenv()

# ------------------------------------------------------------
# CSS: TUDO branco, TODO texto preto
# ------------------------------------------------------------
st.markdown("""
<style>
/* remove header/toolbars */
header[data-testid="stHeader"]{display:none;}
div[data-testid="stToolbar"]{display:none!important;}
#MainMenu{visibility:hidden;}
button[kind="header"]{display:none!important;}

/* fundo absolutamente branco em tudo */
html, body, .stApp, [data-testid="stAppViewContainer"],
.block-container, [data-testid="stSidebar"], header, footer {
  background: #ffffff !important;
  color: #111111 !important;
}

/* se ficou algum overlay antigo */
.stApp::before, .stApp::after, body::before, body::after { content:none !important; background:none !important; }

/* todo texto preto por padrão */
* { color:#111111 !important; }

/* links pretos (sublinhados para acessibilidade) */
a { color:#111111 !important; text-decoration: underline; }

/* inputs/brancos, borda neutra, texto preto */
input, textarea, select, .stTextInput input, .stPassword input {
  background:#ffffff !important; color:#111111 !important;
  border:1px solid #d0d7e2 !important; border-radius:10px !important;
}
input::placeholder, textarea::placeholder { color:#444444 !important; opacity:1 !important; }

/* cards e elementos do login */
.login-card, .login-title {
  background:#ffffff !important; color:#111111 !important;
}
.login-card{
  padding:24px; border:1px solid #e7e7e7; border-radius:16px;
  box-shadow: 0 8px 24px rgba(0,0,0,.06);
}

/* bullet list e títulos */
.hero-eyebrow{ display:inline-block; font-size:12px; letter-spacing:.18em;
  text-transform:uppercase; padding:6px 10px; border:1px solid #111; border-radius:999px; }
.hero-title{ margin:14px 0 8px 0; line-height:1.1; font-size:44px; font-weight:800; }
.hero-sub{ font-size:16px; color:#111 !important; max-width:640px; }
.hero-bullets{ margin:16px 0 24px 0; padding-left:18px; }
.hero-bullets li{ margin:6px 0; }

/* botões simples brancos com contorno preto */
.btn-primary, .btn-ghost{
  display:inline-block; padding:10px 16px; border-radius:10px; text-decoration:none !important;
  background:#ffffff; color:#111111 !important; border:1px solid #111111;
}
.cta-row{ display:flex; gap:12px; margin-top:16px }

/* toggle idioma visível/preto */
.lang-row{ position:absolute; top:16px; left:16px; }

/* footer claro com divisória suave */
.footer{
  position:fixed; left:0; right:0; bottom:0; padding:8px 16px;
  background:#ffffff; border-top:1px solid #ececec; color:#111111;
  display:flex; justify-content:space-between; align-items:center; font-size:12px; z-index:999;
}

/* layout container */
.block-container{ padding-top:2rem; max-width:1200px; }

/* esconder sidebar até logar */
[data-testid="stSidebar"]{ display:none; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# i18n
# ------------------------------------------------------------
if "lang" not in st.session_state: st.session_state.lang = "pt"
st.markdown('<div class="lang-row">', unsafe_allow_html=True)
lang_toggle = st.toggle("English", value=(st.session_state.lang=="en"), key="lang_toggle")
st.markdown('</div>', unsafe_allow_html=True)
st.session_state.lang = "en" if lang_toggle else "pt"

TXT = {
  "pt": {"eyebrow":"Plataforma OGMP 2.0 – L5","title":"PLATAFORMA DE MONITORAMENTO DE METANO POR SATÉLITE",
         "subtitle":"Detecção, quantificação e insights acionáveis a partir de dados multissatélite. Confiabilidade de nível industrial.",
         "bul1":"Detecção e priorização de eventos","bul2":"Relatórios OGMP 2.0 e auditoria","bul3":"Geoportal com mapas, KPIs e séries históricas",
         "cta_login":"Login","cta_about":"Saiba mais","secure_access":"Acesso Seguro","login_hint":"Por favor, faça login para continuar.",
         "bad_credentials":"Usuário ou senha inválidos.","confidential":"Acesso restrito. Conteúdo confidencial.",
         "logged_as":"Logado como","support":"Suporte","privacy":"Privacidade","internal_use":"Uso interno"},
  "en": {"eyebrow":"OGMP 2.0 Platform – L5","title":"SATELLITE METHANE MONITORING PLATFORM",
         "subtitle":"Detection, quantification, and actionable insights from multi-satellite data. Industrial-grade reliability.",
         "bul1":"Event detection & prioritization","bul2":"OGMP 2.0 reporting & audit","bul3":"Geoportal with maps, KPIs, time series",
         "cta_login":"Login","cta_about":"Learn more","secure_access":"Secure Access","login_hint":"Please sign in to continue.",
         "bad_credentials":"Invalid username or password.","confidential":"Restricted access. Confidential content.",
         "logged_as":"Signed in as","support":"Support","privacy":"Privacy","internal_use":"Internal use"}
}
t = TXT[st.session_state.lang]

# ------------------------------------------------------------
# Sidebar show/hide helpers
# ------------------------------------------------------------
def show_sidebar():
    st.markdown("<style>[data-testid='stSidebar']{display:flex!important;}</style>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Authenticator
# ------------------------------------------------------------
def build_authenticator() -> stauth.Authenticate:
    with open("auth_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=SafeLoader)
    return stauth.Authenticate(
        config["credentials"], config["cookie"]["name"],
        config["cookie"]["key"], config["cookie"]["expiry_days"]
    )
authenticator = build_authenticator()

# ------------------------------------------------------------
# Layout
# ------------------------------------------------------------
left, right = st.columns([1.25,1], gap="large")

with left:
    for cand in ("dapatlas.png","dapatlas.jpeg","logo.png","logo.jpeg"):
        if Path(cand).exists():
            st.image(Image.open(cand), width=200)
            break
    st.markdown(f'<div class="hero-eyebrow">{t["eyebrow"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{t["subtitle"]}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <ul class='hero-bullets'>
      <li>{t['bul1']}</li>
      <li>{t['bul2']}</li>
      <li>{t['bul3']}</li>
    </ul>""", unsafe_allow_html=True)
    st.markdown(f"<div class='cta-row'><a class='btn-primary' href='#login'>{t['cta_login']}</a><a class='btn-ghost' href='mailto:support@dapsistemas.com'>{t['cta_about']}</a></div>", unsafe_allow_html=True)

with right:
    st.markdown(f"<div id='login' class='login-card'><div class='login-title'>{t['secure_access']}</div>", unsafe_allow_html=True)
    # Labels em PT; botão "Entrar"
    fields = {"Form name": "", "Username": "Usuário", "Password": "Senha", "Login": "Entrar"}
    try:
        name, auth_status, username = authenticator.login("main", fields=fields)
    except TypeError:
        name, auth_status, username = authenticator.login("main")
    st.markdown(f"<div class='login-note'>{t['confidential']}</div></div>", unsafe_allow_html=True)

# Estado do login
if 'auth_status' in locals():
    if auth_status is False:
        st.error(t["bad_credentials"])
    elif auth_status is None:
        st.info(t["login_hint"])
    if auth_status:
        show_sidebar()
        st.sidebar.success(f'{t["logged_as"]}: {name}')
        try:
            authenticator.logout(location="sidebar")
        except Exception:
            authenticator.logout("Sair", "sidebar")

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
APP_VERSION = os.getenv("APP_VERSION","v1.0.0")
ENV_LABEL = "Produção"
st.markdown(f"""
<div class="footer">
  <div>DAP ATLAS · {APP_VERSION} · Ambiente: {ENV_LABEL}</div>
  <div>{t["internal_use"]} · <a href="mailto:support@dapsistemas.com">{t["support"]}</a> · 
       <a href="https://example.com/privacidade" target="_blank">{t["privacy"]}</a></div>
</div>
""", unsafe_allow_html=True)
