"""
Script para verificar y ajustar la ruta de SharePoint
"""
import os
from pathlib import Path
from urllib.parse import quote, unquote

def mostrar_rutas_posibles():
    """Muestra diferentes variaciones de la ruta para verificar"""
    
    print("=" * 80)
    print("VERIFICACION DE RUTA DE SHAREPOINT")
    print("=" * 80)
    
    # Ruta base
    site_url = "https://verytelcsp.sharepoint.com/sites/OPERACIONES"
    base_path = "Shared Documents/PROYECTOS/Año 2024/2024-1809 MANTTO BOGOTA ETB/8.INFORMES/INFORME MENSUAL"
    carpeta_periodo = "11. 01SEP - 30SEP"
    subcarpeta = "01 OBLIGACIONES GENERALES"
    carpeta_obligacion = "OBLIGACIÓN 1,7,8,9,10,11,13,14 y 15"
    archivo = "Oficio Obli SEPTIEMBRE 2025.pdf"
    
    print("\n[INFORMACION DEL ARCHIVO]")
    print(f"  Carpeta periodo: {carpeta_periodo}")
    print(f"  Subcarpeta: {subcarpeta}")
    print(f"  Carpeta obligacion: {carpeta_obligacion}")
    print(f"  Archivo: {archivo}")
    
    print("\n[RUTA ACTUAL CONSTRUIDA]")
    ruta_actual = f"/sites/OPERACIONES/{base_path}/{carpeta_periodo}/{subcarpeta}/{carpeta_obligacion}/{archivo}"
    print(f"  {ruta_actual}")
    
    print("\n[VARIACIONES POSIBLES A VERIFICAR]")
    
    # Variación 1: Sin espacios después de "11."
    variacion1 = f"/sites/OPERACIONES/{base_path}/11.01SEP - 30SEP/{subcarpeta}/{carpeta_obligacion}/{archivo}"
    print(f"\n1. Sin espacio después de '11.':")
    print(f"   {variacion1}")
    
    # Variación 2: Con guión bajo en lugar de espacios
    variacion2 = f"/sites/OPERACIONES/{base_path}/11._01SEP_-_30SEP/{subcarpeta.replace(' ', '_')}/{carpeta_obligacion.replace(' ', '_')}/{archivo.replace(' ', '_')}"
    print(f"\n2. Con guiones bajos (menos probable):")
    print(f"   {variacion2}")
    
    # Variación 3: Sin el prefijo "11."
    variacion3 = f"/sites/OPERACIONES/{base_path}/01SEP - 30SEP/{subcarpeta}/{carpeta_obligacion}/{archivo}"
    print(f"\n3. Sin prefijo '11.':")
    print(f"   {variacion3}")
    
    # Variación 4: Con diferentes espacios
    variacion4 = f"/sites/OPERACIONES/{base_path}/11. 01SEP-30SEP/{subcarpeta}/{carpeta_obligacion}/{archivo}"
    print(f"\n4. Sin espacios en '01SEP - 30SEP':")
    print(f"   {variacion4}")
    
    # Variación 5: Nombre de archivo diferente
    variacion5_archivo = "Oficio Obli SEPTIEMBRE 2025.pdf"
    variacion5 = f"/sites/OPERACIONES/{base_path}/{carpeta_periodo}/{subcarpeta}/{carpeta_obligacion}/{variacion5_archivo}"
    print(f"\n5. Verificar nombre exacto del archivo:")
    print(f"   {variacion5}")
    
    print("\n" + "=" * 80)
    print("INSTRUCCIONES PARA VERIFICAR")
    print("=" * 80)
    print("\n1. Abre SharePoint en tu navegador")
    print("2. Navega hasta el archivo manualmente")
    print("3. Haz clic derecho en el archivo > 'Detalles' o 'Propiedades'")
    print("4. Copia la ruta completa que aparece")
    print("5. O usa 'Copiar ruta' si está disponible")
    print("\nTambién puedes:")
    print("- Abrir el archivo en SharePoint")
    print("- Copiar la URL completa de la barra de direcciones")
    print("- La ruta estará en la URL después de '/sites/OPERACIONES/'")
    print("\n" + "=" * 80)
    
    # Mostrar cómo construir URL de prueba
    print("\n[URLs DE PRUEBA PARA VERIFICAR]")
    print("\nPara probar cada variación, usa estas URLs (reemplaza [RUTA] con cada variación):")
    print(f"\nhttps://verytelcsp.sharepoint.com/sites/OPERACIONES/_api/web/GetFileByServerRelativeUrl('[RUTA_CODIFICADA]')/$value")
    print("\nDonde [RUTA_CODIFICADA] es la ruta codificada con quote()")
    
    print("\n[EJEMPLO CON RUTA ACTUAL]")
    ruta_codificada = quote(ruta_actual, safe='')
    url_prueba = f"{site_url}/_api/web/GetFileByServerRelativeUrl('{ruta_codificada}')/$value"
    print(f"  {url_prueba}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    mostrar_rutas_posibles()

