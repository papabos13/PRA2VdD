import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGA DE DATOS DESDE GOOGLE DRIVE ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1W3py6RlU9x0q97DRJLDLwYBzHSwDT0M-"
    df = pd.read_csv(url, parse_dates=["month"])
    return df

df = cargar_datos()

st.title("🌍 Visualización interactiva de temperaturas en capitales")

# Variables base
temp_vars = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean"
]

variable = st.selectbox("Selecciona la variable de temperatura base", temp_vars)
col_size = f"rel_{variable}_global"
col_color = f"rel_{variable}_city"

# Validación de columnas
if col_size not in df.columns or col_color not in df.columns:
    st.error(f"No se encuentran las columnas: {col_size} o {col_color}")
    st.stop()

# Selector de mes
fechas_disponibles = df["month"].dt.to_period("M").drop_duplicates().astype(str)
fecha_str = st.selectbox("Selecciona una fecha (AAAA-MM)", fechas_disponibles)
fecha_period = pd.Period(fecha_str, freq="M")
df_filtrado = df[df["month"].dt.to_period("M") == fecha_period]

# Eliminar nulos críticos
df_filtrado = df_filtrado.dropna(subset=["latitude", "longitude", col_size, col_color])

# ---------- MAPA ----------
fig = px.scatter_geo(
    df_filtrado,
    lat="latitude",
    lon="longitude",
    hover_name="city_name",
    hover_data=[variable, col_size, col_color],
    size=col_size,
    color=col_color,
    projection="natural earth",
    title=f"{variable} — {fecha_str}",
)

st.plotly_chart(fig, use_container_width=True)

