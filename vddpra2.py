
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---- CONFIGURACIÓN ----
st.set_page_config(layout="wide")
st.title("🌍 Visualización climática histórica por capitales")

# ---- CARGA DE DATOS DESDE GOOGLE DRIVE ----
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1PumGCVeb9pBb1VdC3Atm9GoLrxybVfh8"  # tu ID de Drive
    df = pd.read_csv(url, parse_dates=["month"])
    return df

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"❌ Error al cargar los datos: {e}")
    st.stop()

# ---- VARIABLES DISPONIBLES ----
variables = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
    "sunrise_avg_min", "sunset_avg_min", "daylight_duration", "sunshine_duration",
    "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours",
    "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration"
]

# ---- SELECCIÓN DE VARIABLE ----
variable = st.selectbox("📊 Variable climática:", sorted(variables))
rel_variable = f"rel_{variable}_historico"

# ---- FILTRO Y FORMATO ----
if "month" not in df.columns or not pd.api.types.is_datetime64_any_dtype(df["month"]):
    try:
        df["month"] = pd.to_datetime(df["month"])
    except Exception:
        st.error("❌ Error: la columna 'month' no se puede convertir a fecha.")
        st.stop()

df["month_str"] = df["month"].dt.strftime("%Y-%m")
df_vis = df.dropna(subset=[variable, rel_variable])

if df_vis.empty:
    st.warning("No hay datos suficientes para esta variable.")
    st.stop()

# ---- VISUALIZACIÓN CON PLOTLY ----
fig = px.scatter_mapbox(
    df_vis,
    lat="latitude",
    lon="longitude",
    color=rel_variable,
    animation_frame="month_str",
    hover_name="city_name",
    hover_data=["country_name", variable, rel_variable],
    color_continuous_scale="RdBu_r",
    size_max=15,
    zoom=1
)

fig.update_layout(
    mapbox_style="carto-positron",
    height=750,
    margin={"r":0, "t":40, "l":0, "b":0},
    title=f"Evolución mensual de {variable}"
)

st.plotly_chart(fig, use_container_width=True)

