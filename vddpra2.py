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

# ---------- VARIABLES DISPONIBLES ----------
variables_disponibles = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
    "sunrise_avg_min", "sunset_avg_min", "daylight_duration", "sunshine_duration",
    "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours",
    "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration"
]

st.title("🌍 Visualización climática histórica por capitales")
variable = st.selectbox("📊 Variable climática:", sorted(variables_disponibles))
rel_variable = f"rel_{variable}_historico"

# ---------- VALIDACIONES ----------
if variable not in df_final.columns:
    st.error(f"La columna '{variable}' no se encuentra en el dataset.")
    st.stop()

if rel_variable not in df_final.columns:
    st.error(f"La columna '{rel_variable}' no se encuentra en el dataset.")
    st.stop()

# ---------- FORMATO DE FECHAS Y FILTRO ----------
df_final["month_str"] = df_final["month"].dt.strftime("%Y-%m")
df_vis = df_final.dropna(subset=[rel_variable, variable])

if df_vis.empty:
    st.warning("No hay datos con valores históricos suficientes para esta variable.")
    st.stop()

# ---------- MAPA ANIMADO ----------
fig = px.scatter_mapbox(
    df_vis,
    lat="latitude",
    lon="longitude",
    color=rel_variable,
    size=df_vis[variable].abs(),
    animation_frame="month_str",
    hover_name="city_name",
    hover_data=["country_name", variable, rel_variable],
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
