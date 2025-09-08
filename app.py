# -*- coding: utf-8 -*-
import os
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import streamlit_authenticator as stauth
import base64

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
# Fundo com imagem local (background.png → base64)
# ------------------------------------------------------------
def _bg_data_uri():
    here = Path(__file__).parent
    candidates = [here/"background.png", here/"assets"/"background.png"]
    for p in candidates:
        if p.exists():
            mime = "image/png"
            b64 = base64.b64encode(p.read_bytes()).decode("ascii")
            return f"data:{mime};base64,{b64}"
    return None

_bg = _bg_data_uri()
if _bg:
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"]::before {{
      content:"";
      position: fixed; inset: 0;
      z-index: 0; pointer-events: none;
      background: #f5f5f5 url('{_bg}') no-repeat center center;
      background-size: cover;
      opacity: .55;  /* ajuste a intensidade */
      filter: contrast(103%) brightness(101%);
    }}
    .block-container, [data-testid="stSidebar"], header, footer {{
      position: relative; z-index: 1;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ 'background.png' não foi encontrado (raiz ou assets/).")

# ------------------------------------------------------------
# i18n
# ------------------------------------------------------------
if "lang" not in st.session_state: 
    st.session_state.lang = "pt"

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
    st.markdown(
        f"<div class='cta-row'><a class='btn-primary' href='#login'>{t['cta_login']}</a>"
        f"<a class='btn-ghost' href='mailto:support@dapsistemas.com'>{t['cta_about']}</a></div>",
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        f"<div id='login' class='login-card'><div class='login-title'>{t['secure_access']}</div>",
        unsafe_allow_html=True
    )
    fields = {"Form name": "", "Username": "Usuário", "Password": "Senha", "Login": "Entrar"}
    try:
        name, auth_status, username = authenticator.login("main", fields=fields)
    except TypeError:
        name, auth_status, username = authenticator.login("main")
    st.markdown(f"<div class='login-note'>{t['confidential']}</div></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# UX Kit (password eye + remember user)
# ------------------------------------------------------------
def apply_ux_enhancements():
    st.markdown("""
    <style>
      .pw-eye {position:absolute; right:10px; top:50%; transform: translateY(-50%);
        border:0; background:transparent; cursor:pointer; font-size:16px; padding:2px; line-height:1;}
      .pw-wrap { position:relative; }
      .caps-hint { margin-top:6px; font-size:12px; color:#d00; }
      .remember-row { display:flex; align-items:center; gap:8px; font-size:13px;
        margin:6px 0 10px 2px; color:#111;}
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
          const u = root.querySelector('input[type="text"]');
          const p = root.querySelector('input[type="password"]');
          const btn = root.querySelector('button');
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
          });
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
