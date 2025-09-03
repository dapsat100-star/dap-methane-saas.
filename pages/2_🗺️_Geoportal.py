import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap

st.set_page_config(page_title="Geoportal", page_icon="🗺️", layout="wide")
if "auth" not in st.session_state:
    st.switch_page("app.py")

st.title("🗺️ Geoportal")

left, right = st.columns([1,3])

with left:
    st.subheader("Últimas aquisições de\nAlta Resolução")
    df = pd.read_csv("data/acquisitions.csv")
    for _, row in df.iterrows():
        with st.container(border=True):
            st.image(row["thumb_path"], caption=f"Report {row['report_id']} — {int(row['emission_kgph'])} kg CH4/h", use_column_width=True)
            st.markdown(f"**{row['date']} – {row['time']}**")

with right:
    top = st.columns([2,1,1])
    site = top[0].selectbox("Site", ["site 1", "site 2", "site 3"], index=1)
    de = top[1].date_input("De")
    ate = top[2].date_input("Até")

    toggle_plume = st.toggle("Pluma", value=True)
    toggle_info = st.toggle("Informações Adicionais", value=True)

    # Basemap centered near Iguazu as in the screenshot
    m = folium.Map(location=[43.083, -79.074], zoom_start=15, tiles="OpenStreetMap")

    # Fake plume as a gaussian cloud of points if enabled
    if toggle_plume:
        rng = np.random.default_rng(42)
        base_lat, base_lon = 43.084, -79.079
        lats = base_lat + rng.normal(0, 0.001, 250)
        lons = base_lon + rng.normal(0, 0.0015, 250)
        weights = np.clip(rng.normal(1, 0.3, 250), 0.2, 2.0)
        HeatMap(list(zip(lats, lons, weights))).add_to(m)

    m_canvas = st_folium(m, height=600, use_container_width=True)

    if toggle_info:
        with st.container(border=True):
            st.markdown("### Painel de Metadados")
            st.markdown("""
            **Grau Confiança da Medição:** Alto  
            **Imagem Base:** BlackSky 0.35 m  
            **Intervalo entre Detecção de Metano (SWIR) e Aquisição da Imagem Base:** 4 horas  
            **Velocidade do Vento (m/s):** 2.0  
            **Direção do Vento (graus):** 85  
            """)

st.caption("Camadas e parâmetros demonstrativos (dados fictícios).")
