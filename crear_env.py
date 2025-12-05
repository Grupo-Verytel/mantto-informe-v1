"""
Script para crear el archivo .env desde la plantilla
"""
from pathlib import Path
import shutil

def crear_archivo_env():
    """Crea el archivo .env desde .env.example si no existe"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("[INFO] El archivo .env ya existe.")
        respuesta = input("¿Deseas sobrescribirlo? (s/n): ").lower()
        if respuesta != 's':
            print("[INFO] Operación cancelada.")
            return
    
    if not env_example.exists():
        print("[ERROR] No se encontró el archivo .env.example")
        return
    
    # Copiar plantilla
    shutil.copy(env_example, env_file)
    print(f"[OK] Archivo .env creado desde .env.example")
    print("\n[IMPORTANTE] Edita el archivo .env y configura tus credenciales:")
    print("  1. OPENAI_API_KEY - Tu API key de OpenAI")
    print("  2. SHAREPOINT_SITE_URL - URL de tu sitio de SharePoint")
    print("  3. SHAREPOINT_USERNAME - Usuario de SharePoint (opcional)")
    print("  4. SHAREPOINT_PASSWORD - Contraseña de SharePoint (opcional)")
    print("  5. SHAREPOINT_CLIENT_ID - Client ID para App Registration (recomendado)")
    print("  6. SHAREPOINT_CLIENT_SECRET - Client Secret para App Registration (recomendado)")
    print(f"\nArchivo creado en: {env_file.absolute()}")

if __name__ == "__main__":
    crear_archivo_env()

