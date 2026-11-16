# ==============================
# IMPORTAR LIBRERÍAS
# ==============================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import pandas as pd
import os


# ==============================
# FUNCIÓN PARA EXTRAER DATOS
# ==============================
def extraer_ciudad(driver, url, nombre_ciudad):
    driver.get(url)

    # Espera hasta 15 s a que aparezca el div con data-chart
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-chart]"))
        )
    except Exception:
        print(f"No se encontró info para {nombre_ciudad}")
        return None

    soup = BeautifulSoup(driver.page_source, "html.parser")
    div = soup.find("div", attrs={"data-chart": True})

    if div is None:
        print(f"No se encontró info para {nombre_ciudad}")
        return None

    data = json.loads(div["data-chart"])

    # Solo la serie de la región (ej. Nayarit); se ignora data["parent"] (México)
    stats = data["statistics"]

    df = pd.DataFrame(stats).rename(columns={"label": "fecha", "value": "precio"})
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["ciudad"] = nombre_ciudad

    return df


# ==============================
# CIUDADES A EXTRAER (cambia solo nombre y URL)
# ==============================
ciudades = [
    {"nombre": "Oaxaca", "url": "https://www.vivanuncios.com.mx/s-inmuebles/oaxaca/v1c30l1019p1"},
    # Agrega más ciudades con el mismo formato:
    # {"nombre": "Guadalajara", "url": "https://..."},
]


# ==============================
# EXTRAER TODO AUTOMÁTICAMENTE
# ==============================
dfs = []
driver = webdriver.Chrome()  # un solo navegador para todas las ciudades

try:
    for ciudad in ciudades:
        print(f"Extrayendo {ciudad['nombre']}...")
        df = extraer_ciudad(driver, ciudad["url"], ciudad["nombre"])

        if df is not None:
            dfs.append(df)
finally:
    driver.quit()


# ==============================
# GUARDADO ACUMULATIVO
# ==============================
if not dfs:
    print("No se extrajo ningún dato. No se modificó el archivo.")
else:
    df_nuevo = pd.concat(dfs, ignore_index=True)

    archivo = "dataset_vivienda_mexico.csv"

    if os.path.exists(archivo):
        df_existente = pd.read_csv(archivo)
        df_existente["fecha"] = pd.to_datetime(df_existente["fecha"])

        df_total = pd.concat([df_existente, df_nuevo], ignore_index=True)
        df_total = df_total.drop_duplicates(subset=["fecha", "ciudad"], keep="last")
    else:
        df_total = df_nuevo

    df_total = df_total.sort_values(["ciudad", "fecha"])
    print(df_total.head())
    print("Filas a guardar:", len(df_total))
    print("Carpeta de trabajo:", os.getcwd())
    df_total.to_csv(archivo, index=False)

    print("Dataset actualizado y guardado ")
