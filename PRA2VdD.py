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
    df['Fecha'] = df['month'].dt.strftime('%m-%Y')  # Creamos una columna de texto con formato 'MM-YYYY' para la animación
    df = df.sort_values(by=['month'])  # Ordenamos los datos por fecha para que la animación sea cronológica
    return df

# Llamamos a la función y guardamos el resultado en 'df'
df = cargar_datos()

# ---------- VARIABLES DISPONIBLES ----------
# Lista de variables climáticas que el usuario puede seleccionar
variables_disponibles = [
    'temperature_2m_max', 'temperature_2m_min', 'temperature_2m_mean',
    'apparent_temperature_max', 'apparent_temperature_min', 'apparent_temperature_mean',
    'daylight_duration', 'sunshine_duration',
    'precipitation_sum', 'rain_sum', 'snowfall_sum', 'precipitation_hours',
    'wind_speed_10m_max', 'wind_gusts_10m_max', 'shortwave_radiation_sum', 
    'et0_fao_evapotranspiration'
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

# ---------- FORMATEO DE VARIABLES PARA HOVER ----------

# Creamos una columna con el valor de la variable seleccionada
df['valor_variable'] = df[variable]
df['valor_rel'] = df[color_var]

# Diccionario con las columnas que se mostrarán en el hover
hover_data = {
    'Fecha':True,
    'country_name': True,
    'valor_variable': True,
    'valor_rel': True,
    'latitude': False,
    'longitude': False,
    size_var: False,
    color_var: False,
    'month': False,
}

# ---------- ANIMACIÓN GLOBAL ----------
fig = px.scatter_mapbox(
    df,
    lat='latitude',
    lon='longitude',
    hover_name='city_name',
    size=size_var,
    color=color_var,
    animation_frame='Fecha',
    size_max=25,
    zoom=2,
    mapbox_style='open-street-map',
    color_continuous_scale='RdBu_r',
    title=f'Evolución de {variable} mensual (1950–2024)',
    hover_data=hover_data
)

# Creamos un hover personalizado 
fig.update_traces(
    hovertemplate=
        '<b>%{hovertext}</b><br>' +
        'Fecha: %{customdata[0]}<br>' +
        'País: %{customdata[1]}<br>' +
        f'{variable.replace("_", " ").capitalize()}: %{{customdata[2]:.2f}}<br>' +
        'Relativo: %{customdata[3]:.2f}<extra></extra>'
)


# Ajustamos los márgenes del gráfico y la altura
fig.update_layout(margin={'r':0, 't':50, 'l':0, 'b':0}, height=1000)

# Mostramos el gráfico dentro de la aplicación Streamlit
st.plotly_chart(fig, use_container_width=True)

# ---------- EXPLICACIÓN DE LA VISUALIZACIÓN ----------
with st.expander('¿Cómo interpretar esta visualización?'):
    st.markdown('''
Esta visualización interactiva muestra la evolución mensual de varias variables climáticas desde 1950 hasta la actualidad en distintas capitales del mundo.

**¿Cómo funciona?**

- En la parte superior, puedes seleccionar la variable climática que deseas visualizar (por ejemplo: temperatura, precipitación, radiación...).
- La animación te permite avanzar cronológicamente **mes a mes** con el botón del play o seleccionar manualmente una fecha con la barra deslizante.
- Cada círculo representa una capital:
    - **Tamaño del círculo**: representa el valor de la variable seleccionada en esa ciudad y mes, **comparado con otras ciudades en ese mismo mes**.
    - **Color**: indica si ese valor es **más alto o más bajo que su propio histórico mensual**. Es decir:
        - Rojo: valor más alto de lo habitual para esa ciudad en ese mes.
        - Azul: valor más bajo de lo habitual.
        - Blanco: valor cercano a su media histórica mensual.
- Al pasar el ratón sobre un círculo, verás:
    - La ciudad y país
    - La fecha
    - El valor concreto de la variable
    - Su desviación respecto a su histórico (relativo)

Esta representación permite **comparar cómo varía el clima entre capitales y en el tiempo**, destacando anomalías o patrones estacionales globales.
    ''')

# ---------- EXPLICACIÓN DE VARIABLES ----------
# Diccionario con descripciones breves 
descripciones = {
    'temperature_2m_max': 'Temperatura máxima diaria del aire a 2 metros sobre el suelo (°C).',
    'temperature_2m_min': 'Temperatura mínima diaria del aire a 2 metros sobre el suelo (°C).',
    'temperature_2m_mean': 'Temperatura media diaria a 2 metros sobre el suelo (°C).',
    'apparent_temperature_max': 'Sensación térmica máxima diaria combinando viento, humedad y radiación solar.',
    'apparent_temperature_min': 'Sensación térmica mínima diaria combinando viento, humedad y radiación solar.',
    'apparent_temperature_mean': 'Sensación térmica media diaria combinando viento, humedad y radiación solar.',
    'daylight_duration': 'Duración de la luz natural diaria (segundos) entre el amanecer y el atardecer.',
    'sunshine_duration': 'Duración del sol directo diario (segundos) con irradiancia superior a 120 W/m².',
    'precipitation_sum': 'Suma total de precipitación mensual (lluvia + nieve) en milímetros.',
    'rain_sum': 'Cantidad total de lluvia mensual (excluyendo nieve) en milímetros.',
    'snowfall_sum': 'Cantidad total de nieve mensual en centímetros.',
    'precipitation_hours': 'Número de horas diarias con precipitación.',
    'wind_speed_10m_max': 'Velocidad máxima del viento a 10 metros diaria (km/h).',
    'wind_gusts_10m_max': 'Ráfaga máxima de viento a 10 metros diaria (km/h).',
    'shortwave_radiation_sum': 'Suma mensual de radiación solar de onda corta en MJ/m².',
    'et0_fao_evapotranspiration': 'Evapotranspiración de referencia diaria (mm) calculada según FAO Penman-Monteith.'
}

with st.expander('Descripción de la variable seleccionada'):
    descripcion = descripciones.get(variable, 'Descripción no disponible.')
    st.markdown(f'**{variable}**: {descripcion}')
