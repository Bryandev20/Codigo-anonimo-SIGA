import pdfplumber
import re
import time
import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# ==========================================
# PARTE 1: EXTRAER DATOS DEL PDF
# ==========================================
print("1. Buscando el archivo PDF en la carpeta...")
carpeta_pdfs = r"C:\Users\INFOUNI\Downloads\sistema codigo anonimos\Actas_PDF"

if not os.path.exists(carpeta_pdfs):
    os.makedirs(carpeta_pdfs)
    print(f"📁 Se creó la carpeta '{carpeta_pdfs}'. Coloca tu PDF ahí y vuelve a ejecutar.")
    exit()

archivos_pdf = glob.glob(f"{carpeta_pdfs}/*.pdf")
if not archivos_pdf:
    print(f"❌ No se encontraron archivos PDF en '{carpeta_pdfs}'.")
    exit()

archivos_pdf.sort(key=os.path.getmtime, reverse=True)
archivo_pdf = archivos_pdf[0]
print(f"📄 Leyendo el archivo: {archivo_pdf}")

diccionario_codigos = {}
try:
    texto_completo = ""
    with pdfplumber.open(archivo_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"

    patron = r'\b(20\d{6}[A-Z])\b\s+(.*?)\s+(\d{5})\b'
    coincidencias = re.findall(patron, texto_completo)

    for match in coincidencias:
        cod_alumno = match[0].strip()
        cod_anonimo = match[2].strip()
        diccionario_codigos[cod_alumno] = cod_anonimo

    print(f"✅ ¡PDF leído! {len(diccionario_codigos)} alumnos encontrados.")
except Exception as e:
    print(f"❌ Error al leer el PDF: {e}")
    exit()

# ==========================================
# PARTE 2: CONECTARSE AL CHROME ABIERTO
# ==========================================
print("\n2. Conectándose a tu ventana de Chrome...")
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ ¡Conectado con éxito a tu Chrome!")
except Exception as e:
    print("\n❌ ERROR: No se pudo conectar a Chrome.")
    exit()

# ==========================================
# PARTE 3: LLENAR EL SIGA (ENTRANDO AL FRAME)
# ==========================================
print("\n=======================================================")
print("👉 Asegúrate de tener la tabla de alumnos visible en Chrome (pestaña normal, NO la de código fuente).")
print("=======================================================\n")
input("Cuando veas la tabla completa, presiona ENTER aquí...")

print("\n3. Entrando al marco de la tabla y colocando códigos...")

try:
    
    print("Cambiando al frame 'appFrame'...")
    driver.switch_to.frame("appFrame")
    
   
    tabla = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "table_car"))
    )
    
    filas = tabla.find_elements(By.XPATH, ".//tbody/tr")
    print(f"✅ ¡Tabla encontrada dentro del frame! Se detectaron {len(filas)} filas.")

    llenados_exitosos = 0
    no_encontrados = []

    for i, fila in enumerate(filas):
        try:
            celdas = fila.find_elements(By.TAG_NAME, "td")
            
            if len(celdas) >= 5:
                
                input_oculto = celdas[1].find_element(By.TAG_NAME, "input")
                codigo_alumno_siga = input_oculto.get_attribute("value").strip()
                
               
                caja_texto = celdas[4].find_element(By.TAG_NAME, "input")
                
                if codigo_alumno_siga in diccionario_codigos:
                    codigo_anonimo = diccionario_codigos[codigo_alumno_siga]
                    
                    caja_texto.clear()
                    caja_texto.send_keys(codigo_anonimo)
                    caja_texto.send_keys(Keys.TAB) 
                    
                    llenados_exitosos += 1
                    print(f"Fila {i+1}: {codigo_alumno_siga} -> {codigo_anonimo} ✅")
                    time.sleep(0.1) 
                else:
                    print(f"⚠️ Fila {i+1}: Alumno {codigo_alumno_siga} NO está en el PDF.")
                    no_encontrados.append(codigo_alumno_siga)
        except Exception as e:
            continue

    print(f"\n✅ ¡PROCESO TERMINADO! Se llenaron {llenados_exitosos} códigos automáticamente.")
    if no_encontrados:
        print(f"⚠️ Alumnos en SIGA no encontrados en el PDF: {no_encontrados}")
    
    print("\nRevisa la pantalla, dale a 'Guardar Código' y cierra Chrome cuando termines.")

except Exception as e:
    print(f"\n❌ ERROR GRAVE: {type(e).__name__} - {e}")
    print("Asegúrate de que la tabla esté visible en la pestaña activa de Chrome.")