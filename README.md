# Plataforma de Monitoramento de Metano – OGMP 2.0 (Template)

Este repositório é um **template mínimo** de um SaaS com *Streamlit* que imita as telas do seu exemplo
(Login + 2FA, Dashboard com mapa e KPIs, Geoportal, Relatório OGMP 2.0 e Agendamento de Imagens).

Ele já vem com _placeholders_ para integração com **Snowflake** (opcional).
Você pode rodar **sem Snowflake** (dados mock em `data/`) e ligar o Snowflake depois.

---

## 🧰 Como usar (localmente)

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Rode o app:
   ```bash
   streamlit run app.py
   ```

3. A senha padrão é `admin` e o código 2FA de demonstração é `123456` (apenas para testes).

---

## 🔗 Conectar ao Snowflake (opcional)

- Configure variáveis de ambiente (ou um arquivo `.env`) com as credenciais:
  ```bash
  SNOWFLAKE_ACCOUNT=xxxxxx-xx
  SNOWFLAKE_USER=seu_usuario
  SNOWFLAKE_PASSWORD=sua_senha
  SNOWFLAKE_WAREHOUSE=COMPUTE_WH
  SNOWFLAKE_DATABASE=APP_DB
  SNOWFLAKE_SCHEMA=PUBLIC
  ```

- No app, ative a flag **"Usar Snowflake"** na tela de login. O código já tenta abrir conexão via
  `snowflake-connector-python`. Se der erro, ele volta para dados mock automaticamente.

---

## 🚀 Subir para o GitHub

1. Crie um repositório vazio no GitHub.
2. **Faça upload do ZIP** `dap_methane_saas.zip` (ou descompacte e suba os arquivos).

---

## 🧊 (Opcional) Implantação com Streamlit in Snowflake (SiS)

Use o arquivo `snowflake_deploy.sql` como base. Passos típicos:

```sql
-- em um worksheet do Snowflake
USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
CREATE DATABASE IF NOT EXISTS APP_DB;
CREATE SCHEMA IF NOT EXISTS APP_DB.PUBLIC;

-- Cria um stage e envia os arquivos (via UI "Stages" ou comando PUT pelo SnowSQL)
CREATE OR REPLACE STAGE APP_DB.PUBLIC.APP_STAGE;

-- Depois de subir os arquivos do app para o stage, crie o app Streamlit:
CREATE OR REPLACE STREAMLIT APP_DB.PUBLIC.METHANE_APP
ROOT_LOCATION = '@APP_DB.PUBLIC.APP_STAGE'
MAIN_FILE = 'app.py';
```

> **Dica**: No Snowflake, o código do app fica dentro de um **Stage**. Você pode manter o código no GitHub
e sincronizar manualmente com o Stage quando fizer mudanças.

---

## 📁 Estrutura

```
app.py
pages/
  1_📊_Estatisticas_Gerais.py
  2_🗺️_Geoportal.py
  3_📄_Relatorio_OGMP_2_0.py
  4_🛰️_Agendamento_de_Imagens.py
data/
  facilities.csv
assets/
  (coloque seu logo aqui como logo.png, se quiser)
requirements.txt
snowflake_deploy.sql
```

---

## 📜 Licença

Uso livre para demonstração/prototipagem. Sem garantias.

---

## 🌐 Modo SaaS (usuários externos) — Hospede fora do Snowflake

### 1) Suba no GitHub
- Envie todos os arquivos (inclusive `auth_config.yaml`, `requirements.txt`, etc.).

### 2) Hospede (Streamlit Community Cloud recomendado)
- Em https://share.streamlit.io → **Deploy an app** → selecione seu repositório.
- Em **Secrets** (ou variáveis de ambiente do provedor), configure as credenciais do Snowflake (opcional):
  - `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`

### 3) Login para seus clientes
- Use os usuários de exemplo no `auth_config.yaml`:
  - `cliente1` / `senha123`
  - `cliente2` / `senha456`
- Edite/adicione usuários e senhas (lembre de gerar o **hash bcrypt**).

> Para mudar a senha de demo: gere um hash bcrypt novo e substitua em `auth_config.yaml`.