"""
Script para corregir las rutas de SharePoint
"""
import os
from pathlib import Path
from dotenv import load_dotenv, set_key

def corregir_base_path():
    """Corrige el SHAREPOINT_BASE_PATH"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("[ERROR] Archivo .env no encontrado")
        return
    
    load_dotenv()
    base_path_actual = os.getenv("SHAREPOINT_BASE_PATH", "")
    
    print("=" * 80)
    print("CORRECCION DE SHAREPOINT_BASE_PATH")
    print("=" * 80)
    print(f"\n[CONFIGURACION ACTUAL]")
    print(f"  {base_path_actual}")
    
    # Corregir: "8.INFORMES" -> "8. INFORMES"
    nuevo_base_path = base_path_actual.replace("8.INFORMES", "8. INFORMES")
    
    if nuevo_base_path != base_path_actual:
        print(f"\n[NUEVA CONFIGURACION]")
        print(f"  {nuevo_base_path}")
        
        try:
            set_key(str(env_file), "SHAREPOINT_BASE_PATH", nuevo_base_path)
            print(f"\n[OK] Archivo .env actualizado exitosamente")
        except Exception as e:
            print(f"\n[ERROR] Error al actualizar .env: {e}")
            print(f"\n[MANUAL] Actualiza manualmente el archivo .env:")
            print(f"  SHAREPOINT_BASE_PATH={nuevo_base_path}")
    else:
        print(f"\n[INFO] El base_path ya está correcto")
    
    print("=" * 80)

if __name__ == "__main__":
    corregir_base_path()

