import streamlit as st
from io import BytesIO

st.title("📄 Relatório OGMP 2.0")

st.write("Gere e baixe um relatório de exemplo (placeholder).")

content = """
Relatório OGMP 2.0 - Exemplo
----------------------------
Este é um conteúdo de demonstração.
Substitua por sua geração real (PDF/HTML).
"""
bio = BytesIO(content.encode("utf-8"))
st.download_button("Baixar relatório de exemplo (.txt)", data=bio, file_name="Relatorio_OGMP20_demo.txt")
