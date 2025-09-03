import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Estatísticas Gerais", page_icon="📊", layout="wide")

if "auth" not in st.session_state:
    st.switch_page("app.py")

st.title("📊 Estatísticas Gerais")

# KPIs (mock)
kpi_cols = st.columns(4)
kpi_cols[0].metric("Relatórios OGMP2.0", 48)
kpi_cols[1].metric("Número de Aquisições de Satélite", 65)
kpi_cols[2].metric("Usuários Logados", 3)
kpi_cols[3].metric("Unidades Monitoradas", 10)

st.divider()

fac = pd.read_csv("data/facilities.csv")
m = folium.Map(location=[-14.2, -51.9], zoom_start=4, tiles="CartoDB positron")
for _, r in fac.iterrows():
    folium.CircleMarker(
        location=[r.lat, r.lon], radius=6, fill=True, popup=r["name"],
        color="#4da3ff", fill_opacity=0.8
    ).add_to(m)

with st.container(border=True):
    st.subheader("Facilidades Monitoradas")
    st_folium(m, height=520, use_container_width=True)

st.caption("Mapa e indicadores meramente ilustrativos (dados fictícios).")
