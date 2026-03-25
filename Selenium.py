# ==============================
# IMPORTAR LIBRERÍAS
# ==============================
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import os


# ==============================
# FUNCIÓN PARA EXTRAER DATOS
# ==============================
def extraer_ciudad(url, nombre_ciudad):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    div = soup.find("div", attrs={"data-chart": True})

    if div is None:
        print(f"No se encontró info para {nombre_ciudad}")
        driver.quit()
        return None

    raw_data = div["data-chart"]
    data = json.loads(raw_data)

    stats = data["statistics"]

    df = pd.DataFrame(stats)
    df.columns = ["fecha", "precio"]

    df["fecha"] = pd.to_datetime(df["fecha"])
    df["ciudad"] = nombre_ciudad

    driver.quit()
    return df


# ==============================
# 🔥 SOLO EDITAS ESTO
# ==============================

ciudades = [
    {"nombre": "Guadalajara", "url": "https://www.vivanuncios.com.mx/s-inmuebles/guadalajara/v1c30l14822p1"},
    {"nombre": "LaPaz", "url": "https://www.vivanuncios.com.mx/s-inmuebles/la-paz-bcs/v1c30l10017p1"},
    {"nombre": "Mexicali", "url": "https://www.vivanuncios.com.mx/s-inmuebles/mexicali/v1c30l10012p1"},
]

# 👉 aquí solo agregas más ciudades siguiendo el mismo formato


# ==============================
# EXTRAER TODO AUTOMÁTICAMENTE
# ==============================

dfs = []

for ciudad in ciudades:
    print(f"Extrayendo {ciudad['nombre']}...")
    df = extraer_ciudad(ciudad["url"], ciudad["nombre"])

    if df is not None:
        dfs.append(df)


df_nuevo = pd.concat(dfs)


# ==============================
# GUARDADO ACUMULATIVO
# ==============================

archivo = "dataset_vivienda_mexico.csv"

if os.path.exists(archivo):
    df_existente = pd.read_csv(archivo)

    # convertir fechas por si acaso
    df_existente["fecha"] = pd.to_datetime(df_existente["fecha"])

    # unir datasets
    df_total = pd.concat([df_existente, df_nuevo])

    # eliminar duplicados
    df_total = df_total.drop_duplicates(subset=["fecha", "ciudad"])

else:
    df_total = df_nuevo


df_total.to_csv(archivo, index=False)

print("Dataset actualizado y guardado ✅")