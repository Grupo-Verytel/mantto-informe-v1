"""
Script de prueba completo para la Sección 1 con LLM y SharePoint
"""
from pathlib import Path
from src.generadores.seccion_1_info_general import GeneradorSeccion1
import os

def test_configuracion():
    """Verifica que las variables de entorno estén configuradas"""
    print("="*70)
    print("VERIFICACIÓN DE CONFIGURACIÓN")
    print("="*70)
    
    # Cargar .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("[WARNING] python-dotenv no está instalado")
    
    # Verificar OpenAI
    openai_key = os.getenv("OPENAI_API_KEY", "")
    print(f"\nOpenAI API Key: {'[OK] Configurada' if openai_key and openai_key != 'tu-api-key-openai-aqui' else '[FALTA] No configurada'}")
    
    # Verificar SharePoint
    sharepoint_url = os.getenv("SHAREPOINT_SITE_URL", "")
    sharepoint_client_id = os.getenv("SHAREPOINT_CLIENT_ID", "")
    sharepoint_client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
    
    print(f"SharePoint Site URL: {'[OK] Configurada' if sharepoint_url and sharepoint_url != 'https://empresa.sharepoint.com/sites/Sitio' else '[FALTA] No configurada'}")
    print(f"SharePoint Client ID: {'[OK] Configurada' if sharepoint_client_id and sharepoint_client_id != 'tu-client-id-aqui' else '[FALTA] No configurada'}")
    print(f"SharePoint Client Secret: {'[OK] Configurada' if sharepoint_client_secret and sharepoint_client_secret != 'tu-client-secret-aqui' else '[FALTA] No configurada'}")
    
    return all([
        openai_key and openai_key != 'tu-api-key-openai-aqui',
        sharepoint_url and sharepoint_url != 'https://empresa.sharepoint.com/sites/Sitio',
        sharepoint_client_id and sharepoint_client_id != 'tu-client-id-aqui',
        sharepoint_client_secret and sharepoint_client_secret != 'tu-client-secret-aqui'
    ])

def test_generacion_seccion1():
    """Prueba la generación completa de la Sección 1"""
    print("\n" + "="*70)
    print("PRUEBA DE GENERACIÓN - SECCIÓN 1")
    print("="*70)
    
    try:
        # Crear generador
        print("\n[INFO] Inicializando generador...")
        gen = GeneradorSeccion1(anio=2025, mes=9, usar_llm_observaciones=True)
        
        # Cargar datos
        print("[INFO] Cargando datos...")
        gen.cargar_datos()
        
        print(f"\n[INFO] Datos cargados:")
        print(f"  - Comunicados emitidos: {len(gen.comunicados_emitidos)}")
        print(f"  - Comunicados recibidos: {len(gen.comunicados_recibidos)}")
        print(f"  - Personal mínimo: {len(gen.personal_minimo)}")
        print(f"  - Personal apoyo: {len(gen.personal_apoyo)}")
        print(f"  - Obligaciones generales: {len(gen.obligaciones_generales_raw)}")
        print(f"  - Obligaciones específicas: {len(gen.obligaciones_especificas_raw)}")
        
        # Mostrar primera obligación procesada
        if gen.obligaciones_generales_raw:
            primera = gen.obligaciones_generales_raw[0]
            print(f"\n[INFO] Primera obligación procesada:")
            print(f"  - Item: {primera.get('item', 'N/A')}")
            print(f"  - Observaciones generadas: {bool(primera.get('observaciones'))}")
            if primera.get('observaciones'):
                obs = primera.get('observaciones', '')
                print(f"  - Observación (primeros 150 caracteres): {obs[:150]}...")
            print(f"  - Generada con LLM: {primera.get('observacion_generada_llm', False)}")
        
        # Procesar contexto
        print("\n[INFO] Procesando contexto para template...")
        contexto = gen.procesar()
        
        print(f"\n[INFO] Contexto generado con {len(contexto)} variables")
        print(f"  - Tabla obligaciones generales: {len(contexto.get('tabla_obligaciones_generales', []))} items")
        
        # Generar documento
        print("\n[INFO] Generando documento Word...")
        output_dir = Path("output/test")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "seccion_1_completo.docx"
        
        gen.guardar(output_file)
        
        print(f"\n[OK] Documento generado exitosamente en: {output_file}")
        print(f"     Tamaño del archivo: {output_file.stat().st_size / 1024:.2f} KB")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error durante la generación: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("PRUEBA COMPLETA - SECCIÓN 1 CON LLM Y SHAREPOINT")
    print("="*70)
    
    # Verificar configuración
    config_ok = test_configuracion()
    
    if not config_ok:
        print("\n[WARNING] Algunas variables no están configuradas correctamente.")
        print("          El sistema intentará funcionar con lo disponible.")
    
    # Probar generación
    resultado = test_generacion_seccion1()
    
    print("\n" + "="*70)
    if resultado:
        print("[OK] Prueba completada exitosamente")
    else:
        print("[ERROR] La prueba falló. Revisa los errores arriba.")
    print("="*70)

if __name__ == "__main__":
    main()

