import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CONFIGURACIÓN ----------
st.set_page_config(page_title="Clima en capitales", layout="wide")
st.title("🌍 Animación del clima mensual en capitales del mundo")

# ---------- CARGA DE DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1MXhkIsh9Eeq1OEhXuWp8rdiS-TZgR_8n"
    df = pd.read_csv(url, parse_dates=["month"])
    df["fecha_str"] = df["month"].dt.strftime("%Y-%m")
    df = df.sort_values(by=["month"])
    return df

df = cargar_datos()

# ---------- VARIABLES DISPONIBLES ----------
variables_disponibles = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
    "sunrise_avg_min", "sunset_avg_min", "daylight_duration", "sunshine_duration",
    "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours",
    "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration"
]

# ---------- SELECCIÓN DE VARIABLE ----------
variable = st.selectbox("📊 Selecciona la variable climática", variables_disponibles)

# ---------- SIZE Y COLOR ----------
variables_shifted = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean"
]

if variable in variables_shifted:
    size_var = f"shifted_{variable}"
else:
    size_var = variable

color_var = f"rel_{variable}"

# ---------- ANIMACIÓN GLOBAL ----------
try:
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="city_name",
        size=size_var,
        color=color_var,
        animation_frame="fecha_str",
        size_max=25,
        zoom=1,
        mapbox_style="open-street-map",
        color_continuous_scale="RdBu_r",  # ← invertimos los colores
        title=f"Evolución de {variable} mensual (1950–2024)"
    )

    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, height=700)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error al generar el mapa animado: {e}")


