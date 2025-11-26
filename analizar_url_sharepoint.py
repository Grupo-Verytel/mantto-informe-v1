"""
Script para analizar la URL real de SharePoint y compararla con la construida
"""
from urllib.parse import unquote, quote

# URL proporcionada por el usuario
url_real = "https://verytelcsp.sharepoint.com/sites/OPERACIONES/Shared%20Documents/PROYECTOS/A%C3%B1o%202024/2024-1809%20MANTTO%20BOGOTA%20ETB/8.%20INFORMES/INFORME%20MENSUAL/11.%2001SEP%20-%2030SEP/01%20OBLIGACIONES%20GENERALES/OBLIGACION%201,7,8,9,10,11,13,14%20y%2015/Oficio%20Obli%20SEPTIEMBRE%202025.pdf"

print("=" * 80)
print("ANALISIS DE URL REAL DE SHAREPOINT")
print("=" * 80)

# Decodificar URL
ruta_decodificada = unquote(url_real)
print("\n[URL DECODIFICADA]")
print(f"  {ruta_decodificada}")

# Extraer la ruta relativa del servidor
# La ruta relativa comienza después de "/sites/OPERACIONES/"
partes = ruta_decodificada.split("/sites/OPERACIONES/")
if len(partes) > 1:
    ruta_relativa_real = "/sites/OPERACIONES/" + partes[1]
    print("\n[RUTA RELATIVA DEL SERVIDOR (REAL)]")
    print(f"  {ruta_relativa_real}")
    
    # Dividir en partes para análisis
    partes_ruta = ruta_relativa_real.replace("/sites/OPERACIONES/", "").split("/")
    print("\n[PARTES DE LA RUTA]")
    for i, parte in enumerate(partes_ruta, 1):
        print(f"  {i}. {parte}")

# Ruta que estábamos construyendo
ruta_construida = "/sites/OPERACIONES/Shared Documents/PROYECTOS/Año 2024/2024-1809 MANTTO BOGOTA ETB/8.INFORMES/INFORME MENSUAL/11. 01SEP - 30SEP/01 OBLIGACIONES GENERALES/OBLIGACIÓN 1,7,8,9,10,11,13,14 y 15/Oficio Obli SEPTIEMBRE 2025.pdf"

print("\n" + "=" * 80)
print("COMPARACION")
print("=" * 80)
print("\n[RUTA CONSTRUIDA (INCORRECTA)]")
print(f"  {ruta_construida}")

print("\n[RUTA REAL (CORRECTA)]")
print(f"  {ruta_relativa_real}")

print("\n[DIFERENCIAS ENCONTRADAS]")
print("  1. '8.INFORMES' vs '8. INFORMES' (falta espacio después del punto)")
print("  2. 'OBLIGACIÓN' vs 'OBLIGACION' (falta la tilde en la 'Ó')")

print("\n" + "=" * 80)
print("CORRECCIONES NECESARIAS")
print("=" * 80)
print("\n1. En SHAREPOINT_BASE_PATH:")
print("   Cambiar: '8.INFORMES'")
print("   Por:     '8. INFORMES'")
print("\n2. En el JSON de obligaciones:")
print("   Cambiar: 'OBLIGACIÓN'")
print("   Por:     'OBLIGACION' (sin tilde)")

print("\n" + "=" * 80)

