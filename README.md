# Proyecto de Extracción de Datos Inmobiliarios en México

## Descripción

Este proyecto implementa un proceso automatizado de extracción, transformación y almacenamiento de datos inmobiliarios publicados en VivaAnuncios para diversas ciudades de México.

El sistema utiliza Selenium para acceder y renderizar páginas web dinámicas, BeautifulSoup para analizar el contenido HTML y Pandas para procesar y almacenar la información obtenida. Los datos recolectados corresponden a series históricas de precios de vivienda y se almacenan de forma acumulativa en un archivo CSV.

El objetivo principal es construir un conjunto de datos histórico que permita analizar tendencias del mercado inmobiliario en distintas ciudades mexicanas.

---

# Objetivos

- Automatizar la recolección de información inmobiliaria.
- Obtener datos históricos de precios por ciudad.
- Consolidar información de múltiples ubicaciones en un único dataset.
- Mantener un histórico actualizado sin generar registros duplicados.
- Facilitar análisis posteriores mediante herramientas de ciencia de datos.

---

# Tecnologías Utilizadas

## Lenguaje de Programación

- Python 3

## Librerías

- Selenium
- BeautifulSoup4
- Pandas
- JSON
- OS
- Time

## Herramientas

- Google Chrome
- ChromeDriver

---

# Arquitectura del Sistema

```text
Sitio Web (VivaAnuncios)
           │
           ▼
      Selenium
(Renderizado dinámico)
           │
           ▼
     BeautifulSoup
 (Extracción HTML)
           │
           ▼
   Procesamiento JSON
           │
           ▼
        Pandas
           │
           ▼
 Consolidación de Datos
           │
           ▼
Archivo CSV Histórico
```

---

# Estructura del Proyecto

```text
proyecto/
│
├── scraper.py
├── dataset_vivienda_mexico.csv
├── requirements.txt
└── README.md
```

---

# Funcionamiento General

El script realiza las siguientes tareas:

1. Accede a la página web de cada ciudad utilizando Selenium.
2. Espera la carga completa del contenido dinámico.
3. Obtiene el código fuente HTML generado.
4. Busca el componente que contiene los datos estadísticos.
5. Extrae la información en formato JSON.
6. Convierte los datos a un DataFrame de Pandas.
7. Agrega la ciudad correspondiente a cada registro.
8. Une la información de todas las ciudades procesadas.
9. Actualiza el dataset histórico.
10. Elimina registros duplicados.
11. Guarda el resultado final en un archivo CSV.

---

# Ciudades Analizadas

Actualmente el sistema extrae información de:

- Guadalajara
- La Paz
- Mexicali

La lista puede ampliarse agregando nuevas ciudades dentro de la variable:

```python
ciudades = [
    {
        "nombre": "Ciudad",
        "url": "https://..."
    }
]
```

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/proyecto-inmobiliario.git

cd proyecto-inmobiliario
```

## 2. Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install selenium beautifulsoup4 pandas
```

O utilizando:

```bash
pip install -r requirements.txt
```

---

# Ejecución

Ejecutar el script:

```bash
python scraper.py
```

Durante la ejecución se mostrará un mensaje por cada ciudad procesada:

```text
Extrayendo Guadalajara...
Extrayendo LaPaz...
Extrayendo Mexicali...
```

Una vez finalizado:

```text
Dataset actualizado y guardado
```

---

# Formato del Dataset

El archivo generado contiene la siguiente estructura:

| Campo | Descripción |
|---------|-------------|
| fecha | Fecha del registro |
| precio | Precio promedio obtenido |
| ciudad | Ciudad analizada |

Ejemplo:

| fecha | precio | ciudad |
|---------|---------|---------|
| 2024-01-01 | 24000 | Guadalajara |
| 2024-01-01 | 18500 | LaPaz |
| 2024-01-01 | 21000 | Mexicali |

---

# Gestión de Duplicados

El sistema evita almacenar registros repetidos mediante la siguiente lógica:

```python
df_total = df_total.drop_duplicates(
    subset=["fecha", "ciudad"]
)
```

De esta forma, cada combinación de fecha y ciudad aparece una sola vez dentro del conjunto de datos.

---

# Seguridad de los Datos

## Acceso Exclusivamente a Información Pública

El script extrae únicamente información disponible públicamente en el sitio web analizado.

No realiza acciones de:

- Autenticación.
- Inicio de sesión.
- Acceso a información privada.
- Acceso a datos personales de usuarios.

---

## Minimización de Datos

El dataset únicamente almacena:

- Fecha.
- Precio.
- Ciudad.

No se recopilan datos personales como:

- Nombres.
- Correos electrónicos.
- Teléfonos.
- Direcciones particulares.
- Información financiera de usuarios.

---

## Integridad de la Información

Antes de guardar los datos:

- Se convierten las fechas a formato estándar.
- Se eliminan registros duplicados.
- Se consolidan múltiples fuentes en un único conjunto de datos.

Esto mejora la calidad y consistencia del dataset final.

---

## Uso Responsable del Web Scraping

Para reducir la carga sobre el sitio web, el proyecto:

- Consulta únicamente un conjunto limitado de ciudades.
- Realiza una pausa durante la carga de las páginas.
- Evita solicitudes masivas simultáneas.
- Extrae exclusivamente la información necesaria para el análisis.

---

## Riesgos y Limitaciones

El funcionamiento del sistema depende de la estructura actual del sitio web.

Cambios en:

- HTML.
- Clases CSS.
- Estructura de datos JSON.
- Elementos del DOM.

pueden afectar la capacidad de extracción y requerir modificaciones en el código.

---

# Posibles Mejoras

- Implementar carga automática de decenas de ciudades.
- Utilizar WebDriver en modo headless.
- Incorporar registro de errores mediante logs.
- Automatizar la ejecución mediante cron o tareas programadas.
- Almacenar la información en una base de datos SQL.
- Generar visualizaciones de tendencias inmobiliarias.
- Integrar procesos de análisis predictivo mediante Machine Learning.
- Exportar resultados a formatos Excel o Parquet.

---

# Aplicaciones del Dataset

La información recopilada puede utilizarse para:

- Análisis del mercado inmobiliario.
- Estudios de variación de precios por región.
- Generación de indicadores económicos.
- Modelos predictivos de precios de vivienda.
- Visualización de tendencias históricas.
- Investigación académica.

---

# Autor

Proyecto desarrollado con fines educativos y de análisis de datos utilizando técnicas de automatización, web scraping y procesamiento de información con Python.

---

# Licencia

Este proyecto se proporciona con fines académicos y de investigación. Se recomienda respetar los términos de uso y políticas del sitio web del cual se obtienen los datos.
