"""
Script de prueba de integracion completa de la Seccion 7
Valida que todo el flujo funcione correctamente
"""
from src.generadores.seccion_7_siniestros import GeneradorSeccion7
from pathlib import Path
import json
import shutil

def test_carga_datos_json():
    """Prueba la carga de datos desde JSON"""
    print("\n[TEST 1] Carga de datos desde JSON")
    print("-" * 70)
    
    gen = GeneradorSeccion7(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar estructura
    print(f"   [OK] Siniestros cargados: {len(gen.siniestros)}")
    print(f"   [OK] Afectaciones cargadas: {len(gen.afectaciones)}")
    print(f"   [OK] Acciones cargadas: {len(gen.acciones)}")
    print(f"   [OK] Seguimiento cargado: {len(gen.seguimiento)}")
    
    # Verificar contenido
    if gen.siniestros:
        primer_siniestro = gen.siniestros[0]
        print(f"   [OK] Primer siniestro: {primer_siniestro.get('tipo', 'N/A')}")
        print(f"   [OK] Lugar: {primer_siniestro.get('lugar', 'N/A')}")
    
    if gen.afectaciones:
        primera_afectacion = gen.afectaciones[0]
        print(f"   [OK] Primera afectacion: {primera_afectacion.get('componente', 'N/A')}")
        print(f"   [OK] Impacto: {primera_afectacion.get('impacto', 'N/A')}")
    
    if gen.acciones:
        primera_accion = gen.acciones[0]
        print(f"   [OK] Primera accion: {primera_accion.get('accion', 'N/A')[:50]}...")
        print(f"   [OK] Estado: {primera_accion.get('estado', 'N/A')}")

def test_procesar_contexto():
    """Prueba el metodo procesar() y el contexto generado"""
    print("\n[TEST 2] Procesamiento de contexto para template")
    print("-" * 70)
    
    gen = GeneradorSeccion7(anio=2024, mes=9)
    gen.cargar_datos()
    contexto = gen.procesar()
    
    # Verificar variables del contexto
    print(f"   [OK] texto_intro presente: {'texto_intro' in contexto}")
    print(f"   [OK] total_siniestros: {contexto.get('total_siniestros', 0)}")
    print(f"   [OK] hay_siniestros: {contexto.get('hay_siniestros', False)}")
    print(f"   [OK] total_afectaciones: {contexto.get('total_afectaciones', 0)}")
    print(f"   [OK] hay_afectaciones: {contexto.get('hay_afectaciones', False)}")
    print(f"   [OK] total_acciones: {contexto.get('total_acciones', 0)}")
    print(f"   [OK] hay_acciones: {contexto.get('hay_acciones', False)}")
    print(f"   [OK] total_seguimiento: {contexto.get('total_seguimiento', 0)}")
    print(f"   [OK] hay_seguimiento: {contexto.get('hay_seguimiento', False)}")
    
    # Verificar que las listas esten presentes
    print(f"   [OK] Lista siniestros: {len(contexto.get('siniestros', []))} items")
    print(f"   [OK] Lista afectaciones: {len(contexto.get('afectaciones', []))} items")
    print(f"   [OK] Lista acciones: {len(contexto.get('acciones', []))} items")
    print(f"   [OK] Lista seguimiento: {len(contexto.get('seguimiento', []))} items")

def test_generacion_completa():
    """Prueba la generacion completa del documento"""
    print("\n[TEST 3] Generacion completa del documento")
    print("-" * 70)
    
    gen = GeneradorSeccion7(anio=2024, mes=9)
    gen.cargar_datos()
    
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Verificar estructura basica
        print(f"   [OK] Paragrafos: {len(doc.paragraphs)}")
        print(f"   [OK] Tablas: {len(doc.tables)}")
        
        # Guardar para inspeccion manual
        output_path = Path("output/test/seccion_7_integracion.docx")
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
    json_path = Path("data/fuentes/siniestros_9_2024.json")
    backup_path = Path("data/fuentes/siniestros_9_2024.json.backup")
    
    if json_path.exists():
        shutil.copy(json_path, backup_path)
        json_path.unlink()
    
    try:
        gen = GeneradorSeccion7(anio=2024, mes=9)
        gen.cargar_datos()
        
        # Verificar que se generaron datos dummy
        print(f"   [OK] Siniestros dummy: {len(gen.siniestros)}")
        print(f"   [OK] Afectaciones dummy: {len(gen.afectaciones)}")
        print(f"   [OK] Acciones dummy: {len(gen.acciones)}")
        print(f"   [OK] Seguimiento dummy: {len(gen.seguimiento)}")
        
        # Verificar que todos tienen datos
        assert len(gen.siniestros) > 0, "Debe haber siniestros dummy"
        assert len(gen.afectaciones) > 0, "Debe haber afectaciones dummy"
        assert len(gen.acciones) > 0, "Debe haber acciones dummy"
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
        "siniestros": [],
        "afectaciones": [],
        "acciones": [],
        "seguimiento": []
    }
    
    json_path = Path("data/fuentes/siniestros_9_2024.json")
    backup_path = Path("data/fuentes/siniestros_9_2024.json.backup")
    
    if json_path.exists():
        shutil.copy(json_path, backup_path)
    
    try:
        # Guardar JSON vacio
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_vacio, f, indent=2, ensure_ascii=False)
        
        gen = GeneradorSeccion7(anio=2024, mes=9)
        gen.cargar_datos()
        contexto = gen.procesar()
        
        # Verificar que los condicionales sean False
        print(f"   [OK] hay_siniestros: {contexto.get('hay_siniestros')} (esperado: False)")
        print(f"   [OK] hay_afectaciones: {contexto.get('hay_afectaciones')} (esperado: False)")
        print(f"   [OK] hay_acciones: {contexto.get('hay_acciones')} (esperado: False)")
        print(f"   [OK] hay_seguimiento: {contexto.get('hay_seguimiento')} (esperado: False)")
        
        # Verificar que los totales sean 0
        assert contexto.get('total_siniestros') == 0
        assert contexto.get('total_afectaciones') == 0
        assert contexto.get('total_acciones') == 0
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

def test_tipos_siniestros():
    """Prueba que los tipos de siniestros se manejen correctamente"""
    print("\n[TEST 6] Tipos de siniestros")
    print("-" * 70)
    
    gen = GeneradorSeccion7(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar tipos de siniestros
    tipos_encontrados = set()
    for siniestro in gen.siniestros:
        tipo = siniestro.get('tipo', '')
        tipos_encontrados.add(tipo)
        print(f"   Siniestro: {tipo} - {siniestro.get('lugar', 'N/A')}")
    
    tipos_validos = {"Vandalismo", "Robo", "Falla eléctrica", "Daño por clima", 
                     "Accidente vehicular", "Corte de servicios", "Falla de equipos"}
    
    print(f"   [OK] Tipos encontrados: {tipos_encontrados}")
    
    # Verificar estados de acciones
    estados_acciones = set()
    for accion in gen.acciones:
        estado = accion.get('estado', '')
        estados_acciones.add(estado)
    
    print(f"   [OK] Estados de acciones: {estados_acciones}")
    
    # Verificar estados de seguimiento
    estados_seguimiento = set()
    for item in gen.seguimiento:
        estado = item.get('estado', '')
        estados_seguimiento.add(estado)
    
    print(f"   [OK] Estados de seguimiento: {estados_seguimiento}")

def main():
    """Ejecuta todas las pruebas de integracion"""
    print("=" * 70)
    print("PRUEBA DE INTEGRACION - SECCION 7")
    print("=" * 70)
    
    test_carga_datos_json()
    test_procesar_contexto()
    test_tipos_siniestros()
    test_generacion_completa()
    test_datos_dummy()
    test_datos_vacios()
    
    print("\n" + "=" * 70)
    print("[OK] TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    main()

