# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CONFIGURACIÓN DE PÁGINA ----------
st.set_page_config(layout="wide")
st.title("🌍 Visualización climática histórica por capitales")

# ---------- CARGA DE DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1PumGCVeb9pBb1VdC3Atm9GoLrxybVfh8"  # tu ID de Drive
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

# ---------- SELECCIÓN DE VARIABLE ----------
variable = st.selectbox("📊 Variable climática:", sorted(variables_disponibles))
rel_variable = f"rel_{variable}_historico"

# ---------- VALIDACIÓN DE COLUMNA DE FECHAS ----------
if "month" not in df.columns or not pd.api.types.is_datetime64_any_dtype(df["month"]):
    try:
        df["month"] = pd.to_datetime(df["month"])
    except Exception:
        st.error("❌ Error: la columna 'month' no se puede convertir a fecha.")
        st.stop()

df["month_str"] = df["month"].dt.strftime("%Y-%m")

# ---------- COLUMNA DE COLOR Y MARCA DE DATOS IMPUTADOS ----------
if rel_variable in df.columns:
    df["color_value"] = df[rel_variable].fillna(0)  # muestra todas las capitales
    df["dato_real"] = df[rel_variable].notna()
    color_leyenda = rel_variable
else:
    st.warning(f"No se encontró la columna histórica: {rel_variable}. Se calculará por mes (global).")
    df["color_value"] = df.groupby("month")[variable].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    df["dato_real"] = True
    color_leyenda = "rel_value"

# ---------- MAPA ----------
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="color_value",
    size=df[variable].abs(),
    animation_frame="month_str",
    hover_name="city_name",
    hover_data={
        "country_name": True,
        variable: True,
        rel_variable: True if rel_variable in df.columns else False,
        "dato_real": True,
    },
    color_continuous_scale="RdBu_r",
    size_max=15,
    zoom=1,
)

fig.update_layout(
    mapbox_style="carto-positron",
    title=f"Evolución mensual de {variable}",
    height=750,
    width=1100,
    margin={"r": 0, "t": 40, "l": 0, "b": 0}
)

st.plotly_chart(fig, use_container_width=False)

