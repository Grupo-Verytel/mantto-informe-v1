"""
Script de prueba para diagnosticar la extracción de observaciones desde SharePoint
"""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from src.ia.extractor_observaciones import get_extractor_observaciones
import json

def test_extractor_observaciones():
    """Prueba la extracción de texto desde SharePoint y generación de observaciones"""
    print("=" * 80)
    print("PRUEBA DE EXTRACCION DE OBSERVACIONES DESDE SHAREPOINT")
    print("=" * 80)
    
    # Cargar configuración
    print("\n[1] Cargando configuración...")
    try:
        import config
        from dotenv import load_dotenv
        load_dotenv()
        
        sharepoint_site_url = getattr(config, 'SHAREPOINT_SITE_URL', None) or os.getenv("SHAREPOINT_SITE_URL")
        sharepoint_client_id = getattr(config, 'SHAREPOINT_CLIENT_ID', None) or os.getenv("SHAREPOINT_CLIENT_ID")
        sharepoint_client_secret = getattr(config, 'SHAREPOINT_CLIENT_SECRET', None) or os.getenv("SHAREPOINT_CLIENT_SECRET")
        sharepoint_base_path = getattr(config, 'SHAREPOINT_BASE_PATH', None) or os.getenv("SHAREPOINT_BASE_PATH")
        openai_api_key = getattr(config, 'OPENAI_API_KEY', None) or os.getenv("OPENAI_API_KEY")
        
        print(f"   [INFO] SharePoint Site URL: {sharepoint_site_url}")
        print(f"   [INFO] SharePoint Client ID: {'***' if sharepoint_client_id else 'NO CONFIGURADO'}")
        print(f"   [INFO] SharePoint Client Secret: {'***' if sharepoint_client_secret else 'NO CONFIGURADO'}")
        print(f"   [INFO] SharePoint Base Path: {sharepoint_base_path}")
        print(f"   [INFO] OpenAI API Key: {'***' if openai_api_key else 'NO CONFIGURADO'}")
        
        if not sharepoint_site_url:
            print("   [ERROR] SHAREPOINT_SITE_URL no está configurado")
            return
        
        if not sharepoint_client_id or not sharepoint_client_secret:
            print("   [ERROR] SHAREPOINT_CLIENT_ID o SHAREPOINT_CLIENT_SECRET no están configurados")
            return
        
    except Exception as e:
        print(f"   [ERROR] Error al cargar configuración: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Crear extractor
    print("\n[2] Creando extractor de observaciones...")
    try:
        extractor = get_extractor_observaciones(
            sharepoint_site_url=sharepoint_site_url,
            sharepoint_client_id=sharepoint_client_id,
            sharepoint_client_secret=sharepoint_client_secret,
            sharepoint_base_path=sharepoint_base_path
        )
        print("   [OK] Extractor creado")
        print(f"   [INFO] Cliente OpenAI disponible: {bool(extractor.client)}")
    except Exception as e:
        print(f"   [ERROR] Error al crear extractor: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Cargar obligaciones de prueba
    print("\n[3] Cargando obligaciones de prueba...")
    try:
        obligaciones_path = Path("data/fuentes/obligaciones_9_2025.json")
        if not obligaciones_path.exists():
            print(f"   [ERROR] Archivo no encontrado: {obligaciones_path}")
            return
        
        with open(obligaciones_path, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        obligaciones = datos.get('obligaciones_generales', [])
        print(f"   [OK] {len(obligaciones)} obligaciones cargadas")
        
        if len(obligaciones) == 0:
            print("   [WARNING] No hay obligaciones para probar")
            return
        
    except Exception as e:
        print(f"   [ERROR] Error al cargar obligaciones: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Probar cada obligación
    print("\n[4] Procesando obligaciones...")
    print("=" * 80)
    
    for i, obligacion in enumerate(obligaciones[:2], 1):  # Probar solo las primeras 2
        print(f"\n[4.{i}] Procesando obligación {obligacion.get('item', 'N/A')}...")
        print(f"   Obligación: {obligacion.get('obligacion', '')[:100]}...")
        print(f"   Anexo: {obligacion.get('anexo', 'N/A')}")
        
        try:
            obligacion_procesada = extractor.procesar_obligacion(obligacion)
            
            observacion = obligacion_procesada.get('observaciones', '')
            generada_llm = obligacion_procesada.get('observacion_generada_llm', False)
            
            print(f"\n   [RESULTADO]")
            print(f"   - Observación generada: {len(observacion)} caracteres")
            print(f"   - Generada con LLM: {generada_llm}")
            if observacion:
                print(f"   - Primeros 200 caracteres: {observacion[:200]}...")
            else:
                print(f"   - [WARNING] Observación vacía")
            
        except Exception as e:
            print(f"   [ERROR] Error al procesar obligación: {e}")
            import traceback
            traceback.print_exc()
    
    # Limpiar archivos temporales
    print("\n[5] Limpiando archivos temporales...")
    try:
        extractor.limpiar_archivos_temporales()
        print("   [OK] Archivos temporales limpiados")
    except Exception as e:
        print(f"   [WARNING] Error al limpiar archivos temporales: {e}")
    
    print("\n" + "=" * 80)
    print("[OK] PRUEBA COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    test_extractor_observaciones()

