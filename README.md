# DAP ATLAS – Plataforma de Monitoramento de Metano (OGMP 2.0 – L5)

Este repositório contém um **MVP em Streamlit** com 4 páginas:
1. **Login (app.py)** com autenticação simples + 2FA fictício;
2. **📊 Estatísticas Gerais** (mapa de facilidades + KPIs);
3. **🗺️ Geoportal** (basemap + pluma sintética via heatmap);
4. **📄 Relatório OGMP 2.0** (lista de relatórios e visualização futura);
5. **🛰️ Agendamento de Imagens** (formulário de tasking / placeholder).

> Usuário de teste: `john` | Senha: `dap2025!` | Código 2FA: `123456`

## Como rodar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Community Cloud
- Faça o push para um repositório GitHub;
- No Streamlit Cloud, aponte para `app.py`;
- Configure variáveis de ambiente conforme necessário.
