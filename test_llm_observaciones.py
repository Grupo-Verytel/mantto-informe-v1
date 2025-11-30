"""
Script de prueba para generación de observaciones con LLM
"""
from pathlib import Path
from src.generadores.seccion_1_info_general import GeneradorSeccion1
from src.ia.extractor_observaciones import get_extractor_observaciones
import os

def test_extractor_directo():
    """Prueba el extractor de observaciones directamente"""
    print("="*70)
    print("PRUEBA 1: Extractor de Observaciones Directo")
    print("="*70)
    
    # Verificar si hay API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[WARNING] OPENAI_API_KEY no configurada. Usando modo fallback.")
        print("         Configura la variable de entorno para usar LLM real.")
    
    extractor = get_extractor_observaciones()
    
    # Obligación de ejemplo
    obligacion = {
        "item": 1,
        "obligacion": "Acatar la Constitución, la Ley, las normas legales y procedimientos establecidos por el Gobierno Nacional y Distrital, y demás disposiciones pertinentes.",
        "periodicidad": "Permanente",
        "cumplio": "Cumplió",
        "observaciones": "",
        "anexo": "01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 1/ archivo.pdf",
        "regenerar_observacion": True
    }
    
    print(f"\nObligación original:")
    print(f"  Item: {obligacion['item']}")
    print(f"  Obligación: {obligacion['obligacion'][:80]}...")
    print(f"  Anexo: {obligacion['anexo']}")
    print(f"  Observaciones (antes): {obligacion['observaciones'] or '(vacío)'}")
    
    # Procesar obligación
    print("\n[INFO] Procesando obligación...")
    obligacion_procesada = extractor.procesar_obligacion(obligacion)
    
    print(f"\nObligación procesada:")
    print(f"  Observaciones (después): {obligacion_procesada['observaciones'][:200]}...")
    print(f"  Generada con LLM: {obligacion_procesada.get('observacion_generada_llm', False)}")
    
    return obligacion_procesada

def test_generador_seccion1():
    """Prueba el generador completo de la Sección 1"""
    print("\n" + "="*70)
    print("PRUEBA 2: Generador Sección 1 con LLM")
    print("="*70)
    
    # Verificar si hay API key
    api_key = os.getenv("OPENAI_API_KEY")
    usar_llm = bool(api_key)
    
    if not usar_llm:
        print("[WARNING] OPENAI_API_KEY no configurada. Usando modo sin LLM.")
        print("         Las observaciones serán genéricas.")
    
    # Crear generador
    gen = GeneradorSeccion1(anio=2025, mes=9, usar_llm_observaciones=usar_llm)
    
    print("\n[INFO] Cargando datos...")
    gen.cargar_datos()
    
    print(f"\nObligaciones cargadas:")
    print(f"  Generales: {len(gen.obligaciones_generales_raw)}")
    print(f"  Específicas: {len(gen.obligaciones_especificas_raw)}")
    print(f"  Ambientales: {len(gen.obligaciones_ambientales_raw)}")
    print(f"  Anexos: {len(gen.obligaciones_anexos_raw)}")
    
    # Mostrar primera obligación procesada
    if gen.obligaciones_generales_raw:
        primera = gen.obligaciones_generales_raw[0]
        print(f"\nPrimera obligación procesada:")
        print(f"  Item: {primera.get('item', 'N/A')}")
        print(f"  Observaciones: {primera.get('observaciones', '')[:200]}...")
        print(f"  Generada con LLM: {primera.get('observacion_generada_llm', False)}")
    
    # Procesar contexto
    print("\n[INFO] Procesando contexto para template...")
    contexto = gen.procesar()
    
    # Verificar tablas de obligaciones en el contexto
    print(f"\nTablas de obligaciones en contexto:")
    print(f"  tabla_obligaciones_generales: {len(contexto.get('tabla_obligaciones_generales', []))} items")
    
    return gen, contexto

def main():
    """Función principal de prueba"""
    print("\n" + "="*70)
    print("PRUEBA DE GENERACIÓN DE OBSERVACIONES CON LLM")
    print("="*70)
    print("\nEste script prueba el sistema de generación dinámica de observaciones")
    print("basándose en el contenido de archivos de anexos usando LLM.\n")
    
    try:
        # Prueba 1: Extractor directo
        obligacion_procesada = test_extractor_directo()
        
        # Prueba 2: Generador completo
        gen, contexto = test_generador_seccion1()
        
        print("\n" + "="*70)
        print("RESUMEN")
        print("="*70)
        print("\n[OK] Pruebas completadas exitosamente")
        print("\nPróximos pasos:")
        print("1. Configurar OPENAI_API_KEY si quieres usar LLM real")
        print("2. Colocar archivos de anexos en data/anexos/")
        print("3. Crear archivo obligaciones_{mes}_{anio}.json con las obligaciones")
        print("4. Ejecutar generación completa del informe")
        
    except Exception as e:
        print(f"\n[ERROR] Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

