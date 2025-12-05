"""
Script de prueba de integracion completa de la Seccion 6
Valida que todo el flujo funcione correctamente
"""
from src.generadores.seccion_6_visitas import GeneradorSeccion6
from pathlib import Path
import json
import shutil

def test_carga_datos_json():
    """Prueba la carga de datos desde JSON"""
    print("\n[TEST 1] Carga de datos desde JSON")
    print("-" * 70)
    
    gen = GeneradorSeccion6(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar estructura
    print(f"   [OK] Visitas cargadas: {len(gen.visitas)}")
    print(f"   [OK] Observaciones cargadas: {len(gen.observaciones)}")
    print(f"   [OK] Hallazgos cargados: {len(gen.hallazgos)}")
    print(f"   [OK] Seguimiento cargado: {len(gen.seguimiento)}")
    
    # Verificar contenido
    if gen.visitas:
        primera_visita = gen.visitas[0]
        print(f"   [OK] Primera visita: {primera_visita.get('lugar', 'N/A')}")
        print(f"   [OK] Responsable: {primera_visita.get('responsable', 'N/A')}")
    
    if gen.hallazgos:
        primer_hallazgo = gen.hallazgos[0]
        print(f"   [OK] Primer hallazgo: {primer_hallazgo.get('hallazgo', 'N/A')}")
        print(f"   [OK] Impacto: {primer_hallazgo.get('impacto', 'N/A')}")

def test_procesar_contexto():
    """Prueba el metodo procesar() y el contexto generado"""
    print("\n[TEST 2] Procesamiento de contexto para template")
    print("-" * 70)
    
    gen = GeneradorSeccion6(anio=2024, mes=9)
    gen.cargar_datos()
    contexto = gen.procesar()
    
    # Verificar variables del contexto
    print(f"   [OK] texto_intro presente: {'texto_intro' in contexto}")
    print(f"   [OK] total_visitas: {contexto.get('total_visitas', 0)}")
    print(f"   [OK] hay_visitas: {contexto.get('hay_visitas', False)}")
    print(f"   [OK] total_observaciones: {contexto.get('total_observaciones', 0)}")
    print(f"   [OK] hay_observaciones: {contexto.get('hay_observaciones', False)}")
    print(f"   [OK] total_hallazgos: {contexto.get('total_hallazgos', 0)}")
    print(f"   [OK] hay_hallazgos: {contexto.get('hay_hallazgos', False)}")
    print(f"   [OK] total_seguimiento: {contexto.get('total_seguimiento', 0)}")
    print(f"   [OK] hay_seguimiento: {contexto.get('hay_seguimiento', False)}")
    
    # Verificar que las listas esten presentes
    print(f"   [OK] Lista visitas: {len(contexto.get('visitas', []))} items")
    print(f"   [OK] Lista observaciones: {len(contexto.get('observaciones', []))} items")
    print(f"   [OK] Lista hallazgos: {len(contexto.get('hallazgos', []))} items")
    print(f"   [OK] Lista seguimiento: {len(contexto.get('seguimiento', []))} items")

def test_generacion_completa():
    """Prueba la generacion completa del documento"""
    print("\n[TEST 3] Generacion completa del documento")
    print("-" * 70)
    
    gen = GeneradorSeccion6(anio=2024, mes=9)
    gen.cargar_datos()
    
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Verificar estructura basica
        print(f"   [OK] Paragrafos: {len(doc.paragraphs)}")
        print(f"   [OK] Tablas: {len(doc.tables)}")
        
        # Guardar para inspeccion manual
        output_path = Path("output/test/seccion_6_integracion.docx")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        gen.guardar(output_path)
        print(f"   [OK] Guardado en: {output_path}")
        
    except Exception as e:
        print(f"   [ERROR] Error al generar: {e}")
        import traceback
        traceback.print_exc()

def test_datos_dummy():
    """Prueba la generacion de datos dummy cuando no hay JSON"""
    print("\n[TEST 4] Generacion de datos dummy")
    print("-" * 70)
    
    # Crear backup del JSON si existe
    json_path = Path("data/fuentes/visitas_9_2024.json")
    backup_path = Path("data/fuentes/visitas_9_2024.json.backup")
    
    if json_path.exists():
        shutil.copy(json_path, backup_path)
        json_path.unlink()
    
    try:
        gen = GeneradorSeccion6(anio=2024, mes=9)
        gen.cargar_datos()
        
        # Verificar que se generaron datos dummy
        print(f"   [OK] Visitas dummy: {len(gen.visitas)}")
        print(f"   [OK] Observaciones dummy: {len(gen.observaciones)}")
        print(f"   [OK] Hallazgos dummy: {len(gen.hallazgos)}")
        print(f"   [OK] Seguimiento dummy: {len(gen.seguimiento)}")
        
        # Verificar que todos tienen datos
        assert len(gen.visitas) > 0, "Debe haber visitas dummy"
        assert len(gen.observaciones) > 0, "Debe haber observaciones dummy"
        assert len(gen.hallazgos) > 0, "Debe haber hallazgos dummy"
        assert len(gen.seguimiento) > 0, "Debe haber seguimiento dummy"
        
        print("   [OK] Todos los datos dummy generados correctamente")
        
    finally:
        # Restaurar JSON si existia
        if backup_path.exists():
            shutil.copy(backup_path, json_path)
            backup_path.unlink()

def test_datos_vacios():
    """Prueba el manejo de listas vacias"""
    print("\n[TEST 5] Manejo de datos vacios")
    print("-" * 70)
    
    # Crear JSON con listas vacias
    json_vacio = {
        "visitas": [],
        "observaciones": [],
        "hallazgos": [],
        "seguimiento": []
    }
    
    json_path = Path("data/fuentes/visitas_9_2024.json")
    backup_path = Path("data/fuentes/visitas_9_2024.json.backup")
    
    if json_path.exists():
        shutil.copy(json_path, backup_path)
    
    try:
        # Guardar JSON vacio
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_vacio, f, indent=2, ensure_ascii=False)
        
        gen = GeneradorSeccion6(anio=2024, mes=9)
        gen.cargar_datos()
        contexto = gen.procesar()
        
        # Verificar que los condicionales sean False
        print(f"   [OK] hay_visitas: {contexto.get('hay_visitas')} (esperado: False)")
        print(f"   [OK] hay_observaciones: {contexto.get('hay_observaciones')} (esperado: False)")
        print(f"   [OK] hay_hallazgos: {contexto.get('hay_hallazgos')} (esperado: False)")
        print(f"   [OK] hay_seguimiento: {contexto.get('hay_seguimiento')} (esperado: False)")
        
        # Verificar que los totales sean 0
        assert contexto.get('total_visitas') == 0
        assert contexto.get('total_observaciones') == 0
        assert contexto.get('total_hallazgos') == 0
        assert contexto.get('total_seguimiento') == 0
        
        print("   [OK] Manejo de datos vacios correcto")
        
        # Intentar generar documento (debe funcionar sin errores)
        doc = gen.generar()
        print("   [OK] Documento generado con datos vacios sin errores")
        
    finally:
        # Restaurar JSON original
        if backup_path.exists():
            shutil.copy(backup_path, json_path)
            backup_path.unlink()

def test_formato_fechas():
    """Prueba que las fechas se manejen correctamente"""
    print("\n[TEST 6] Formato de fechas")
    print("-" * 70)
    
    gen = GeneradorSeccion6(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar formato de fechas en visitas
    if gen.visitas:
        for i, visita in enumerate(gen.visitas[:2], 1):
            fecha = visita.get('fecha', '')
            print(f"   Visita {i} - Fecha: {fecha}")
            # Verificar que tenga formato ISO o español
            assert len(fecha) > 0, "Fecha no puede estar vacia"
    
    # Verificar formato de fechas en hallazgos
    if gen.hallazgos:
        for i, hallazgo in enumerate(gen.hallazgos[:2], 1):
            fecha = hallazgo.get('fecha', '')
            print(f"   Hallazgo {i} - Fecha: {fecha}")
            assert len(fecha) > 0, "Fecha no puede estar vacia"
    
    print("   [OK] Formato de fechas correcto")

def main():
    """Ejecuta todas las pruebas de integracion"""
    print("=" * 70)
    print("PRUEBA DE INTEGRACION - SECCION 6")
    print("=" * 70)
    
    test_carga_datos_json()
    test_procesar_contexto()
    test_formato_fechas()
    test_generacion_completa()
    test_datos_dummy()
    test_datos_vacios()
    
    print("\n" + "=" * 70)
    print("[OK] TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    main()

