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
# CSS: fundo cinza claro (#f5f5f5), texto preto
# ------------------------------------------------------------
st.markdown("""
<style>
/* remove header/toolbars */
header[data-testid="stHeader"]{display:none;}
div[data-testid="stToolbar"]{display:none!important;}
#MainMenu{visibility:hidden;}
button[kind="header"]{display:none!important;}

/* fundo e texto padrão */
html, body, .stApp, [data-testid="stAppViewContainer"],
.block-container, [data-testid="stSidebar"], header, footer {
  background: #f5f5f5 !important;   /* CINZA CLARO */
  color: #111111 !important;
}

/* kill qualquer overlay antigo */
.stApp::before, .stApp::after, body::before, body::after { 
  content:none !important; 
  background:none !important; 
}

/* todo texto preto por padrão */
* { color:#111111 !important; }

/* links pretos (sublinhados) */
a { color:#111111 !important; text-decoration: underline; }

/* inputs: brancos, borda suave, texto preto */
input, textarea, select, .stTextInput input, .stPassword input {
  background:#ffffff !important; 
  color:#111111 !important;
  border:1px solid #d0d7e2 !important; 
  border-radius:10px !important;
}
input::placeholder, textarea::placeholder { 
  color:#444444 !important; 
  opacity:1 !important; 
}

/* card do login */
.login-card{
  padding:24px; border:1px solid #e7e7e7; border-radius:16px;
  box-shadow: 0 8px 24px rgba(0,0,0,.06);
  background:#ffffff !important;
}
.login-title{ font-size:18px; margin:0 0 14px 0; font-weight:700; }

/* hero area */
.hero-eyebrow{ display:inline-block; font-size:12px; letter-spacing:.18em;
  text-transform:uppercase; padding:6px 10px; border:1px solid #111; border-radius:999px; }
.hero-title{ margin:14px 0 8px 0; line-height:1.1; font-size:40px; font-weight:800; }
.hero-sub{ font-size:16px; max-width:640px; }
.hero-bullets{ margin:16px 0 24px 0; padding-left:18px; }
.hero-bullets li{ margin:6px 0; }

/* botões */
.btn-primary, .btn-ghost{
  display:inline-block; padding:10px 16px; border-radius:10px; text-decoration:none !important;
  background:#ffffff; color:#111111 !important; border:1px solid #111111;
}
.cta-row{ display:flex; gap:12px; margin-top:16px }

/* toggle idioma */
.lang-row{ position:absolute; top:16px; left:16px; }

/* footer */
.footer{
  position:fixed; left:0; right:0; bottom:0; padding:8px 16px;
  background:#f5f5f5; border-top:1px solid #ececec; color:#111111;
  display:flex; justify-content:space-between; align-items:center; font-size:12px; z-index:999;
}

/* layout container */
.block-container{ padding-top:2rem; max-width:1200px; }

/* esconder sidebar até logar */
[data-testid="stSidebar"]{ display:none; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# BG “linhas/trilhos” sutil (mantém o cinza)
# ------------------------------------------------------------
st.markdown("""
<style>
/* camada fixa por trás de tudo */
[data-testid="stAppViewContainer"]::before{
  content:"";
  position: fixed; inset: 0;
  z-index: 0; pointer-events: none;
  background-color: #f5f5f5;

  /* SVG embutido (neutro e discreto) */
  background-image: url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'>\
<defs>\
  <radialGradient id='g' cx='50%%' cy='40%%' r='80%%'>\
    <stop offset='0%%' stop-color='%23f7f7f7'/>\
    <stop offset='100%%' stop-color='%23f3f3f3'/>\
  </radialGradient>\\
  <style> .l{stroke:%23999;stroke-opacity:.18;stroke-width:1.2} .d{fill:%23999;fill-opacity:.22} </style>\
</defs>\
<rect width='100%%' height='100%%' fill='url(%23g)'/>\
<g class='grid'>\
  <path class='l' d='M-50,120 C200,80 350,160 520,120 740,65 980,165 1220,110 1420,65 1650,150 1700,120'/>\
  <path class='l' d='M-50,320 C180,280 360,360 560,315 820,255 1020,330 1260,300 1450,280 1650,340 1700,320'/>\
  <path class='l' d='M-50,520 C220,470 380,560 600,515 860,455 1060,540 1300,505 1500,480 1650,560 1700,520'/>\
  <path class='l' d='M-50,720 C220,670 420,760 640,710 900,650 1120,740 1360,700 1540,670 1660,760 1700,720'/>\
  <path class='l' d='M120,0 C160,220 260,300 420,360 640,440 860,420 1080,360 1300,300 1440,220 1500,0'/>\
  <path class='l' d='M0,80 C200,180 360,220 560,220 800,220 1040,160 1280,60 1400,10 1500,-10 1700,10'/>\
</g>\
<g class='nodes'>\
  <circle class='d' cx='200' cy='120' r='2.6'/><circle class='d' cx='520' cy='120' r='2.6'/>\
  <circle class='d' cx='820' cy='255' r='2.6'/><circle class='d' cx='1060' cy='540' r='2.6'/>\
  <circle class='d' cx='1280' cy='60' r='2.6'/><circle class='d' cx='1360' cy='700' r='2.6'/>\
  <circle class='d' cx='420' cy='360' r='2.6'/><circle class='d' cx='600' cy='515' r='2.6'/>\
</g>\
</svg>");
  background-size: cover;
  background-position: center;
  opacity: .45;               /* ajuste a intensidade do desenho (.30 a .60) */
  filter: contrast(103%) brightness(101%);
}

/* gradiente sutil no topo (herói) - opcional */
[data-testid="stAppViewContainer"]::after{
  content:"";
  position: fixed; inset: 0 0 auto 0; height: 28vh;
  pointer-events:none; z-index: 0;
  background: linear-gradient(180deg, rgba(0,0,0,.04), rgba(0,0,0,0));
}

/* garante que o conteúdo fique acima do BG */
.block-container, [data-testid="stSidebar"], header, footer { position: relative; z-index: 1; }
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
    fields = {"Form name": "", "Username": "Usuário", "Password": "Senha", "Login": "Entrar"}
    try:
        name, auth_status, username = authenticator.login("main", fields=fields)
    except TypeError:
        name, auth_status, username = authenticator.login("main")
    st.markdown(f"<div class='login-note'>{t['confidential']}</div></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# UX Kit
# ------------------------------------------------------------
def apply_ux_enhancements():
    st.markdown("""
    <style>
      .pw-eye {
        position:absolute; right:10px; top:50%; transform: translateY(-50%);
        border:0; background:transparent; cursor:pointer; font-size:16px;
        padding:2px; line-height:1;
      }
      .pw-wrap { position:relative; }
      .caps-hint { margin-top:6px; font-size:12px; color:#d00; }
      .remember-row {
        display:flex; align-items:center; gap:8px; font-size:13px;
        margin:6px 0 10px 2px; color:#111;
      }
      .remember-row input[type="checkbox"]{ transform: scale(1.1); }
      @media (max-width: 780px){ .footer{ position: static; } }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <script>
    (function(){
      const root = document.getElementById('login') || document.body;
      function onceReady(fn){
        let tries = 0;
        const iv = setInterval(()=>{
          tries++;
          const u = root.querySelector('input[type="text"]') || document.querySelector('input[type="text"]');
          const p = root.querySelector('input[type="password"]') || document.querySelector('input[type="password"]');
          const btn = root.querySelector('button') || document.querySelector('button[kind="secondary"], button');
          if ((u || p) && btn){ clearInterval(iv); fn({u,p,btn}); }
          if (tries > 25) clearInterval(iv);
        }, 180);
      }
      onceReady(({u,p,btn})=>{
        if (u && !u.placeholder) u.placeholder = "Usuário";
        if (p && !p.placeholder) p.placeholder = "Senha";
        if (u){
          const saved = localStorage.getItem('dap_username') || "";
          if (saved && !u.value) u.value = saved;
          const row = document.createElement('label');
          row.className = 'remember-row';
          row.innerHTML = "<input type='checkbox' id='rememberUser'> <span>Lembrar usuário</span>";
          (u.parentElement?.parentElement || u.parentElement).insertAdjacentElement('afterend', row);
          const cb = row.querySelector('#rememberUser');
          cb.checked = !!saved;
          const store = () => { cb.checked ? localStorage.setItem('dap_username', u.value) : localStorage.removeItem('dap_username'); };
          u.addEventListener('input', store); cb.addEventListener('change', store);
        }
        if (p){
          if (!p.parentElement.classList.contains('pw-wrap')) p.parentElement.classList.add('pw-wrap');
          const eye = document.createElement('button');
          eye.type = 'button'; eye.className = 'pw-eye';
          eye.setAttribute('aria-label','Mostrar/ocultar senha');
          eye.textContent = '👁';
          p.parentElement.appendChild(eye);
          eye.addEventListener('click', ()=>{ p.type = (p.type === 'password' ? 'text' : 'password'); });
          const hint = document.createElement('div');
          hint.className = 'caps-hint';
          hint.textContent = 'Caps Lock ativo';
          hint.style.display = 'none';
          p.parentElement.appendChild(hint);
          p.addEventListener('keyup', (e)=>{ hint.style.display = (e.getModifierState && e.getModifierState('CapsLock')) ? 'block' : 'none'; });
        }
        (u || p)?.focus();
        [u,p].forEach(el => el && el.addEventListener('keydown', (e)=>{ if (e.key === 'Enter'){ btn?.click(); }}));
        if (btn){
          btn.addEventListener('click', ()=>{
            const old = btn.textContent;
            btn.disabled = true; btn.textContent = 'Entrando…';
            setTimeout(()=>{ btn.disabled = false; btn.textContent = old; }, 4000);
          }, { once:false });
        }
      });
    })();
    </script>
    """, unsafe_allow_html=True)

apply_ux_enhancements()

# ------------------------------------------------------------
# Estado do login
# ------------------------------------------------------------
if 'auth_status' in locals():
    if 'last_auth_status' not in st.session_state:
        st.session_state.last_auth_status = None
    if auth_status != st.session_state.last_auth_status:
        if auth_status is True:
            st.toast("Login realizado com sucesso. Bem-vindo!", icon="✅")
        elif auth_status is False:
            st.toast("Usuário ou senha inválidos.", icon="⚠️")
        st.session_state.last_auth_status = auth_status
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

