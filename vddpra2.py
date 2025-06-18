
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CARGAR DATOS ----------
@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1PumGCVeb9pBb1VdC3Atm9GoLrxybVfh8"  # tu ID de Drive
    df = pd.read_csv(url, parse_dates=["month"])
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m-%d")  # aseguro que es datetime
    df["month_slider"] = df["month"].dt.date  # necesario para slider
    return df

df = cargar_datos()

# ---------- INTERFAZ DE USUARIO ----------
st.title("🌍 Evolución Climática de Capitales")
st.markdown("Selecciona una variable para visualizar su evolución en el tiempo por capital.")

variables_absolutas = [
    col for col in df.columns
    if col not in ['city_name', 'month', 'month_slider', 'latitude', 'longitude',
                   'country_name', 'sunrise_avg_hhmm', 'sunset_avg_hhmm', 'year',
                   'month_number', 'month_num']
    and not col.startswith("rel_")
]

var_abs = st.selectbox("Selecciona una variable absoluta", variables_absolutas)
var_rel = f"rel_{var_abs}_historico"

# Slider usando valores tipo date
min_fecha = df["month_slider"].min()
max_fecha = df["month_slider"].max()
fecha = st.slider("Selecciona una fecha", min_value=min_fecha, max_value=max_fecha, value=min_fecha, format="YYYY-MM")

# Filtro usando columna auxiliar convertida
df_filtrado = df[df["month_slider"] == fecha]

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
    st.warning("No hay datos para la fecha seleccionada.")
