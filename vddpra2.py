import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1c3Ok49GNhWxgdDAxOPISMTDUd9SyWE2v"
    df = pd.read_csv(url, parse_dates=["month"])
    df["year"] = df["month"].dt.year
    df["month_num"] = df["month"].dt.month
    return df

df = cargar_datos()

st.title("🌍 Visualización climática por capitales")

variables_disponibles = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
    "sunrise_avg_min", "sunset_avg_min", "daylight_duration", "sunshine_duration",
    "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours",
    "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration"
]

variable = st.selectbox("📊 Variable climática:", variables_disponibles)

# Ordenamos por ciudad y fecha para garantizar el orden cronológico
df.sort_values(by=["city_name", "month"], inplace=True)

# Agrupamos por ciudad y mes para evitar cálculos innecesarios
rel_values = []
for (ciudad, mes), grupo in df.groupby(["city_name", "month_num"]):
    historico = []
    for i, fila in grupo.iterrows():
        pasado = [v for v in historico if pd.notnull(v)]
        if len(pasado) > 1:
            media = sum(pasado) / len(pasado)
            std = pd.Series(pasado).std()
            valor = (fila[variable] - media) / std if std != 0 else None
        else:
            valor = None
        rel_values.append(valor)
        historico.append(fila[variable])

df["rel_value_historico"] = rel_values

# Crear animación con Plotly
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    size=df[variable].abs(),
    color="rel_value_historico",
    animation_frame=df["month"].dt.strftime("%Y-%m"),
    hover_name="city_name",
    hover_data=["country_name", variable],
    color_continuous_scale="RdBu_r",
    size_max=15,
    zoom=1
)

fig.update_layout(
    mapbox_style="carto-positron",
    title=f"Evolución histórica de {variable} respecto a datos anteriores",
    height=750,
    width=1100
)

st.plotly_chart(fig, use_container_width=False)



