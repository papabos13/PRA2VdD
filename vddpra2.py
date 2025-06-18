
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGAR DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1PumGCVeb9pBb1VdC3Atm9GoLrxybVfh8"  # tu ID de Drive
    df = pd.read_csv(url, parse_dates=["month"])
    return df

df = cargar_datos()

# ---------- INTERFAZ DE USUARIO ----------
st.title("🌍 Evolución Climática de Capitales")
st.markdown("Selecciona una variable para visualizar su evolución en el tiempo por capital.")

# Variables absolutas (excluyendo columnas auxiliares)
variables_absolutas = [col for col in df.columns if col not in ['city_name', 'month', 'latitude', 'longitude'] and not col.startswith('rel_')]

# Selección de variable
var_abs = st.selectbox("Selecciona una variable absoluta", variables_absolutas)

# Derivar el nombre de la variable relativa correspondiente
var_rel = f"rel_{var_abs}_historico"

# Convertir a tipo date para evitar errores en st.slider
df["month"] = pd.to_datetime(df["month"])
df["month_date"] = df["month"].dt.date  # <- importante para slider

# Selección de fecha
min_fecha = df["month_date"].min()
max_fecha = df["month_date"].max()
fecha = st.slider("Selecciona una fecha", min_value=min_fecha, max_value=max_fecha, value=min_fecha, format="YYYY-MM")

# Filtrar datos por fecha seleccionada
df_filtrado = df[df["month_date"] == fecha].copy()


# ---------- VISUALIZACIÓN ----------
st.subheader(f"{var_abs} en {fecha.strftime('%B %Y')}")

fig = px.scatter_geo(
    df_filtrado,
    lat="latitude",
    lon="longitude",
    hover_name="city_name",
    size=df_filtrado[var_abs].abs(),
    color=var_rel if var_rel in df.columns else None,
    projection="natural earth",
    color_continuous_scale="RdBu",
    title=f"{var_abs} con color relativo {var_rel}" if var_rel in df.columns else f"{var_abs} sin color relativo",
)

st.plotly_chart(fig, use_container_width=True)
