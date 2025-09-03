-- 🚀 Deploy Streamlit app no Snowflake (caminho fácil)
-- 1) Ajuste estes nomes, se quiser:
SET WAREHOUSE = 'COMPUTE_WH';
SET DB = 'APP_DB';
SET SCHEMA = 'PUBLIC';
SET STAGE = 'APP_STAGE';
SET APP_NAME = 'METHANE_APP';

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE IDENTIFIER($WAREHOUSE);
CREATE DATABASE IF NOT EXISTS IDENTIFIER($DB);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($DB)||'.'||IDENTIFIER($SCHEMA);

-- Cria (ou recria) o Stage onde os arquivos do app ficarão
CREATE OR REPLACE STAGE IDENTIFIER($DB)||'.'||IDENTIFIER($SCHEMA)||'.'||IDENTIFIER($STAGE);

-- ⬆️ Agora, no SnowSQL, execute os PUTs abaixo a partir da pasta do projeto (onde estão os arquivos).
-- IMPORTANTE:
-- - No Windows use caminhos com \ ou rode o snowsql dentro da pasta do projeto.
-- - Mantemos AUTO_COMPRESS=FALSE (os arquivos ficam "puros" no stage).

-- Arquivo principal
PUT file://app.py @IDENTIFIER($DB)||'.'||IDENTIFIER($SCHEMA)||'.'||IDENTIFIER($STAGE) AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- Páginas
PUT file://pages/* @IDENTIFIER($DB)||'.'||IDENTIFIER($SCHEMA)||'.'||IDENTIFIER($STAGE)/pages/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- Assets (logo, etc.)
PUT file://assets/* @IDENTIFIER($DB)||'.'||IDENTIFIER($SCHEMA)||'.'||IDENTIFIER($STAGE)/assets/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- Dados mock
PUT file://data/* @IDENTIFIER($DB)||'.'||IDENTIFIER($SCHEMA)||'.'||IDENTIFIER($STAGE)/data/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- Cria/recria o app Streamlit apontando para o Stage
CREATE OR REPLACE STREAMLIT IDENTIFIER($DB)||'.'||IDENTIFIER($SCHEMA)||'.'||IDENTIFIER($APP_NAME)
ROOT_LOCATION = '@' || IDENTIFIER($DB)||'.'||IDENTIFIER($SCHEMA)||'.'||IDENTIFIER($STAGE)
MAIN_FILE = 'app.py';

-- Abra o app no Snowsight: Data » Databases » (seu DB) » (seu Schema) » Streamlit Apps » $APP_NAME
