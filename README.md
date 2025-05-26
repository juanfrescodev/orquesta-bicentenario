# 🎻 Análisis de Alumnos - Orquesta del Bicentenario Bariloche

Este proyecto analiza la base de datos de alumnos de la **Orquesta del Bicentenario Bariloche**, obtenida desde una hoja de cálculo online. El objetivo es comprender la distribución por instrumento, edad, escuela, antigüedad y otros factores relevantes para la planificación pedagógica y organizativa del proyecto.

---

## 🖼️ Vista previa

### Informe interactivo (HTML):
![Informe](https://github.com/juanfrescodev/orquesta-bicentenario/blob/main/capturas/informe_html.png)

### Mapa interactivo:
![Mapa](https://github.com/juanfrescodev/orquesta-bicentenario/blob/main/capturas/mapa_escuelas.png)

### Archivo ejecutable:
![Mapa](https://github.com/juanfrescodev/orquesta-bicentenario/blob/main/capturas/ejecutable.png)

> 📂 Las capturas están en la carpeta `/capturas/`.

---

## 📁 Archivos incluidos

- `app_orquesta.py`: Script principal que realiza la limpieza, análisis y visualización de datos.
- `/graficos/`: Carpeta con visualizaciones exportadas como imágenes.
- `informe_alumnos_orquesta.html`: Informe interactivo final con gráficos y conclusiones.
- `mapa_escuelas.html`: Mapa interactivo con escuelas que aportan alumnos a la orquesta.
- `README.md`: Este documento.
- `app_orquesta.exe`: Archivo ejecutable para realizar el análisis de manera automática (sin necesidad de conocimientos técnicos).



---

## 🧪 Tecnologías utilizadas

- Python 3
- Pandas
- Matplotlib
- Seaborn
- Folium *(para mapas interactivos)*
- BeautifulSoup *(para generar el HTML final)*
- Google Colab *(como entorno de desarrollo)*

---

## 🎯 Objetivos del análisis

- Visualizar la cantidad de alumnos por instrumento, escuela, grado/año.
- Calcular estadísticas como promedio de edad y antigüedad.
- Detectar desigualdades en la distribución de alumnos.
- Generar visualizaciones interactivas y un informe automático reutilizable.

---

## 📊 Gráficos generados

- Cantidad de alumnos por instrumento  
- Promedio de edad por instrumento  
- Cantidad de alumnos por grado/año  
- Antigüedad promedio en la orquesta  
- Heatmap: Rango de edad vs. instrumento  
- Barras apiladas: Rango de edad vs. instrumento  
- Boxplot de antigüedad por instrumento  
- Cantidad de alumnos por escuela  
- 🗺️ Mapa interactivo: escuelas y cantidad de alumnos aportados

---


## 🚀 Cómo ejecutar el análisis

1. Cloná el repositorio:
   
```bash 
   git clone https://github.com/juanfrescodev/orquesta-bicentenario.git
   cd orquesta-bicentenario
```


2. Instalá las dependencias necesarias (opcional si usás Google Colab):
    
```bash
    pip install pandas matplotlib seaborn folium beautifulsoup4
```


3. Ejecutá el script:
    
```bash
    python orquesta_analisis.py
```

💻 Ejecutar el Análisis sin Necesitar Python
Además del script en Python, también hemos incluido un archivo ejecutable .exe que permite ejecutar el análisis de forma completamente automática. Esto está diseñado para que los trabajadores de la Orquesta del Bicentenario Bariloche puedan reutilizar el análisis sin necesidad de tener conocimientos de programación ni instalar Python.

Para ejecutar el análisis:

Descargá el archivo analisis_orquesta.exe desde esta carpeta.

Ejecutalo en tu computadora.

El programa realizará todo el análisis y generará los resultados automáticamente.

Nota: Este archivo .exe ya contiene todas las dependencias necesarias para que funcione de forma independiente. No es necesario tener Python instalado ni realizar configuraciones adicionales.



💬 Contacto
Este proyecto forma parte de mi portfolio como analista de datos.
Podés contactarme o ver más de mi trabajo en:

GitHub: juanfrescodev

Email: juanfresco1@gmail.com

Portfolio: juanfrescodev.github.io
