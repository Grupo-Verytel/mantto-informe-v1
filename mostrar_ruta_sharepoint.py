"""
Script para mostrar la ruta construida de SharePoint
"""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from src.ia.extractor_observaciones import get_extractor_observaciones

def mostrar_ruta_construida():
    """Muestra cómo se construye la ruta de SharePoint"""
    print("=" * 80)
    print("CONSTRUCCION DE RUTA DE SHAREPOINT")
    print("=" * 80)
    
    # Cargar configuración
    try:
        import config
        from dotenv import load_dotenv
        load_dotenv()
        
        sharepoint_site_url = getattr(config, 'SHAREPOINT_SITE_URL', None) or os.getenv("SHAREPOINT_SITE_URL")
        sharepoint_client_id = getattr(config, 'SHAREPOINT_CLIENT_ID', None) or os.getenv("SHAREPOINT_CLIENT_ID")
        sharepoint_client_secret = getattr(config, 'SHAREPOINT_CLIENT_SECRET', None) or os.getenv("SHAREPOINT_CLIENT_SECRET")
        sharepoint_base_path = getattr(config, 'SHAREPOINT_BASE_PATH', None) or os.getenv("SHAREPOINT_BASE_PATH")
        
        print("\n[CONFIGURACION ACTUAL]")
        print(f"  Site URL: {sharepoint_site_url}")
        print(f"  Base Path: {sharepoint_base_path}")
        print(f"  Client ID: {'***' if sharepoint_client_id else 'NO CONFIGURADO'}")
        print(f"  Client Secret: {'***' if sharepoint_client_secret else 'NO CONFIGURADO'}")
        
        # Crear extractor
        extractor = get_extractor_observaciones(
            sharepoint_site_url=sharepoint_site_url,
            sharepoint_client_id=sharepoint_client_id,
            sharepoint_client_secret=sharepoint_client_secret,
            sharepoint_base_path=sharepoint_base_path
        )
        
        # Ejemplo de ruta de anexo (con prefijo "11. ")
        ruta_anexo_ejemplo = "11. 01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 1,7,8,9,10,11,13,14 y 15/ Oficio Obli SEPTIEMBRE 2025.pdf"
        
        print("\n[EJEMPLO DE RUTA DE ANEXO]")
        print(f"  Ruta original: {ruta_anexo_ejemplo}")
        
        # Resolver ruta
        ruta_resuelta = extractor._resolver_ruta_anexo(ruta_anexo_ejemplo)
        
        print("\n[RUTA RESUELTA]")
        print(f"  Ruta completa: {ruta_resuelta}")
        
        # Mostrar desglose de construcción
        print("\n[DESGLOSE DE CONSTRUCCION]")
        from urllib.parse import urlparse
        
        sitio_parsed = urlparse(sharepoint_site_url)
        sitio_path_parts = [p for p in sitio_parsed.path.split('/') if p]
        
        print(f"  1. Site URL parseado:")
        print(f"     - Path parts del sitio: {sitio_path_parts}")
        
        if sharepoint_base_path:
            base_path_clean = sharepoint_base_path.strip('/').strip()
            base_path_parts = [p for p in base_path_clean.split('/') if p]
            print(f"  2. Base Path dividido:")
            print(f"     - Partes: {base_path_parts}")
        
        ruta_normalizada = ruta_anexo_ejemplo.replace(" / ", "/").replace(" /", "/").replace("/ ", "/")
        print(f"  3. Ruta de anexo normalizada:")
        print(f"     - Ruta: {ruta_normalizada}")
        
        # Construir ruta completa
        path_parts = sitio_path_parts.copy()
        if sharepoint_base_path:
            base_path_clean = sharepoint_base_path.strip('/').strip()
            if base_path_clean:
                base_path_parts = [p for p in base_path_clean.split('/') if p]
                path_parts.extend(base_path_parts)
        
        ruta_archivo_clean = ruta_normalizada.lstrip('/')
        server_relative_url = '/' + '/'.join(path_parts) + '/' + ruta_archivo_clean
        
        print(f"\n  4. Ruta relativa del servidor construida:")
        print(f"     - Server Relative URL: {server_relative_url}")
        
        # Mostrar URL completa de API REST
        from urllib.parse import quote
        api_url = f"{sharepoint_site_url.rstrip('/')}/_api/web/GetFileByServerRelativeUrl('{quote(server_relative_url, safe='')}')/$value"
        
        print(f"\n  5. URL de API REST para descarga:")
        print(f"     - API URL: {api_url}")
        
        print("\n" + "=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print(f"Ruta relativa del servidor: {server_relative_url}")
        print(f"\nEsta es la ruta que se usa para acceder al archivo en SharePoint.")
        print(f"Si obtienes error 403, verifica:")
        print(f"  1. Que esta ruta sea correcta en tu SharePoint")
        print(f"  2. Que la App Registration tenga permisos en esta ubicación")
        print(f"  3. Que el archivo exista en esta ruta")
        print("=" * 80)
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    mostrar_ruta_construida()

