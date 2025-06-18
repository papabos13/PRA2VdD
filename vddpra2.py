# Importamos las librerías necesarias
import streamlit as st                # Para crear la interfaz web interactiva
import pandas as pd                  # Para manejar datos en forma de tabla
import plotly.express as px          # Para crear gráficos interactivos, como mapas

# Configuramos la página de Streamlit con un título en la pestaña del navegador y ancho completo
st.set_page_config(page_title='Evolución de variables climáticas en las capitales del mundo desde 1950 hasta la actualidad', layout='wide')

# Título principal que se muestra en la aplicación
st.title('Evolución de variables climáticas en las capitales del mundo desde 1950 hasta la actualidad')

# ---------- CARGA DE DATOS ----------
# Esta función carga los datos desde un enlace de Google Drive (archivo CSV)
# La función está cacheada para no volver a cargar si no ha cambiado
@st.cache_data
def cargar_datos():
    url = 'https://drive.google.com/uc?id=1MXhkIsh9Eeq1OEhXuWp8rdiS-TZgR_8n'
    df = pd.read_csv(url, parse_dates=['month'])  # Cargamos el CSV y convertimos 'month' a formato fecha
    df['fecha_str'] = df['month'].dt.strftime('%Y-%m')  # Creamos una columna de texto con formato 'YYYY-MM' para la animación
    df = df.sort_values(by=['month'])  # Ordenamos los datos por fecha para que la animación sea cronológica
    return df

# Llamamos a la función y guardamos el resultado en 'df'
df = cargar_datos()

# ---------- VARIABLES DISPONIBLES ----------
# Lista de variables climáticas que el usuario puede seleccionar
variables_disponibles = [
    'temperature_2m_max', 'temperature_2m_min', 'temperature_2m_mean',
    'apparent_temperature_max', 'apparent_temperature_min', 'apparent_temperature_mean',
    'sunrise_avg_min', 'sunset_avg_min', 'daylight_duration', 'sunshine_duration',
    'precipitation_sum', 'rain_sum', 'snowfall_sum', 'precipitation_hours',
    'wind_speed_10m_max', 'wind_gusts_10m_max', 'wind_direction_10m_dominant',
    'shortwave_radiation_sum', 'et0_fao_evapotranspiration'
]

# ---------- SELECCIÓN DE VARIABLE ----------
# Mostramos un menú desplegable para que el usuario elija la variable a visualizar
variable = st.selectbox('Selecciona la variable climática', variables_disponibles)

# ---------- SIZE Y COLOR ----------
# Lista de variables que tienen versión 'shifted_' (se usan para size cuando hay negativos)
variables_shifted = [
    'temperature_2m_max', 'temperature_2m_min', 'temperature_2m_mean',
    'apparent_temperature_max', 'apparent_temperature_min', 'apparent_temperature_mean'
]

# Si la variable está en la lista de 'shifted', usamos esa como tamaño de burbuja
if variable in variables_shifted:
    size_var = f'shifted_{variable}'  # Nombre de la columna con valores positivos
else:
    size_var = variable  # Si no, usamos directamente la variable

# El color será siempre la variable 'rel_' correspondiente (valor relativo)
color_var = f'rel_{variable}'

# ---------- ANIMACIÓN GLOBAL ----------
# Creamos un mapa animado con Plotly Express
fig = px.scatter_mapbox(
    df,  # DataFrame con los datos
    lat='latitude',  # Columna de latitud
    lon='longitude',  # Columna de longitud
    hover_name='city_name',  # Nombre que aparece al pasar el ratón
    size=size_var,  # Tamaño de los puntos (burbuja)
    color=color_var,  # Color según desviación respecto al histórico
    animation_frame='fecha_str',  # Variable temporal para animar (meses)
    size_max=25,  # Tamaño máximo de las burbujas
    zoom=1,  # Zoom inicial (1 = vista mundial)
    mapbox_style='open-street-map',  # Estilo del mapa (gratuito)
    color_continuous_scale='RdBu_r',  # Escala de color invertida: azul = negativo, rojo = positivo
    title=f'Evolución de {variable} mensual (1950–2024)'  # Título dinámico del gráfico
)

# Ajustamos los márgenes del gráfico y la altura
fig.update_layout(margin={'r':0, 't':50, 'l':0, 'b':0}, height=1000)

# Mostramos el gráfico dentro de la aplicación Streamlit
st.plotly_chart(fig, use_container_width=True)

# ---------- EXPLICACIÓN DE VARIABLES ----------
# Diccionario con descripciones breves (modifícalo o amplíalo a tu gusto)
descripciones = {
    'temperature_2m_max': 'Temperatura máxima a 2 m sobre el suelo (°C).',
    'temperature_2m_min': 'Temperatura mínima a 2 m sobre el suelo (°C).',
    'temperature_2m_mean': 'Temperatura media a 2 m sobre el suelo (°C).',
    'apparent_temperature_max': 'Temperatura aparente (sensación térmica) máxima (°C).',
    'apparent_temperature_min': 'Temperatura aparente mínima (°C).',
    'apparent_temperature_mean': 'Temperatura aparente media (°C).',
    'sunrise_avg_min': 'Hora media (en minutos) del amanecer en el mes.',
    'sunset_avg_min': 'Hora media (en minutos) del atardecer en el mes.',
    'daylight_duration': 'Duración total de luz diurna (segundos).',
    'sunshine_duration': 'Horas de sol directo registradas (segundos).',
    'precipitation_sum': 'Precipitación total mensual (mm).',
    'rain_sum': 'Lluvia total mensual (mm).',
    'snowfall_sum': 'Nieve total mensual (mm).',
    'precipitation_hours': 'Horas con precipitación en el mes.',
    'wind_speed_10m_max': 'Velocidad máxima del viento a 10 m (m/s).',
    'wind_gusts_10m_max': 'Ráfagas máximas de viento a 10 m (m/s).',
    'wind_direction_10m_dominant': 'Dirección dominante del viento a 10 m (grados).',
    'shortwave_radiation_sum': 'Radiación solar de onda corta acumulada (Wh/m²).',
    'et0_fao_evapotranspiration': 'Evapotranspiración potencial FAO (mm).'
}

with st.expander('Descripción de la variable seleccionada'):
    descripcion = descripciones.get(variable, 'Descripción no disponible.')
    st.markdown(f'**{variable}**: {descripcion}')


