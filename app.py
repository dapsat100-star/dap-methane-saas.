# app.py — Landing (visual) + integração com Snowflake
import base64
import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Plataforma de Metano – OGMP 2.0 • DAP", page_icon="🛰️", layout="wide")

def load_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# Usuário atual (controle real de acesso é por roles do Snowflake)
session = get_active_session()
current_user = session.sql("select current_user()").collect()[0][0]

st.markdown("""
<style>
:root{ --brand:#173b5a; --brand2:#0f2a40; --borda:#e6e8ec; }
.topbar{width:100%;background:#000;color:#fff;padding:8px 16px;font-size:14px;}
.card{background:#fff;border:1px solid var(--borda);border-radius:12px;padding:20px;box-shadow:0 1px 2px rgba(0,0,0,.03);}
.stButton>button[kind="primary"]{background:var(--brand);color:#fff;border:1px solid var(--brand);border-radius:8px;padding:10px 14px;font-weight:600;}
.stButton>button[kind="primary"]:hover{background:var(--brand2);border-color:var(--brand2);}
.hero{padding:24px 16px 8px 16px;}
.hero h1{font-size:clamp(32px,4.5vw,64px);line-height:1.05;margin:0 0 12px 0;}
.hero p.lead{max-width:640px;font-size:16px;color:#222;}
.footer-water{width:100%;height:24px;background:linear-gradient(0deg,#dff1f7,#eaf6fb);border-top:1px solid #e9eef2;margin-top:24px;}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;background:#eef3f6;border:1px solid #dde6ee;color:#334;}
</style>
""", unsafe_allow_html=True)

logo_b64 = load_b64("assets/dap_logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" height="28" style="float:right;" />' if logo_b64 else ""
st.markdown(f'<div class="topbar">Plataforma de Monitoramento de Metano OGMP 2.0 - L5 {logo_html}</div>', unsafe_allow_html=True)

colL, colR = st.columns([0.6, 0.4], gap="large")
with colL:
    st.markdown(f"""
    <div class="hero">
      <h1>Plataforma de Monitoramento<br/>de Emissões de Metano OGMP 2.0 - L5</h1>
      <p class="lead">
        Plataforma DAP ATLAS certificada como estratégica de Defesa pelo Ministério da Defesa do Brasil,
        segundo Portaria GMD-MD nº 5.574, DOU 12/12/2024.
      </p>
      <div class="badge">Usuário Snowflake: <b>{current_user}</b></div>
    </div>
    """, unsafe_allow_html=True)

with colR:
    st.markdown("#### Autenticação de dois fatores")
    st.caption("Digite o código de 6 dígitos do seu aplicativo de autenticação")
    st.text_input("Código de verificação", max_chars=6, key="code_mock")
    st.button("Verificar", type="primary", use_container_width=True)
    st.link_button("Reenviar código", "#", type="secondary")

with colL:
    st.markdown("#### Acesso ao sistema")
    st.text_input("Nome de usuário", placeholder="seu.usuario", key="u_mock")
    st.text_input("Senha", type="password", key="p_mock")
    st.button("Iniciar sessão", type="primary", use_container_width=True)

st.markdown('<div class="footer-water"></div>', unsafe_allow_html=True)
st.divider()
st.subheader("Entrar na Plataforma")
st.page_link("pages/Dashboard.py", label="📊 Abrir Dashboard")
st.page_link("pages/Relatorios.py", label="📑 Relatórios")
