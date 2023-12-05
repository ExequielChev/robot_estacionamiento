import os
import re
import pandas as pd
from pathlib import Path
from PyPDF2 import PdfReader

# Variables globales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
patron_compromiso = r'Documento Respaldatorio: AVS-(16-0-\d+)'
patron_cuenta = r'(\d+) '

Nombre_excel =  "Comprobantesestacionamiento.xlsx"

def procesar_compromisos():
    carpeta_compromisos = os.path.join(BASE_DIR, 'comprobantes')
    carpeta_path = Path(carpeta_compromisos)
    archivos_pdf = carpeta_path.glob("*.pdf")

    # Inicializar listas vacías fuera del bucle
    tipo_compr_total = []
    num_compr_total = []
    num_cuenta_total = []

    for archivo_pdf in archivos_pdf:
        # Reiniciar listas para cada archivo PDF
        tipo_compr = []
        num_compr = []
        num_cuenta = []

        reader = PdfReader(archivo_pdf)
        page = reader.pages[0]
        text = page.extract_text()

        lineas = text.split('\n')

        comprobante = None
        tipo_c = None
        num_c = None
        cuenta = None

        for linea in lineas:
            match_compromiso = re.search(patron_compromiso, linea)
            if match_compromiso:
                comprobante = match_compromiso.group(1)
                match_divisor = re.search(r'-0-', comprobante, re.IGNORECASE)
                if match_divisor:
                    partes = re.split(r'-0-', comprobante, flags=re.IGNORECASE)
                    tipo_c = partes[0]
                    num_c = partes[1]
                    tipo_compr.append(tipo_c)
                    num_compr.append(num_c)
                else:
                    num_c = comprobante

            match_cuenta = re.search(patron_cuenta, linea)
            if match_cuenta:
                cuenta = match_cuenta.group(1)

        if cuenta:
            num_cuenta.extend([cuenta])

        # Extender listas globales con listas locales
        tipo_compr_total.extend(tipo_compr)
        num_compr_total.extend(num_compr)
        num_cuenta_total.extend(num_cuenta)

        # Crear DataFrame para el archivo PDF actual
        data = {
            "Tipo_comprobante": tipo_compr_total,
            "Numero_comprobante": num_compr_total,
            "Numero_cuenta": num_cuenta_total
        }

    df_compr = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo Excel
    nombre_archivo_excel = os.path.join(carpeta_compromisos, Nombre_excel) # Se establece la ruta en donde se almacenará el archivo
    df_compr.to_excel(nombre_archivo_excel, sheet_name="Compromisos", index=False) # Convierte el DataFrame en un excel, se le indica dónde debe guardarse, el nómbre de la hoja de cálculo y se excluye el índice de cada dato almacenado

    print(f"Datos guardados en el archivo Excel: {nombre_archivo_excel}") # Se verifica que el archivo se esté creando con un "print()" que da el mensaje confirmando la acción


procesar_compromisos() # Se llama a la función para ser ejecutada