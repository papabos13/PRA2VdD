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

# ---------- TÍTULO Y VARIABLE ----------
st.title("🌍 Visualización climática histórica por capitales")

variables_disponibles = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
    "sunrise_avg_min", "sunset_avg_min", "daylight_duration", "sunshine_duration",
    "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours",
    "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration"
]

# Selector de variable
variable = st.selectbox("📊 Variable climática:", variables_disponibles)
rel_variable = f"rel_{variable}_historico"

# ---------- FILTRADO Y MAPA ----------
df_final["month_str"] = df_final["month"].dt.strftime("%Y-%m")

# Filtrar solo registros con histórico válido
df_vis = df_final.dropna(subset=[rel_variable])

# Crear figura
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

