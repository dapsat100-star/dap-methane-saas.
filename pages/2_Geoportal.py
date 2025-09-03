import streamlit as st

st.title("🗺️ Geoportal")
st.write("Espaço para camadas geoespaciais, filtros e visualizações avançadas.")

st.divider()
st.subheader("Upload de camadas (GeoJSON, CSV, etc.)")
up = st.file_uploader("Envie um arquivo (ex.: GeoJSON/CSV)", type=["geojson","json","csv"])
if up is not None:
    st.success(f"Arquivo recebido: {up.name}")
    if up.name.lower().endswith(".csv"):
        import pandas as pd
        df = pd.read_csv(up)
        st.dataframe(df.head())
