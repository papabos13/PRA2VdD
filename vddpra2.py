# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGAR DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1YtEcEhdS9bddZddkCoZO_NkUuavwmLJz"
    df = pd.read_csv(url, parse_dates=["month"])
    df["month"] = pd.to_datetime(df["month"])
    return df

df = cargar_datos()

# ---------- TÍTULO ----------
st.title("🌍 Visualización climática por capitales")
st.write("Selecciona una variable para visualizar su evolución a lo largo del tiempo.")

# ---------- VARIABLES NUMÉRICAS ----------
columnas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
variable = st.selectbox("📌 Variable a visualizar (tamaño del punto)", columnas_numericas)

# ---------- FECHA (MENÚ DESPLEGABLE) ----------
fechas_disponibles = sorted(df["month"].dt.to_period("M").astype(str).unique())
fecha_str = st.selectbox("🗓️ Selecciona una fecha", fechas_disponibles)

# Filtrar datos por la fecha seleccionada
df_filtrado = df[df["month"].dt.to_period("M").astype(str) == fecha_str]

# Eliminar filas con NaN en coordenadas o en la variable
df_filtrado_validas = df_filtrado.dropna(subset=["latitude", "longitude", variable])

# ---------- MAPA ----------
if df_filtrado_validas.empty:
    st.warning(f"⚠️ No hay datos disponibles para la fecha seleccionada: {fecha_str}")
else:
    st.success(f"✅ Mostrando datos para **{variable}** en **{fecha_str}**")
    fig = px.scatter_geo(
        df_filtrado_validas,
        lat="latitude",
        lon="longitude",
        color=variable,
        size=variable,
        hover_name="city_name" if "city_name" in df.columns else None,
        projection="natural earth",
        title=f"{variable} en {fecha_str}",
    )
    st.plotly_chart(fig)
