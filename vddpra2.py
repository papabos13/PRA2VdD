
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGAR DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1YtEcEhdS9bddZddkCoZO_NkUuavwmLJz"  # tu ID de Drive
    df = pd.read_csv(url, parse_dates=["month"])
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m-%d", errors="coerce")
    df["month_slider"] = df["month"].dt.date  # Necesario para el slider de Streamlit
    return df

df = cargar_datos()

# ---------- CONFIGURACIÓN DE INTERFAZ ----------
st.title("🌍 Visualización climática por capitales")
st.markdown("Selecciona una variable para visualizar su evolución a lo largo del tiempo.")

# Lista de variables absolutas válidas (sin las auxiliares ni las relativas)
variables_absolutas = [
    col for col in df.columns
    if col not in [
        'city_name', 'month', 'month_slider', 'latitude', 'longitude',
        'country_name', 'sunrise_avg_hhmm', 'sunset_avg_hhmm', 'year',
        'month_number', 'month_num'
    ] and not col.startswith("rel_")
]

# Selector de variable absoluta
var_abs = st.selectbox("📌 Variable a visualizar (tamaño del punto)", variables_absolutas)

# Determinar la columna relativa correspondiente
var_rel = f"rel_{var_abs}_historico"

# Slider de fecha
min_fecha = df["month_slider"].min()
max_fecha = df["month_slider"].max()
fecha = st.slider("🗓️ Selecciona una fecha", min_value=min_fecha, max_value=max_fecha, value=min_fecha, format="YYYY-MM")

# Filtrar datos por fecha seleccionada
df_filtrado = df[df["month_slider"] == fecha].copy()

# Quitar filas si la variable relativa tiene muchos NaN
if var_rel in df.columns:
    df_filtrado = df_filtrado.dropna(subset=[var_rel])

# ---------- VISUALIZACIÓN ----------
st.subheader(f"{var_abs} en {fecha.strftime('%B %Y')}")

if not df_filtrado.empty:
    fig = px.scatter_geo(
        df_filtrado,
        lat="latitude",
        lon="longitude",
        hover_name="city_name",
        size=df_filtrado[var_abs].abs(),
        color=var_rel if var_rel in df.columns else None,
        projection="natural earth",
        color_continuous_scale="RdBu",
        title=f"{var_abs} con color relativo {var_rel}" if var_rel in df.columns else f"{var_abs} sin color relativo"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ No hay datos disponibles para la fecha seleccionada.")
