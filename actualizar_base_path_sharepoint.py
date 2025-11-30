"""
Script para actualizar SHAREPOINT_BASE_PATH con "Shared Documents"
"""
import os
from pathlib import Path
from dotenv import load_dotenv, set_key

def actualizar_base_path():
    """Actualiza SHAREPOINT_BASE_PATH para incluir 'Shared Documents'"""
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("[ERROR] Archivo .env no encontrado")
        return
    
    # Cargar variables actuales
    load_dotenv()
    base_path_actual = os.getenv("SHAREPOINT_BASE_PATH", "")
    
    print("=" * 80)
    print("ACTUALIZACION DE SHAREPOINT_BASE_PATH")
    print("=" * 80)
    print(f"\n[CONFIGURACION ACTUAL]")
    print(f"  SHAREPOINT_BASE_PATH: {base_path_actual}")
    
    # Verificar si ya incluye "Shared Documents"
    if "Shared Documents" in base_path_actual:
        print(f"\n[INFO] El base_path ya incluye 'Shared Documents'")
        print(f"  No se requiere actualización")
        return
    
    # Construir nuevo base_path
    if base_path_actual.startswith("Documentos/"):
        # Reemplazar "Documentos" por "Shared Documents"
        nuevo_base_path = base_path_actual.replace("Documentos/", "Shared Documents/", 1)
    elif base_path_actual.startswith("Documentos "):
        nuevo_base_path = base_path_actual.replace("Documentos ", "Shared Documents/", 1)
    else:
        # Agregar "Shared Documents/" al inicio
        nuevo_base_path = f"Shared Documents/{base_path_actual.lstrip('/')}"
    
    print(f"\n[NUEVA CONFIGURACION]")
    print(f"  SHAREPOINT_BASE_PATH: {nuevo_base_path}")
    
    # Actualizar .env
    try:
        set_key(str(env_file), "SHAREPOINT_BASE_PATH", nuevo_base_path)
        print(f"\n[OK] Archivo .env actualizado exitosamente")
        print(f"\n[IMPORTANTE] Reinicia el script o recarga las variables de entorno")
        print(f"  para que los cambios surtan efecto")
    except Exception as e:
        print(f"\n[ERROR] Error al actualizar .env: {e}")
        print(f"\n[MANUAL] Actualiza manualmente el archivo .env:")
        print(f"  SHAREPOINT_BASE_PATH={nuevo_base_path}")
    
    print("\n" + "=" * 80)
    print("RUTA CONSTRUIDA CON LA NUEVA CONFIGURACION")
    print("=" * 80)
    print(f"\nLa ruta ahora será:")
    print(f"  /sites/OPERACIONES/Shared Documents/PROYECTOS/Año 2024/...")
    print("=" * 80)

if __name__ == "__main__":
    actualizar_base_path()

