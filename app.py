import os
import pathlib
import streamlit as st
from dotenv import load_dotenv
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# -----------------------------------------------------------------------------
# Configuração da página
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Plataforma de Metano OGMP 2.0 - L5", layout="wide")
load_dotenv()  # opcional, útil em deploys fora do Streamlit Cloud

# -----------------------------------------------------------------------------
# Função: Hero central (só na tela de login)
# -----------------------------------------------------------------------------
def login_hero():
    # Mostra logo + título no centro da tela
    st.markdown(
        """
        <div style="display:flex;flex-direction:column;justify-content:center;
                    align-items:center;height:60vh;text-align:center;">
            <img src="dapatlas.jpeg" width="220">
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
# Espera-se que exista um 'auth_config.yaml' na raiz do repositório, ex.:
# credentials:
#   usernames:
#     demo:
#       name: Demo User
#       email: demo@dap.com
#       password: "<hash_bcrypt_aqui>"
# cookie:
#   expiry_days: 30
#   key: "CHAVE_SECRETA_ALEATORIA"
#   name: dap_auth

with open("auth_config.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Mantemos o hero visível até o login
placeholder = st.empty()
with placeholder.container():
    login_hero()

# Formulário de login (fix para versões recentes: usar location="main")
name, auth_status, username = authenticator.login(location="main")

if auth_status is False:
    st.error("Usuário ou senha inválidos.")
elif auth_status is None:
    st.info("Por favor, faça login para continuar.")
elif auth_status:
    # Remove o hero quando autentica
    placeholder.empty()

    # Barra lateral (logout + navegação)
    st.sidebar.success(f"Logado como: {name}")
    authenticator.logout("Sair", "sidebar")

    # -----------------------------------------------------------------------------
    # (Opcional) Conectar ao Snowflake (read-only) usando variáveis de ambiente
    # Defina estes secrets/variáveis no provedor de hospedagem (ex.: Streamlit Cloud):
    #   SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    #   SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
    # -----------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------
    # Navegação entre páginas do Streamlit
    # As páginas estão dentro de pages/
    # -----------------------------------------------------------------------------
    st.sidebar.page_link("pages/1_📊_Estatisticas_Gerais.py", label="Estatísticas Gerais")
    st.sidebar.page_link("pages/2_🗺️_Geoportal.py", label="Geoportal")
    st.sidebar.page_link("pages/3_📄_Relatorio_OGMP_2_0.py", label="Relatório OGMP 2.0")
    st.sidebar.page_link("pages/4_🛰️_Agendamento_de_Imagens.py", label="Agendamento de Imagens")

    st.markdown("> Use o menu à esquerda para navegar nas páginas.")
