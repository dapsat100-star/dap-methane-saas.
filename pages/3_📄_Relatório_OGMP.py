import streamlit as st
import pandas as pd

st.set_page_config(page_title="Relatório OGMP 2.0", page_icon="📄", layout="wide")
if "auth" not in st.session_state:
    st.switch_page("app.py")

st.title("📄 Relatório OGMP 2.0")

df = pd.read_csv("data/acquisitions.csv")
st.dataframe(df[["report_id","date","time","site","emission_kgph","confidence"]].rename(columns={
    "report_id":"ID",
    "date":"Data",
    "time":"Hora",
    "site":"Site",
    "emission_kgph":"Emissão (kg CH4/h)",
    "confidence":"Confiança"
}), use_container_width=True, hide_index=True)

st.info("Selecione uma linha acima para, em versões futuras, abrir o relatório completo com gráficos, notas OGMP 2.0 e exportação em PDF.")
