# -*- coding: utf-8 -*-
import os
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import streamlit_authenticator as stauth

# -------------------- Config inicial --------------------
st.set_page_config(
    page_title="Plataforma de Metano OGMP 2.0 - L5",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_dotenv()

# -------------------- Background tech (orbits) --------------------
def apply_tech_bg():
    st.markdown("""
    <style>
    .stApp { background: none !important; }
    .stApp {
      background-color: #0a1b3a;
      background-image:
        radial-gradient(1200px 800px at 75% 40%, rgba(70,115,255,0.18), rgba(0,0,0,0) 60%),
        radial-gradient(900px 600px at 10% 80%, rgba(0,240,255,0.12), rgba(0,0,0,0) 60%),
        url("data:image/svg+xml;utf8,\
        <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'>\
          <defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>\
            <stop offset='0%' stop-color='%23A7C8FF' stop-opacity='0.35'/>\
            <stop offset='100%' stop-color='%2300E5FF' stop-opacity='0.15'/>\
          </linearGradient></defs>\
          <g fill='none' stroke='url(%23g)' stroke-width='1.2'>\
            <path d='M-200,700 C300,400 900,420 1800,200'/>\
            <path d='M-200,820 C420,520 1020,540 1800,360'/>\
            <path d='M-200,580 C260,320 880,340 1800,140'/>\
            <path d='M-200,460 C200,260 820,280 1800,60'/>\
          </g>\
          <g fill='none' stroke='%239bb8ff' stroke-opacity='0.12' stroke-width='0.8'>\
            <circle cx='1250' cy='320' r='220'/>\
            <circle cx='1250' cy='320' r='320'/>\
          </g>\
        </svg>");
      background-repeat: no-repeat, no-repeat, no-repeat;
      background-position: center center, left bottom, right center;
      background-size: cover, 1400px 900px, 100% 100%;
    }
    .stApp::before{
      content:""; position: fixed; inset:0;
      background: linear-gradient(120deg, rgba(7,18,45,0.90) 0%, rgba(14,36,82,0.88) 50%, rgba(17,44,95,0.90) 100%);
      z-index:0; pointer-events:none;
    }
    .block-container, [data-testid="stSidebar"], header { position: relative; z-index:1; }
    </style>
    """, unsafe_allow_html=True)

apply_tech_bg()

# -------------------- Estilos globais --------------------
st.markdown("""
<style>
header[data-testid="stHeader"]{display:none;}
div[data-testid="stToolbar"]{display:none!important;}
#MainMenu{visibility:hidden;}
button[kind="header"]{display:none!important;}

:root{
  --dap-primary:#0b2b5c;
  --dap-accent:#2b8cff;
  --card:#ffffffdd;
  --border:#e6ebf2;
  --shadow:0 18px 60px rgba(20,40,120,.18);
  --radius:20px;
}
.block-container{padding-top:2.2rem; max-width:1200px;}

.hero-eyebrow{
  display:inline-block; font-size:13px; letter-spacing:.18em; text-transform:uppercase;
  padding:6px 10px; border:1px solid #2a4f86; border-radius:999px;
  background:rgba(255,255,255,.08); color:#dbeafe;
}
.hero-title{margin:14px 0 8px 0; line-height:1.1; font-size:44px; font-weight:800; color:#fff;}
.hero-sub{font-size:17px; color:#d6e3ff; max-width:600px}
.hero-bullets{margin:16px 0 24px 0; padding:0; list-style:none}
.hero-bullets li{margin:6px 0; color:#d6e3ff}
.hero-bullets li::before{content:"•"; margin-right:8px; color:#8ec1ff; font-weight:700}

.cta-row{display:flex; gap:12px; margin:18px 0 0 0}
.btn-primary{display:inline-block; padding:10px 16px; border-radius:12px;
  background:var(--dap-accent); color:#fff; font-weight:700; text-decoration:none;}
.btn-ghost{display:inline-block; padding:10px 16px; border-radius:12px;
  background:transparent; color:#cfe2ff; border:1px solid rgba(255,255,255,.28); text-decoration:none;}

.login-card{
  padding:28px; border-radius:var(--radius);
  background: var(--card);
  -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
  border:1px solid var(--border); box-shadow: var(--shadow);
  color:#0f172a;
}
.login-title{font-size:18px; margin:0 0 14px 0; color:#eef3ff; font-weight:700}

/* ========= Labels e textos brancos/visíveis ========= */
.lang-row, .lang-row * { color:#ffffff !important; }          /* toggle "English" */
#login label, #login [data-testid="stWidgetLabel"]{
  display:inline-block !important; visibility:visible !important; opacity:1 !important;
  color:#ffffff !important; font-weight:600 !important;
}
#login input::placeholder { color:#cfe1ff !important; opacity:1; }
.login-note { color:#e8f0ff !important; opacity:.95; }
/* ==================================================== */

.lang-row{position:absolute; top:16px; left:16px; opacity:.95}

.footer{
  position:fixed; left:0; right:0; bottom:0; padding:8px 16px;
  background:rgba(15,25,50,.6); backdrop-filter: blur(8px);
  border-top:1px solid rgba(255,255,255,.12);
  font-size:12px; color:#d7e6ff; display:flex; gap:12px;
  justify-content:space-between; align-items:center; z-index:9999;
}
.footer a{color:#9fd0ff; text-decoration:none}
</style>
""", unsafe_allow_html=True)

# -------------------- i18n --------------------
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

# -------------------- Sidebar visibility --------------------
def hide_sidebar():
    st.markdown("<style>[data-testid='stSidebar']{display:none!important;}</style>", unsafe_allow_html=True)
def show_sidebar():
    st.markdown("<style>[data-testid='stSidebar']{display:flex!important;}</style>", unsafe_allow_html=True)

# -------------------- Authenticator --------------------
def build_authenticator() -> stauth.Authenticate:
    with open("auth_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=SafeLoader)
    return stauth.Authenticate(
        config["credentials"], config["cookie"]["name"],
        config["cookie"]["key"], config["cookie"]["expiry_days"]
    )
authenticator = build_authenticator()
hide_sidebar()

# -------------------- Layout --------------------
left, right = st.columns([1.25,1], gap="large")
with left:
    for cand in ("dapatlas.jpeg", "dapatlas.png", "logo.png", "logo.jpeg"):
        if Path(cand).exists():
            st.image(Image.open(cand), width=200)
            break
    st.markdown(f'<div class="hero-eyebrow">{t["eyebrow"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{t["subtitle"]}</div>', unsafe_allow_html=True)
    st.markdown(f"<ul class='hero-bullets'><li>{t['bul1']}</li><li>{t['bul2']}</li><li>{t['bul3']}</li></ul>", unsafe_allow_html=True)
    st.markdown(f"<div class='cta-row'><a class='btn-primary' href='#login'>{t['cta_login']}</a><a class='btn-ghost' href='mailto:support@dapsistemas.com'>{t['cta_about']}</a></div>", unsafe_allow_html=True)

with right:
    st.markdown(f"<div id='login' class='login-card'><div class='login-title'>{t['secure_access']}</div>", unsafe_allow_html=True)

    # Labels PT; se a versão suportar, usa fields; senão, fallback mantém rótulos brancos via CSS
    fields = {"Form name": "", "Username": "Usuário", "Password": "Senha", "Login": "Entrar"}
    try:
        name, auth_status, username = authenticator.login("main", fields=fields)
    except TypeError:
        name, auth_status, username = authenticator.login("main")

    st.markdown(f"<div class='login-note'>{t['confidential']}</div></div>", unsafe_allow_html=True)
    # --- forçar cores (visíveis) dos rótulos e textos do login ---
st.markdown("""
<style>
/* rótulo do toggle "English" */
.lang-row, .lang-row * { color:#ffffff !important; }

/* rótulos "Usuário" e "Senha" */
#login label,
#login [data-testid="stWidgetLabel"],
#login [data-testid="stWidgetLabel"] * {
  color:#ffffff !important;
  visibility:visible !important;
  opacity:1 !important;
  font-weight:600 !important;
}

/* texto de ajuda abaixo do card */
#login .login-note { color:#e8f0ff !important; opacity:.95 !important; }

/* placeholders dos campos (se aparecerem) */
#login input::placeholder { color:#cfe1ff !important; opacity:1 !important; }

/* se ainda não aparecer por alguma classe obscura, descomente a linha abaixo (modo “martelo”)
#login, #login * { color:#ffffff !important; }
*/
</style>
""", unsafe_allow_html=True)




# -------------------- Pós-login --------------------
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

# -------------------- Footer --------------------
APP_VERSION = os.getenv("APP_VERSION","v1.0.0")
ENV_LABEL = "Produção"
st.markdown(f"""
<div class="footer">
  <div>📦 DAP ATLAS · {APP_VERSION} · Ambiente: {ENV_LABEL}</div>
  <div>🔒 {t["internal_use"]} · <a href="mailto:support@dapsistemas.com">{t["support"]}</a> · 
       <a href="https://example.com/privacidade" target="_blank">{t["privacy"]}</a></div>
</div>
""", unsafe_allow_html=True)
