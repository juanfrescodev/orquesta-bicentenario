print("Ejecutando analisis de Orquesta del Bicentenario Bariloche")
print("Se generaran en la misma carpeta donde está este archivo:")
print("mapa interactivo: mapa_escuelas.html")
print("analisis: informe_alumnos_orquesta.html")
print("gráficos representativos")

import pandas as pd
from datetime import date, datetime
import seaborn as sns
import matplotlib.pyplot as plt
import re
import sys
import folium
import base64
from bs4 import BeautifulSoup
from textwrap import dedent
import pandas as pd # Make sure pandas is imported
from datetime import date, datetime # Make sure datetime is imported
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
from bs4 import BeautifulSoup
from textwrap import dedent
import os
import sys



print("Obteniendo base de datos desde planilla alumnos online...")
# ID del documento y GID de la hoja
sheet_id = "1xtA2hKqrtjuQ8CyB-phhACHK_q14wG-o"
gid = "793729635"

# URL para leer como CSV
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Saltar las primeras 2 filas (títulos o comentarios vacíos)
df = pd.read_csv(url, skiprows=2)


print("ordenando datos...")
# Renombrar columnas
df.rename(columns={
    'Feche Nac.': 'Fecha Nac.',
    'grado/año': 'Grado/Año',
    'en inclusion': 'En Inclusión',
    'Tpo de disco': 'Tipo de Disco'
}, inplace=True)

# Eliminar columnas innecesarias
df.drop(columns=['En Inclusión', 'Tipo de Disco', 'observaciones'], inplace=True)

# Convertir 'Fecha Nac.' a datetime
df['Fecha Nac.'] = pd.to_datetime(df['Fecha Nac.'], errors='coerce')

# Diccionario con los valores correctos de 'Fecha Nac.' para personas con datos mal cargados
fechas_corregidas = {
    'Coutada Josefina': '02/10/2012',
    'Escobar Luciano': '01/10/2008',
    'Flores Sol Carolina': '16/01/2008',
    'Molina Vespa Jazmín': '26/04/2011',
    'Pacheco Brianna': '24/04/2015',
    'Yapura Daiana Aylen': '16/10/2012'
}
# Convertir las fechas al formato datetime
for nombre, fecha in fechas_corregidas.items():
    df.loc[df['Nombre y Apellido'] == nombre, 'Fecha Nac.'] = pd.to_datetime(fecha, format='%d/%m/%Y')
# Limpiar espacios y hacer la búsqueda insensible a mayúsculas/minúsculas
df['Nombre y Apellido'] = df['Nombre y Apellido'].str.strip().str.lower()
# Corregir las fechas para las filas específicas
df.loc[df['Nombre y Apellido'] == 'calfuleo valle micaela', 'Fecha Nac.'] = '29/11/2012'
df.loc[df['Nombre y Apellido'] == 'fulgueiras camilo', 'Fecha Nac.'] = '26/04/2011'


print("agrupando datos...")
#agrupar por instrumento
#Diccionario para corregir nombres con errores de escritura que refieren a un mismo instrumento
df['Instrumento'] = df['Instrumento'].str.strip().str.lower()
instrumento_corregido = {
    'violin 1': 'Violín 1',
    'violin 2': 'Violín 2',
    'violin 3': 'Violín 3',
    'violin 4': 'Violín 4',
    'violín 1': 'Violín 1',
    'violín 2': 'Violín 2',
    'violín 3': 'Violín 3',
    'violín 4': 'Violín 4',
    'violin': 'Violín',
    'Violín': 'Violín',
    'percusion': 'Percusión',
    'trombon': 'Trombón',
    'violonchelo': 'Violoncello',
    'violoncello': 'Violoncello'
}
for nombre, instrumento in instrumento_corregido.items():
    df.loc[df['Instrumento'] == nombre, 'Instrumento'] = instrumento

# Calcular el promedio de edad por instrumento
edad_promedio = df.groupby('Instrumento')['Edad'].mean().sort_values(ascending=False)

#Agrupar por escuela
#limpiar espacios
df["Escuela"] = df["Escuela"].str.strip()
#contar alumnas por escuela
conteo_alumnos = df.groupby("Escuela").size().reset_index(name="cantidad_alumnos")

#cantidad de alumnos por grado/año
df['Grado/Año'] = df['Grado/Año'].astype(str).str.strip().str.lower()
correcciones_grado = {
    '1 año': '1° año',
    '1er año': '1° año',
    '1° año': '1° año',
    '1°año': '1° año',
    '1°': '1° año',
    '1 an̈o': '1° año',
    'primer año': '1° año',
    '2año' : '2° año',
    '2do año': '2° año',
    '2do': '2° año',
    '2do año': '2° año',
    '2° año': '2° año',
    '2 año': '2° año',
    '3ro año': '3° año',
    '4to año': '4° año',
    '4 año': '4° año',
    '4° año': '4° año',
    '4to': '4° año',
    '4mo': '4° año',
    '4mo año': '4° año',
    '4 to año': '4° año',
    '5 año': '5° año',
    '5° año': '5° año',
    '5to': '5° año',
    '5to año': '5° año',
    '5mo': '5° año',
    '5mo año': '5° año',
    '5' : '5° año',
    '6to año': '6° año',
    '6° año': '6° año',
    '6to': '6° año',
    '6 to': '6° año',
    '6mo': '6° año',
    '6mo año': '6° año',
    '7 año': '7° año',
    '1° año': '1° año',
    '3 año': '3° año',
    "3'año": '3° año',
    '3° año': '3° año',
    '3er año': '3° año',
    '4° año': '4° año',
    '5° año': '5° año',
    '6° año': '6° año',
    '7° año': '7° año',
    '7 grado': '7° grado',
    '7° grado': '7° grado',
    '7mo': '7° grado',
    '7 mo': '7° grado',
    '7mo grado': '7° grado',
    '7 mo grado': '7° grado',
    '7°': '7° grado',
    '7° grado': '7° grado',
    '6to grado': '6° grado',
    '6 grado': '6° grado',
    '5t0 grado': '5° grado',
    '5 grado': '5° grado',
    '5º grado': '5° grado',
    '5to grado': '5° grado',
    '4 grado': '4° grado',
    '4to grado': '4° grado',
    '4° grado': '4° grado',
    '1 grado': '1° grado',
    '2 grado': '2° grado',
    '3 grado': '3° grado',
    '1 cuatrimestre' : 'Otro',
    'pasteleria': 'Otro',
    'chocolateria': 'Otro',
    '2 cuatrimestres': 'Otro',
    '': 'Otro',
    'nan': 'Otro',
}

df['Grado Normalizado'] = df['Grado/Año'].map(correcciones_grado)

#calcular antiguedad
año_actual = datetime.now().year
df['Antigüedad'] = año_actual - df['INGRESO']
df = df[~df['Antigüedad'].isin([float('nan'), float('inf'), -float('inf')])]
df['Antigüedad'] = df['Antigüedad'].astype(int)
prom_antiguedad = df.groupby('Instrumento')['Antigüedad'].mean().sort_values(ascending=False)

#rangos de edad
df['Rango Edad'] = pd.cut(df['Edad'], bins=[6, 10, 13, 18, 99], labels=['Niño', 'Preadolescente', 'Adolescente', 'Adulto'], right=True)
tabla = pd.crosstab(df['Instrumento'], df['Rango Edad'])

print("dibujando mapa...")
#Mapa
coordenadas_manuales = {
    "CEM 105": (-41.14120327353672, -71.30405995962707),
    "CEM 36": (-41.15344634515291, -71.3074845075138),
    "CEM 45": (-41.13904403118103, -71.30744244613582),
    "CEM 46": (-41.13273365903047, -71.29034413635121),
    "CEM 97": (-41.170291085568486, -71.3389704038061),
    "CET 2": (-41.12893469585726, -71.28336813264498),
    "CET 25": (-41.128769776917544, -71.28379171730035),
    "CET 28": (-41.16145838713428, -71.32615463210459),
    "COLEGIO DEL SOL": (-41.13137699946679, -71.35964947497244),
    "COLEGIO SAN ESTEBAN": (-41.13996994842761, -71.30786876682544),
    "COLEGIO TECNOLÓGICO DEL SUR": (-41.13886275104532, -71.30607101729967),
    "COLEGIO TÉCNICO JORGE NEWERY": (-34.65606399436127, -58.58874500234522),
    "CRN 96 DINA HUAPI": (-41.07576037036012, -71.16777123653277),
    "DON BOSCO": (-41.13612905957176, -71.3024467474372),
    "EL OBRADOR ESCUELA DE COCINA": (-41.136045145991865, -71.31391564452599),
    "EP 284": (-41.14886177944396, -71.30885270380755),
    "EP 320": (-41.1551421687666, -71.30174724613475),
    "ESRN 123": (-41.1228726228412, -71.40584223079206),
    "ESRN 132": (-41.14133275345476, -71.30374654798887),
    "ESRN 138": (-41.146823685065506, -71.26967180195439),
    "ESRN 33": (-41.1512801996282, -71.29906626822654),
    "ESRN 36": (-41.153373640633966, -71.30747377867763),
    "ESRN 45": (-41.13905211123045, -71.30749609031672),
    "ESRN 20": (-41.14076847300108, -71.30469770566127),
    "ESRN 37": (-41.13246418192254, -71.28980841730004),
    "Escuela 284": (-41.148877937122606, -71.30876687311809),
    "Escuela 187": (-41.14173605685861, -71.31191413264418),
    "Escuela 266": (-41.1333841253819, -71.29185808846378),
    "Escuela 267": (-41.149921878649046, -71.29966020499035),
    "Escuela 273": (-41.141247534290265, -71.30511634798894),
    "Escuela 278": (-41.15225988715826, -71.30522137497114),
    "Escuela 295": (-41.15185037281309, -71.29215709031583),
    "Escuela 312 DINA HUAPI": (-41.07686271867368, -71.16816605150322),
    "Escuela 315": (-41.16751359983633, -71.31665769031486),
    "Escuela 328": (-41.150379556719415, -71.29772914613507),
    "Escuela 324": (-41.15917700789762, -71.41699753449636),
    "Escuela DE HOTELERÍA": (-41.12870512636184, -71.28379171730035),
    "Escuela DE OFICIOS": (-41.13922859108756, -71.30737721915288),
    "Escuela SIGLO XXI": (-41.1275432279167, -71.36212895376312),
    "Escuela DON BOSCO": (-41.13612905957176, -71.3024467474372),
    "Escuela Antu Ruca": (-41.14078887302621, -71.30027771915279),
    "Escuela 154": (-41.161850398975915, -71.32578027311733),
    "FASTA": (-41.13929438072877, -71.31667852375585),
    "INSTITUTO SUPERIOR PATAGÓNICO": (-41.14036844938471, -71.31233699566144),
    "JORGE NEWBERY CET 2": (-41.12884580155019, -71.2833037596279),
    "LOS ANDES": (-41.144688671926424, -71.29397575427554),
    "MARÍA AUXILIADORA": (-41.13978948863875, -71.30344397846365),
    "NEHUEN PEHUMAN": (-41.15679775988216, -71.31502257497081),
    "NUESTRA SEÑORA DE LA VIDA": (-41.1676609246654, -71.33624085147082),
    "SIGLO XXI": (-41.1275432279167, -71.36212895376312),
    "UNIVERSIDAD DE RÍO NEGRO": (-41.14150989017697, -71.31332403412632),
    "UNIVERSIDAD DEL COMAHUE": (-41.144490393582174, -71.31595050544496)
}
#Crear mapa
# 1. Limpiar nombres
df["Escuela"] = df["Escuela"].str.strip()

# 2. Contar alumnos
conteo_alumnos = df.groupby("Escuela").size().reset_index(name="cantidad_alumnos")

# 3. Coordenadas -> DataFrame
df_coords = pd.DataFrame.from_dict(coordenadas_manuales, orient='index', columns=["lat", "lon"])
df_coords.reset_index(inplace=True)
df_coords.rename(columns={"index": "Escuela"}, inplace=True)

# 4. Unir coordenadas + conteo
df_mapa = df_coords.merge(conteo_alumnos, on="Escuela", how="left")
df_mapa["cantidad_alumnas"] = df_mapa["cantidad_alumnos"].fillna(0).astype(int)

# 5. Función para color según cantidad
def color_por_cantidad(cantidad):
    if cantidad < 2:
        return "green"
    elif cantidad < 4:
        return "orange"
    else:
        return "red"

# 6. Crear mapa
mapa = folium.Map(location=[-41.1335, -71.3103], zoom_start=12)

# 7. Agregar marcadores y círculos
for _, fila in df_mapa.iterrows():
    popup_texto = f"{fila['Escuela']}<br>Cantidad de alumnos: {fila['cantidad_alumnos']}"
    color = color_por_cantidad(fila["cantidad_alumnos"])    
    
    # Agregar círculo proporcional
    folium.CircleMarker(
        location=[fila["lat"], fila["lon"]],
        radius=3 + fila["cantidad_alumnos"] * 4,  # Escala ajustable
        color=color,
        fill=True,
        fill_opacity=0.6,
        popup=popup_texto
    ).add_to(mapa)

# 8. Guardar
# Guardar el mapa como archivo HTML
mapa_path = "mapa_escuelas.html"
mapa.save(mapa_path)

print("creando gráficos...")
#GRAFICOS
#grafico de cantidad de alumnos por instrumento
instrumento = df['Instrumento'].value_counts()
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Instrumento', order= instrumento.index)
plt.title('Distribución de Instrumentos')
plt.xlabel('Instrumento')
plt.ylabel('Alumnos')
plt.xticks(rotation=45)
plt.savefig('grafico_instrumentos.png')
plt.close()


#grafico de promedio de edad por instrumento
plt.figure(figsize=(12, 6))  # Aumentamos el tamaño de la figura
sns.barplot(x=edad_promedio.index, y=edad_promedio.values)
plt.title('Promedio de Edad por Instrumento')
plt.xlabel('Instrumento')
plt.ylabel('Promedio de Edad')
# Ajustar la rotación de las etiquetas y añadir espacio
plt.xticks(rotation=45, ha='right', rotation_mode='anchor', fontsize=10, fontweight='bold')  # Ajustar el ángulo y la alineación
plt.tight_layout()  # Ajusta el espacio automáticamente para evitar que se sobrepongan
plt.savefig('grafico_edad.png')
plt.close()

#grafico de cantidad de musicos por grado/año
plt.figure(figsize=(10,6))
sns.countplot(data=df, x='Grado Normalizado', order=df['Grado Normalizado'].value_counts().index)
plt.title('Distribución de Alumnos por Grado/Año')
plt.xlabel('Grado/Año')
plt.ylabel('Cantidad de Alumnos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_grado.png')
plt.close()

#grafico de antiguedad de alumnos
sns.countplot(x='Antigüedad', data=df, hue='Antigüedad', palette='viridis', legend=False)
plt.title('Distribución de Antigüedad en la Orquesta')
plt.xlabel('Años en la orquesta')
plt.ylabel('Cantidad de estudiantes')
plt.savefig('grafico_antiguedad.png')
plt.close()

#grafico heatmap cruce rango de edad vs instrumento
plt.figure(figsize=(12, 8))
sns.heatmap(tabla, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Distribución de Rangos de Edad por Instrumento")
plt.xlabel("Rango de Edad")
plt.ylabel("Instrumento")
plt.savefig('grafico_edad_vs_instrumento.png')
plt.close()

#grafico de barras cruce rango de edad vs instrumento
tabla.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title("Distribución de Rangos de Edad por Instrumento")
plt.xlabel("Instrumento")
plt.ylabel("Cantidad")
plt.legend(title="Rango de Edad")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_edad_vs_instrumento_barras.png')
plt.close()

#grafico heatmap edad vs instrumento
tabla_edad = pd.crosstab(df['Instrumento'], df['Edad'])
plt.figure(figsize=(14, 8))
sns.heatmap(tabla_edad, cmap='YlOrRd', annot=True, fmt='d')
plt.title('Cantidad de Alumnos por Edad Exacta e Instrumento')
plt.xlabel('Edad')
plt.ylabel('Instrumento')
plt.savefig('grafico_edad_vs_instrumento_heatmap.png')
plt.close()

#promedio de antiguedad y instrumento
prom_antiguedad.plot(kind='barh', figsize=(10, 6))
plt.title('Antigüedad Promedio por Instrumento')
plt.xlabel('Años')
plt.ylabel('Instrumento')
plt.savefig('grafico_antiguedad_instrumento.png')
plt.close()

#Distribución de antiguedad por instrumento
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Instrumento', y='Antigüedad')
plt.title('Distribución de Antigüedad por Instrumento')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_antiguedad_instrumento_boxplot.png')
plt.close()

#grafico cantidad de alumnos por escuela
# Ordenar por cantidad y graficar
df_ordenado = df_mapa.sort_values('cantidad_alumnas', ascending=False)

plt.figure(figsize=(12, max(6, len(df_ordenado) * 0.5)))  # altura proporcional a cantidad de escuelas
sns.barplot(x='cantidad_alumnas', y='Escuela', data=df_ordenado, hue='Escuela', palette='viridis', legend=False)
plt.title('Cantidad de Alumnos por Escuela')
plt.xlabel('Cantidad de Alumnos')
plt.ylabel('Escuela')
plt.tight_layout()
plt.savefig('grafico_escuelas.png')
plt.close()

#Exportar datos en HTML
print("exportando informe...")



# Diccionario con nombre lógico e imagen convertida
imagenes_base64 = {
    "grafico_instrumentos": img_to_base64("grafico_instrumentos.png"),
    "grafico_edad": img_to_base64("grafico_edad.png"),
    "grafico_grado": img_to_base64("grafico_grado.png"),
    "grafico_antiguedad": img_to_base64("grafico_antiguedad.png"),
    "grafico_edad_vs_instrumento": img_to_base64("grafico_edad_vs_instrumento.png"),
    "grafico_edad_vs_instrumento_barras": img_to_base64("grafico_edad_vs_instrumento_barras.png"),
    "grafico_antiguedad_instrumento_boxplot": img_to_base64("grafico_antiguedad_instrumento_boxplot.png"),
    "grafico_escuelas": img_to_base64("grafico_escuelas.png"),
}

# Leer el HTML del mapa generado con Folium
with open("mapa_escuelas.html", "r", encoding="utf-8") as f:
    mapa_html = f.read()



# Extraer head y body por separado
soup = BeautifulSoup(mapa_html, "html.parser")
mapa_div = soup.find("div")  # este es el mapa (div id="map")
mapa_scripts = soup.find_all("script")  # todos los <script> que Folium necesita
mapa_styles = soup.find_all("style")  # estilos internos
mapa_links = soup.find_all("link")    # posibles hojas de estilo externas

# Convertir a string HTML
mapa_div_html = str(mapa_div)
scripts_html = "\n".join(str(tag) for tag in mapa_scripts)
styles_html = "\n".join(str(tag) for tag in mapa_styles)
links_html = "\n".join(str(tag) for tag in mapa_links)

#informe automatico


# =====================
# 🔍 Análisis avanzado
# =====================

# Cantidad total
total_alumnos = len(df)
total_escuelas = df['Escuela'].nunique()
total_instrumentos = df['Instrumento'].nunique()
total_grados = df['Grado/Año'].nunique()

# Estadísticas clave
escuela_mas_alumnos = df['Escuela'].value_counts().idxmax()
escuela_menos_alumnos = df['Escuela'].value_counts().idxmin()
instrumento_mas_usado = df['Instrumento'].value_counts().idxmax()
instrumento_menos_usado = df['Instrumento'].value_counts().idxmin()
edad_prom = df['Edad'].mean()
edad_std = df['Edad'].std()
antiguedad_prom = df['Antigüedad'].mean()

# Detección de dispersión
dispersión_edad = "alta" if edad_std > 2.5 else "moderada" if edad_std > 1.5 else "baja"

# Grado con más alumnos
grado_mas_comun = df['Grado/Año'].mode().iloc[0]

# Análisis de equilibrio
alumnos_por_escuela = df['Escuela'].value_counts()
escuelas_desequilibradas = alumnos_por_escuela[alumnos_por_escuela < (total_alumnos / total_escuelas * 0.5)].index.tolist()

alumnos_por_instrumento = df['Instrumento'].value_counts()
instrumentos_desequilibrados = alumnos_por_instrumento[alumnos_por_instrumento < (total_alumnos / total_instrumentos * 0.5)].index.tolist()

# Generar texto
texto_analisis_avanzado = f"""
<h2>🧠 Análisis Avanzado y Conclusiones</h2>

<p>El total de alumnos registrados es de <strong>{total_alumnos}</strong>, distribuidos en <strong>{total_escuelas}</strong> escuelas, <strong>{total_instrumentos}</strong> instrumentos y <strong>{total_grados}</strong> grados escolares.</p>

<p>La escuela con más alumnos es <strong>{escuela_mas_alumnos}</strong>, mientras que <strong>{escuela_menos_alumnos}</strong> tiene la menor participación.</p>

<p>El instrumento más elegido es <strong>{instrumento_mas_usado}</strong>, en contraste con <strong>{instrumento_menos_usado}</strong>, que presenta menor cantidad de inscriptos.</p>

<p>La edad promedio es de <strong>{edad_prom:.1f} años</strong>, con una dispersión <strong>{dispersión_edad}</strong>, lo que indica que {"hay perfiles de edades muy variados" if dispersión_edad == "alta" else "las edades están relativamente concentradas"}.</p>

<p>El grado más representado es <strong>{grado_mas_comun}</strong>, y la antigüedad promedio de los alumnos en la orquesta es de <strong>{antiguedad_prom:.1f} años</strong>.</p>

<h3>⚠️ Observaciones y desigualdades detectadas</h3>
<ul>
    {"<li>Algunas escuelas con baja representación: <strong>" + ', '.join(escuelas_desequilibradas) + "</strong></li>" if escuelas_desequilibradas else ""}
    {"<li>Instrumentos con pocos alumnos: <strong>" + ', '.join(instrumentos_desequilibrados) + "</strong></li>" if instrumentos_desequilibrados else ""}
</ul>

<h3>✅ Recomendaciones</h3>
<ul>
    {"<li>Reforzar la convocatoria en escuelas con baja participación.</li>" if escuelas_desequilibradas else ""}
    <li>Evaluar si la dispersión de edades requiere adaptar métodos pedagógicos por grupo.</li>
</ul>
"""


# Crear HTML del informe final (incrustando estilos + div + scripts del mapa)
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Análisis de Alumnos - Orquesta del Bicentenario Bariloche</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f9f9f9;
        }}
        h1 {{
            color: #2c3e50;
        }}
        h2 {{
            color: #34495e;
            margin-top: 40px;
        }}
        img {{
            max-width: 800px;
            width: 100%;
            margin-top: 10px;
            margin-bottom: 40px;
            border: 1px solid #ccc;
            padding: 10px;
            background: white;
        }}
        footer {{
            margin-top: 60px;
            font-size: 14px;
            color: #555;
        }}
    </style>
    {links_html}
    {styles_html}
</head>
<body>

<h1>Análisis de Alumnos - Orquesta del Bicentenario Bariloche</h1>

<p>Este informe analiza la distribución de alumnos según escuela, instrumento y edad, en el marco del proyecto educativo de la Orquesta del Bicentenario Bariloche.</p>

{texto_analisis_avanzado}

<h2>📊 Cantidad de alumnos por instrumento</h2>
<img src="data:image/png;base64,{imagenes_base64['grafico_instrumentos']}" alt="Cantidad de alumnos por instrumento">

<h2>📊 Promedio de edad por instrumento</h2>
<img src="data:image/png;base64,{imagenes_base64['grafico_edad']}" alt="Promedio de edad por instrumento">

<h2>📊 Cantidad de alumnos por grado/año</h2>
<img src="data:image/png;base64,{imagenes_base64['grafico_grado']}" alt="Cantidad de alumnos por grado/año">

<h2>📊 Antigüedad en la Orquesta</h2>
<img src="data:image/png;base64,{imagenes_base64['grafico_antiguedad']}" alt="Antigüedad en la Orquesta">

<h2>📈 Heatmap: Rango de Edad vs Instrumento</h2>
<img src="data:image/png;base64,{imagenes_base64['grafico_edad_vs_instrumento']}" alt="Heatmap: Rango de Edad vs Instrumento">

<h2>📊 Barras Apiladas: Rango de Edad vs Instrumento</h2>
<img src="data:image/png;base64,{imagenes_base64['grafico_edad_vs_instrumento_barras']}" alt="Barras Apiladas: Rango de Edad vs Instrumento">

<h2>📊 Boxplot de Antigüedad por Instrumento</h2>
<img src="data:image/png;base64,{imagenes_base64['grafico_antiguedad_instrumento_boxplot']}" alt="Boxplot de Antigüedad por Instrumento">

<h2>📊 Cantidad de alumnos por escuela</h2>
<img src="data:image/png;base64,{imagenes_base64['grafico_escuelas']}" alt="Cantidad de alumnos por escuela">

<h2>🗺️ Mapa interactivo con escuelas y cantidad de alumnos aportados a la orquesta</h2>
{mapa_div_html}

<footer>
    <p><strong>Juan Fresco</strong><br>
    📧 juanfrescodev@gmail.com<br>
    💻 <a href="https://github.com/juanfrescodev" target="_blank">github.com/juanfrescodev</a></p>
</footer>

{scripts_html}

</body>
</html>
"""


# Guardar el archivo HTML final


# Determinar el directorio correcto, dependiendo si estamos en un .exe o .py
if getattr(sys, 'frozen', False):
    # Si estamos ejecutando el archivo como un .exe con PyInstaller
    script_dir = os.path.dirname(sys.executable)
else:
    # Si estamos ejecutando desde el archivo .py
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Verificamos el directorio en el que estamos
print(f"Directorio actual donde se guarda el HTML: {script_dir}")

# Crear la ruta completa para el archivo HTML
html_file_path = os.path.join(script_dir, "informe_alumnos_orquesta.html")

# Guardar el archivo HTML final
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Informe HTML generado con éxito como '{html_file_path}'")

