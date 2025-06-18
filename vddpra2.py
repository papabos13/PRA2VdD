import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CONFIGURACIÓN ----------
st.set_page_config(page_title="Clima en capitales", layout="wide")

st.title("🌍 Visualización de clima en capitales del mundo")

# ---------- CARGA DE DATOS DESDE GOOGLE DRIVE ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1MXhkIsh9Eeq1OEhXuWp8rdiS-TZgR_8n"
    df = pd.read_csv(url, parse_dates=["month"])
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

# ---------- SELECCIÓN DE VARIABLES Y FECHA ----------
col1, col2 = st.columns(2)
with col1:
    variable = st.selectbox("📊 Selecciona la variable climática", variables_disponibles)

with col2:
    fecha = st.selectbox("📅 Selecciona el mes y año", sorted(df["month"].dt.strftime("%Y-%m").unique()))

# ---------- FILTRADO DE FECHA ----------
df_fecha = df[df["month"].dt.strftime("%Y-%m") == fecha]

# ---------- LÓGICA DE SIZE ----------
# Las variables de temperatura que tienen versión shifted_*
variables_shifted = ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
                     "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean"]

if variable in variables_shifted:
    size_var = f"shifted_{variable}"
else:
    size_var = variable

color_var = f"rel_{variable}"

# ---------- MAPA ----------
fig = px.scatter_geo(
    df_fecha,
    lat="latitude",
    lon="longitude",
    hover_name="city_name",
    size=size_var,
    color=color_var,
    color_continuous_scale="RdBu",
    projection="natural earth",
    title=f"{variable} en {fecha}",
)

fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
