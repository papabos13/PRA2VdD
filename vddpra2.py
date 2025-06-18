# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGAR DATOS ----------
@st.cache_data
def cargar_datos():  
    url = "https://drive.google.com/uc?id=1XsGsc3nVLuOldbId5z3gdj4hOf7MlZqa"
    df_final = pd.read_csv(url, parse_dates=["month"])
    return df_final

df_final = cargar_datos()

# ---------- VARIABLES DISPONIBLES CON HISTÓRICO ----------
todas_las_columnas = df_final.columns
variables_disponibles = [
    col.replace("rel_", "").replace("_historico", "")
    for col in todas_las_columnas
    if col.startswith("rel_") and col.endswith("_historico")
]

# ---------- INTERFAZ ----------
st.title("🌍 Visualización climática histórica por capitales")
variable = st.selectbox("📊 Variable climática:", sorted(variables_disponibles))
rel_variable = f"rel_{variable}_historico"

# Verificación de columna
if rel_variable not in df_final.columns:
    st.error(f"La columna '{rel_variable}' no está en el archivo.")
    st.stop()

# ---------- MAPA ----------
df_final["month_str"] = df_final["month"].dt.strftime("%Y-%m")
df_vis = df_final.dropna(subset=[rel_variable])

fig = px.scatter_mapbox(
    df_vis,
    lat="latitude",
    lon="longitude",
    color=rel_variable,
    size=df_vis[variable].abs(),
    animation_frame="month_str",
    hover_name="city_name",
    hover_data=["country_name", variable],
    color_continuous_scale="RdBu_r",
    size_max=15,
    zoom=1
)

fig.update_layout(
    mapbox_style="carto-positron",
    title=f"Evolución histórica mensual de {variable}",
    height=750,
    width=1100
)

st.plotly_chart(fig, use_container_width=False)
