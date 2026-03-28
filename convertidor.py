import os
import zipfile
from google.colab import files

# 1. BOTÓN PARA SUBIR EL ZIP
print("📦 SELECCIONA TU ARCHIVO .ZIP (el que contiene la carpeta Batch_Export...)")
subida = files.upload()

if not subida:
    print("❌ No seleccionaste ningún archivo.")
else:
    nombre_zip_subido = list(subida.keys())[0]
    folder_extraccion = 'mis_notas_temp'

    # 2. DESCOMPRIMIR
    with zipfile.ZipFile(nombre_zip_subido, 'r') as zip_ref:
        zip_ref.extractall(folder_extraccion)
    print(f"✅ Carpeta extraída.")

    # 3. CONVERSIÓN RECURSIVA (Busca en carpetas y subcarpetas)
    conteo = 0
    for raiz, directorios, archivos in os.walk(folder_extraccion):
        for nombre in archivos:
            if nombre.lower().endswith(".txt"):
                ruta_vieja = os.path.join(raiz, nombre)
                # Separamos el nombre de la extensión y ponemos .md
                nombre_base = os.path.splitext(ruta_vieja)[0]
                ruta_nueva = nombre_base + ".md"
                
                os.rename(ruta_vieja, ruta_nueva)
                conteo += 1

    print(f"📝 Se convirtieron {conteo} archivos a formato Markdown (.md).")

    # 4. VOLVER A COMPRIMIR Y DESCARGAR
    archivo_final = "NOTAS_LISTAS_OBSIDIAN.zip"
    # El comando !zip mantiene la estructura de carpetas original
    !zip -r {archivo_final} {folder_extraccion}
    
    print("🚀 Descarga automática iniciando...")
    files.download(archivo_final)
