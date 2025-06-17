# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGAR DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1c3Ok49GNhWxgdDAxOPISMTDUd9SyWE2v"
    df = pd.read_csv(url, parse_dates=["month"])
    return df

df = cargar_datos()

# ---------- TÍTULO Y VARIABLE ----------
st.title("🌍 Evolución climática por capitales del mundo")

variables_disponibles = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
    "sunrise_avg_min", "sunset_avg_min", "daylight_duration", "sunshine_duration",
    "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours",
    "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration"
]

variable = st.selectbox("📊 Variable climática:", variables_disponibles)

# ---------- NORMALIZACIÓN MENSUAL POR CAPITAL ----------
df["month_str"] = df["month"].dt.strftime("%Y-%m")

# Normalizamos cada ciudad respecto a su propio histórico mensual
df["rel_value"] = df.groupby(["city_name", df["month"].dt.month])[variable].transform(
    lambda x: (x - x.mean()) / x.std() if x.std() != 0 else 0
)

# ---------- MAPA CON ANIMACIÓN ----------
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    size=df[variable].abs(),
    color="rel_value",
    animation_frame="month_str",
    hover_name="city_name",
    hover_data=["country_name", variable],
    color_continuous_scale="RdBu_r",
    size_max=15,
    zoom=1
)

fig.update_layout(
    mapbox_style="carto-positron",
    title=f"Evolución mensual de {variable} normalizada por ciudad",
    height=750,
    width=1100
)

st.plotly_chart(fig, use_container_width=False)


