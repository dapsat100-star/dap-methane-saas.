import streamlit as st

st.title("📊 Estatísticas Gerais")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Relatórios OGMP 2.0", 48)
c2.metric("Aquisições de Satélite", 65)
c3.metric("Usuários Logados", 3)
c4.metric("Unidades Monitoradas", 10)

st.divider()
st.subheader("Mapa (exemplo simples)")
try:
    import folium
    from streamlit_folium import st_folium
    m = folium.Map(location=[-15.78, -47.93], zoom_start=4, tiles="cartodbpositron")
    for lat, lon, name in [
        (-3.13, -60.02, "Manaus"),
        (-22.90, -43.20, "Rio de Janeiro"),
        (-23.95, -46.33, "Santos"),
        (-30.03, -51.23, "Porto Alegre"),
    ]:
        folium.CircleMarker(location=[lat, lon], radius=6, tooltip=name).add_to(m)
    st_folium(m, height=480, width=980)
except Exception as e:
    st.info(f"Folium não disponível ou erro ao renderizar mapa: {e}")
