import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGA DE DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1wG04qSWqz3wCcck8ozYNyynX4FRvl7Bu"
    df = pd.read_csv(url, parse_dates=["month"])
    df["month"] = pd.to_datetime(df["month"])
    return df

df = cargar_datos()

# ---------- INTERFAZ PRINCIPAL ----------
st.title("🧭 Dashboard Climático Interactivo por Capitales")

st.markdown("""
Explora los datos climáticos históricos mensuales para las capitales del mundo.
""")

# ---------- SELECTORES ----------
col1, col2 = st.columns(2)

# Variable numérica a analizar
columnas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
with col1:
    variable = st.selectbox("📌 Variable a visualizar", columnas_numericas, index=columnas_numericas.index("temperature_2m_mean"))

# Fecha seleccionada para el mapa
fechas = df["month"].dt.to_period("M").astype(str).sort_values().unique()
with col2:
    fecha_str = st.selectbox("🗓️ Fecha para el mapa", fechas, index=0)

# Capital a analizar
capitales = sorted(df["city_name"].dropna().unique())
ciudad = st.selectbox("🏙️ Selecciona una ciudad", capitales, index=capitales.index("Abidjan"))

# ---------- MAPA GEOCLIMÁTICO ----------
df_fecha = df[df["month"].dt.to_period("M").astype(str) == fecha_str]
df_fecha = df_fecha.dropna(subset=["latitude", "longitude", variable])

st.subheader("🌍 Mapa mundial")
fig_mapa = px.scatter_geo(
    df_fecha,
    lat="latitude",
    lon="longitude",
    color=variable,
    size=variable,
    hover_name="city_name",
    projection="natural earth",
    title=f"{variable} en {fecha_str}"
)
st.plotly_chart(fig_mapa)

# ---------- GRÁFICO DE EVOLUCIÓN TEMPORAL ----------
st.subheader(f"📈 Evolución de {variable} en {ciudad}")
df_ciudad = df[df["city_name"] == ciudad].dropna(subset=[variable])

fig_linea = px.line(
    df_ciudad,
    x="month",
    y=variable,
    title=f"{variable} mensual en {ciudad}",
    labels={"month": "Mes", variable: variable},
)
st.plotly_chart(fig_linea)

# ---------- ESTADÍSTICAS ----------
media = df_ciudad[variable].mean()
desviacion = df_ciudad[variable].std()

st.subheader("📊 Indicadores de la ciudad seleccionada")
col3, col4 = st.columns(2)
col3.metric("Media histórica", f"{media:.2f}")
col4.metric("Desviación estándar", f"{desviacion:.2f}")
