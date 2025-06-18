# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGAR DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1YtEcEhdS9bddZddkCoZO_NkUuavwmLJz"
    df = pd.read_csv(url, parse_dates=["month"])
    return df

df = cargar_datos()

# ---------- INTERFAZ ----------
st.title("🌍 Visualización climática por capitales")

columnas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
variable = st.selectbox("📌 Variable a visualizar (tamaño del punto)", columnas_numericas)

# Asegurarse de que 'month' es tipo datetime
df["month"] = pd.to_datetime(df["month"])

# Obtener lista de fechas únicas como objetos datetime (no strings)
fechas_disponibles = sorted(df["month"].dt.to_period("M").drop_duplicates().astype(str))
fecha_str = st.selectbox("🗓️ Selecciona una fecha", fechas_disponibles)

# Convertimos la fecha seleccionada a periodo mensual y comparamos
df_filtrado = df[df["month"].dt.to_period("M").astype(str) == fecha_str]

# Mostrar advertencia si no hay datos
if df_filtrado.empty:
    st.warning(f"⚠️ No hay datos disponibles para la fecha seleccionada: {fecha_str}")
else:
    st.success(f"✅ Mostrando datos para {variable} en {fecha_str}")
    fig = px.scatter_geo(
        df_filtrado,
        lat="latitude",
        lon="longitude",
        color=variable,
        size=variable,
        hover_name="capital",
        projection="natural earth",
        title=f"{variable} en {fecha_str}",
    )
    st.plotly_chart(fig)
