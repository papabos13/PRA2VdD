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
st.title("🌍 Mapa climático por capitales")

# Mostrar columnas numéricas disponibles para seleccionar
columnas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# Selección de variable
variable = st.selectbox("Selecciona la variable a visualizar:", columnas_numericas)

# Selección de fecha (opcional si hay columna 'month')
if "month" in df.columns:
    fechas_disponibles = sorted(df["month"].unique())
    fecha_seleccionada = st.selectbox("Selecciona la fecha:", fechas_disponibles)
    df_filtrado = df[df["month"] == fecha_seleccionada]
else:
    df_filtrado = df.copy()

# ---------- MAPA ----------
if all(col in df_filtrado.columns for col in ["latitude", "longitude"]):
    fig = px.scatter_geo(
        df_filtrado,
        lat="latitude",
        lon="longitude",
        color=variable,
        size=variable,
        hover_name="capital",
        projection="natural earth",
        title=f"Distribución geográfica de {variable}",
    )
    st.plotly_chart(fig)
else:
    st.error("❌ El dataset no tiene columnas de latitud o longitud.")

