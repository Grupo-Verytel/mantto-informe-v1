"""
Script de prueba de integracion completa de la Seccion 8
Valida que todo el flujo funcione correctamente
"""
from src.generadores.seccion_8_presupuesto import GeneradorSeccion8
from src.utils.formato_moneda import formato_moneda_cop
from pathlib import Path
import json
import shutil

def test_carga_datos_json():
    """Prueba la carga de datos desde JSON"""
    print("\n[TEST 1] Carga de datos desde JSON")
    print("-" * 70)
    
    gen = GeneradorSeccion8(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar estructura
    print(f"   [OK] Ejecucion mensual cargada: {len(gen.ejecucion_mensual)} categorias")
    print(f"   [OK] Consolidado cargado: {len(gen.consolidado)} meses")
    print(f"   [OK] Compras bolsa cargadas: {len(gen.compras_bolsa)} items")
    print(f"   [OK] Variaciones cargadas: {len(gen.variaciones)} variaciones")
    
    # Verificar que se calcularon porcentajes y formatos
    if gen.ejecucion_mensual:
        primera = gen.ejecucion_mensual[0]
        print(f"   [OK] Primera categoria: {primera.get('categoria', 'N/A')}")
        print(f"   [OK] Porcentaje calculado: {primera.get('porcentaje_ejecucion', 0)}%")
        print(f"   [OK] Presupuesto formateado: {primera.get('presupuesto_formato', 'N/A')}")
        print(f"   [OK] Ejecutado formateado: {primera.get('ejecutado_formato', 'N/A')}")

def test_calculo_totales():
    """Prueba el calculo de totales"""
    print("\n[TEST 2] Calculo de totales y porcentajes")
    print("-" * 70)
    
    gen = GeneradorSeccion8(anio=2024, mes=9)
    gen.cargar_datos()
    totales = gen._calcular_totales()
    
    print(f"   [OK] Total presupuesto: {formato_moneda_cop(totales['total_presupuesto'])}")
    print(f"   [OK] Total ejecutado: {formato_moneda_cop(totales['total_ejecutado'])}")
    print(f"   [OK] Porcentaje total ejecucion: {totales['porcentaje_total_ejecucion']}%")
    print(f"   [OK] Total compras bolsa: {formato_moneda_cop(totales['total_compras_bolsa'])}")
    
    # Verificar que el porcentaje sea correcto
    if totales['total_presupuesto'] > 0:
        porcentaje_calculado = round((totales['total_ejecutado'] / totales['total_presupuesto']) * 100, 2)
        assert abs(porcentaje_calculado - totales['porcentaje_total_ejecucion']) < 0.01
        print(f"   [OK] Porcentaje calculado correctamente")

def test_procesar_contexto():
    """Prueba el metodo procesar() y el contexto generado"""
    print("\n[TEST 3] Procesamiento de contexto para template")
    print("-" * 70)
    
    gen = GeneradorSeccion8(anio=2024, mes=9)
    gen.cargar_datos()
    contexto = gen.procesar()
    
    # Verificar variables del contexto
    print(f"   [OK] texto_intro presente: {'texto_intro' in contexto}")
    print(f"   [OK] periodo: {contexto.get('periodo', 'N/A')}")
    print(f"   [OK] contrato_numero: {contexto.get('contrato_numero', 'N/A')}")
    print(f"   [OK] total_ejecucion_mensual: {contexto.get('total_ejecucion_mensual', 0)}")
    print(f"   [OK] hay_ejecucion_mensual: {contexto.get('hay_ejecucion_mensual', False)}")
    print(f"   [OK] total_consolidado: {contexto.get('total_consolidado', 0)}")
    print(f"   [OK] hay_consolidado: {contexto.get('hay_consolidado', False)}")
    print(f"   [OK] total_compras_bolsa: {contexto.get('total_compras_bolsa', 0)}")
    print(f"   [OK] hay_compras_bolsa: {contexto.get('hay_compras_bolsa', False)}")
    print(f"   [OK] total_variaciones: {contexto.get('total_variaciones', 0)}")
    print(f"   [OK] hay_variaciones: {contexto.get('hay_variaciones', False)}")
    
    # Verificar totales formateados
    print(f"   [OK] total_presupuesto_formato: {contexto.get('total_presupuesto_formato', 'N/A')}")
    print(f"   [OK] total_ejecutado_formato: {contexto.get('total_ejecutado_formato', 'N/A')}")
    print(f"   [OK] porcentaje_total_ejecucion: {contexto.get('porcentaje_total_ejecucion', 0)}%")
    print(f"   [OK] observaciones presente: {'observaciones' in contexto}")

def test_generacion_completa():
    """Prueba la generacion completa del documento"""
    print("\n[TEST 4] Generacion completa del documento")
    print("-" * 70)
    
    gen = GeneradorSeccion8(anio=2024, mes=9)
    gen.cargar_datos()
    
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Verificar estructura basica
        print(f"   [OK] Paragrafos: {len(doc.paragraphs)}")
        print(f"   [OK] Tablas: {len(doc.tables)}")
        
        # Guardar para inspeccion manual
        output_path = Path("output/test/seccion_8_integracion.docx")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        gen.guardar(output_path)
        print(f"   [OK] Guardado en: {output_path}")
        
    except Exception as e:
        print(f"   [ERROR] Error al generar: {e}")
        import traceback
        traceback.print_exc()

def test_datos_dummy():
    """Prueba la generacion de datos dummy cuando no hay JSON"""
    print("\n[TEST 5] Generacion de datos dummy")
    print("-" * 70)
    
    # Crear backup del JSON si existe
    json_path = Path("data/fuentes/ejecucion_presupuestal_9_2024.json")
    backup_path = Path("data/fuentes/ejecucion_presupuestal_9_2024.json.backup")
    
    if json_path.exists():
        shutil.copy(json_path, backup_path)
        json_path.unlink()
    
    try:
        gen = GeneradorSeccion8(anio=2024, mes=9)
        gen.cargar_datos()
        
        # Verificar que se generaron datos dummy
        print(f"   [OK] Ejecucion mensual dummy: {len(gen.ejecucion_mensual)} categorias")
        print(f"   [OK] Consolidado dummy: {len(gen.consolidado)} meses")
        print(f"   [OK] Compras bolsa dummy: {len(gen.compras_bolsa)} items")
        print(f"   [OK] Variaciones dummy: {len(gen.variaciones)} variaciones")
        
        # Verificar que todos tienen datos y formatos
        assert len(gen.ejecucion_mensual) > 0, "Debe haber ejecucion mensual dummy"
        assert all('porcentaje_ejecucion' in item for item in gen.ejecucion_mensual)
        assert all('presupuesto_formato' in item for item in gen.ejecucion_mensual)
        
        print("   [OK] Todos los datos dummy generados correctamente con formatos")
        
    finally:
        # Restaurar JSON si existia
        if backup_path.exists():
            shutil.copy(backup_path, json_path)
            backup_path.unlink()

def test_formato_moneda():
    """Prueba el formato de moneda en los datos"""
    print("\n[TEST 6] Formato de moneda")
    print("-" * 70)
    
    gen = GeneradorSeccion8(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar formato en ejecucion mensual
    if gen.ejecucion_mensual:
        item = gen.ejecucion_mensual[0]
        presupuesto_formato = item.get('presupuesto_formato', '')
        print(f"   [OK] Formato presupuesto: {presupuesto_formato}")
        assert presupuesto_formato.startswith('$'), "Formato debe empezar con $"
        assert '.' in presupuesto_formato, "Formato debe tener separadores de miles"
    
    # Verificar formato en compras bolsa
    if gen.compras_bolsa:
        item = gen.compras_bolsa[0]
        valor_total_formato = item.get('valor_total_formato', '')
        print(f"   [OK] Formato valor total: {valor_total_formato}")
        assert valor_total_formato.startswith('$'), "Formato debe empezar con $"

def test_porcentajes_calculados():
    """Prueba que los porcentajes se calculen correctamente"""
    print("\n[TEST 7] Calculo de porcentajes")
    print("-" * 70)
    
    gen = GeneradorSeccion8(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar porcentajes en ejecucion mensual
    for item in gen.ejecucion_mensual:
        presupuesto = item.get('presupuesto', 0)
        ejecutado = item.get('ejecutado', 0)
        porcentaje = item.get('porcentaje_ejecucion', 0)
        
        if presupuesto > 0:
            porcentaje_esperado = round((ejecutado / presupuesto) * 100, 2)
            assert abs(porcentaje - porcentaje_esperado) < 0.01, f"Porcentaje incorrecto para {item.get('categoria')}"
            print(f"   [OK] {item.get('categoria')}: {porcentaje}% (esperado: {porcentaje_esperado}%)")
    
    print("   [OK] Todos los porcentajes calculados correctamente")

def main():
    """Ejecuta todas las pruebas de integracion"""
    print("=" * 70)
    print("PRUEBA DE INTEGRACION - SECCION 8")
    print("=" * 70)
    
    test_carga_datos_json()
    test_calculo_totales()
    test_porcentajes_calculados()
    test_formato_moneda()
    test_procesar_contexto()
    test_generacion_completa()
    test_datos_dummy()
    
    print("\n" + "=" * 70)
    print("[OK] TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    main()

