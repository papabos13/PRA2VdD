import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGA DE DATOS DESDE DRIVE ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1W3py6RlU9x0q97DRJLDLwYBzHSwDT0M-"
    df = pd.read_csv(url, parse_dates=["month"])
    return df

df = cargar_datos()

# ---------- INTERFAZ ----------
st.title("🌍 Visualización interactiva de temperaturas en capitales")

# Variables base
temp_vars = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean"
]

# Selector de variable de temperatura base
variable = st.selectbox("Selecciona la variable de temperatura base", temp_vars)

# Columnas relativas
col_size = f"rel_{variable}_global"
col_color = f"rel_{variable}_city"

min_val = df_filtrado[col_size].min()
max_val = df_filtrado[col_size].max()

df_filtrado["size_scaled"] = (
    (df_filtrado[col_size] - min_val) / (max_val - min_val) * 45 + 5
)

# Selector de fecha (año-mes)
fechas_disponibles = df["month"].dt.to_period("M").drop_duplicates().astype(str)
fecha_str = st.selectbox("Selecciona una fecha (AAAA-MM)", fechas_disponibles)

# Filtrar por la fecha seleccionada
fecha_period = pd.Period(fecha_str, freq="M")
df_filtrado = df[df["month"].dt.to_period("M") == fecha_period]

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


