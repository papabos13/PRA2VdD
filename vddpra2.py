
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGAR DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1PumGCVeb9pBb1VdC3Atm9GoLrxybVfh8"  # tu ID de Drive
    df = pd.read_csv(url, parse_dates=["month"])
    return df

df = cargar_datos()

# ---------- TÍTULO Y VARIABLE ----------
st.title("🌍 Visualización climática por capitales")

variables_disponibles = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
    "sunrise_avg_min", "sunset_avg_min", "daylight_duration", "sunshine_duration",
    "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours",
    "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration"
]

variable = st.selectbox("📊 Variable climática:", variables_disponibles)
rel_variable = f"rel_{variable}_historico"



# ---------- FORMATO DE FECHA PARA ANIMACIÓN ----------
df["month_str"] = df["month"].dt.strftime("%Y-%m")

# ---------- VISUALIZACIÓN PLOTLY ----------
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    size=df[variable].abs(),
    color=color_col,
    animation_frame="month_str",
    hover_name="city_name",
    hover_data=["country_name", variable, color_col],
    color_continuous_scale="RdBu_r",
    size_max=15,
    zoom=1
)

fig.update_layout(
    mapbox_style="carto-positron",
    title=f"Evolución mensual de {variable}",
    height=750,
    width=1100
)

st.plotly_chart(fig, use_container_width=False)

