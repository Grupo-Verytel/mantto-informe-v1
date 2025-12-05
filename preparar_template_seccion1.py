"""
Script para copiar el template de referencia y prepararlo con variables Jinja2
"""
from docx import Document
from pathlib import Path
import shutil

# Copiar template de referencia
origen = Path("data/segmentos/Seccion 1.docx")
destino = Path("templates/seccion_1_info_general.docx")

if origen.exists():
    # Hacer backup del template actual si existe
    if destino.exists():
        backup = Path("templates/seccion_1_info_general_backup.docx")
        shutil.copy(destino, backup)
        print(f"[INFO] Backup creado: {backup}")
    
    # Copiar template de referencia
    shutil.copy(origen, destino)
    print(f"[OK] Template copiado de referencia a: {destino}")
    print("\n[INSTRUCCIONES]")
    print("1. Abre el archivo templates/seccion_1_info_general.docx en Word")
    print("2. Reemplaza los valores dinámicos con variables Jinja2:")
    print("   - Texto introductorio: {{ texto_intro }}")
    print("   - Valores en Tabla 1: {{ tabla_1_info_general.campo }}")
    print("   - Filas de tablas: Usa {% for item in lista %} ... {% endfor %}")
    print("3. Guarda el archivo")
    print("\n[NOTA] Este proceso requiere edición manual en Word para")
    print("agregar las variables Jinja2 correctamente en las celdas de las tablas.")
else:
    print(f"[ERROR] No se encontró el archivo de referencia: {origen}")

