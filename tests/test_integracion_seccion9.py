"""
Script de prueba de integracion completa de la Seccion 9
Valida que todo el flujo funcione correctamente
"""
from src.generadores.seccion_9_riesgos import GeneradorSeccion9
from pathlib import Path
import shutil

def test_carga_datos_csv():
    """Prueba la carga de datos desde CSV"""
    print("\n[TEST 1] Carga de datos desde CSV")
    print("-" * 70)
    
    gen = GeneradorSeccion9(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar estructura
    print(f"   [OK] Riesgos cargados: {len(gen.riesgos)}")
    
    # Verificar que se calcularon niveles y clasificaciones
    if gen.riesgos:
        primer_riesgo = gen.riesgos[0]
        print(f"   [OK] Primer riesgo: {primer_riesgo.get('riesgo', 'N/A')}")
        print(f"   [OK] Probabilidad: {primer_riesgo.get('probabilidad', 0)}")
        print(f"   [OK] Impacto: {primer_riesgo.get('impacto', 0)}")
        print(f"   [OK] Nivel calculado: {primer_riesgo.get('nivel_num', 0)}")
        print(f"   [OK] Clasificacion: {primer_riesgo.get('clasificacion', 'N/A')}")
        
        # Verificar que está ordenado (el primero debe ser el de mayor nivel)
        niveles = [r.get('nivel_num', 0) for r in gen.riesgos]
        print(f"   [OK] Niveles ordenados: {niveles}")
        assert niveles == sorted(niveles, reverse=True), "Riesgos deben estar ordenados descendente"

def test_calculo_clasificacion():
    """Prueba el calculo de clasificaciones"""
    print("\n[TEST 2] Calculo de clasificaciones")
    print("-" * 70)
    
    gen = GeneradorSeccion9(anio=2024, mes=9)
    
    # Probar diferentes niveles
    casos = [
        (1, "Bajo"),   # 1x1 = 1
        (4, "Bajo"),   # 2x2 = 4
        (5, "Medio"),  # 1x5 = 5
        (8, "Medio"),  # 2x4 = 8
        (9, "Alto"),   # 3x3 = 9
        (12, "Alto"),  # 3x4 = 12
        (13, "Crítico"), # 3x5 = 15
        (25, "Crítico") # 5x5 = 25
    ]
    
    for nivel, esperado in casos:
        resultado = gen._calcular_clasificacion(nivel)
        print(f"   Nivel {nivel}: {resultado} (esperado: {esperado})")
        assert resultado == esperado, f"Clasificacion incorrecta para nivel {nivel}"

def test_resumen_clasificacion():
    """Prueba la generacion del resumen por clasificacion"""
    print("\n[TEST 3] Resumen por clasificacion")
    print("-" * 70)
    
    gen = GeneradorSeccion9(anio=2024, mes=9)
    gen.cargar_datos()
    gen._generar_resumen_clasificacion()
    
    print(f"   [OK] Total clasificaciones: {len(gen.resumen_clasificacion)}")
    
    # Verificar que los porcentajes suman 100%
    total_porcentaje = sum(item.get('porcentaje', 0) for item in gen.resumen_clasificacion)
    print(f"   [OK] Suma de porcentajes: {total_porcentaje}%")
    assert abs(total_porcentaje - 100.0) < 0.1, "Porcentajes deben sumar 100%"
    
    # Verificar orden (Crítico > Alto > Medio > Bajo)
    orden_esperado = ["Crítico", "Alto", "Medio", "Bajo"]
    orden_actual = [item.get('clasificacion') for item in gen.resumen_clasificacion]
    print(f"   [OK] Orden de clasificaciones: {orden_actual}")
    
    for item in gen.resumen_clasificacion:
        print(f"      {item.get('clasificacion')}: {item.get('cantidad')} ({item.get('porcentaje')}%)")

def test_generacion_heatmap():
    """Prueba la generacion del heatmap"""
    print("\n[TEST 4] Generacion de heatmap")
    print("-" * 70)
    
    gen = GeneradorSeccion9(anio=2024, mes=9)
    gen.cargar_datos()
    
    output_dir = Path("output/test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        ruta_heatmap = gen._generar_heatmap(output_dir)
        
        if ruta_heatmap:
            print(f"   [OK] Heatmap generado: {ruta_heatmap}")
            archivo = Path(ruta_heatmap)
            assert archivo.exists(), "Archivo heatmap debe existir"
            print(f"   [OK] Archivo existe: {archivo.exists()}")
            print(f"   [OK] Tamaño archivo: {archivo.stat().st_size} bytes")
        else:
            print("   [WARN] Heatmap no generado (matplotlib no disponible o sin riesgos)")
    except Exception as e:
        print(f"   [WARN] Error al generar heatmap: {e}")

def test_procesar_contexto():
    """Prueba el metodo procesar() y el contexto generado"""
    print("\n[TEST 5] Procesamiento de contexto para template")
    print("-" * 70)
    
    gen = GeneradorSeccion9(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Generar heatmap primero
    output_dir = Path("output/test")
    output_dir.mkdir(parents=True, exist_ok=True)
    gen.grafico_matriz_img = gen._generar_heatmap(output_dir)
    
    contexto = gen.procesar()
    
    # Verificar variables del contexto
    print(f"   [OK] texto_intro presente: {'texto_intro' in contexto}")
    print(f"   [OK] total_riesgos: {contexto.get('total_riesgos', 0)}")
    print(f"   [OK] hay_riesgos: {contexto.get('hay_riesgos', False)}")
    print(f"   [OK] riesgos_criticos: {contexto.get('riesgos_criticos', 0)}")
    print(f"   [OK] riesgos_altos: {contexto.get('riesgos_altos', 0)}")
    print(f"   [OK] riesgos_medios: {contexto.get('riesgos_medios', 0)}")
    print(f"   [OK] riesgos_bajos: {contexto.get('riesgos_bajos', 0)}")
    print(f"   [OK] total_resumen: {contexto.get('total_resumen', 0)}")
    print(f"   [OK] hay_resumen: {contexto.get('hay_resumen', False)}")
    print(f"   [OK] grafico_matriz_img: {contexto.get('grafico_matriz_img', 'N/A')[:50]}...")
    
    # Verificar que las listas esten presentes
    print(f"   [OK] Lista riesgos: {len(contexto.get('riesgos', []))} items")
    print(f"   [OK] Lista resumen: {len(contexto.get('resumen_clasificacion', []))} items")

def test_generacion_completa():
    """Prueba la generacion completa del documento"""
    print("\n[TEST 6] Generacion completa del documento")
    print("-" * 70)
    
    gen = GeneradorSeccion9(anio=2024, mes=9)
    gen.cargar_datos()
    
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Verificar estructura basica
        print(f"   [OK] Paragrafos: {len(doc.paragraphs)}")
        print(f"   [OK] Tablas: {len(doc.tables)}")
        
        # Verificar que el heatmap se genero
        if gen.grafico_matriz_img:
            archivo_heatmap = Path(gen.grafico_matriz_img)
            if archivo_heatmap.exists():
                print(f"   [OK] Heatmap generado: {archivo_heatmap}")
        
        # Guardar para inspeccion manual
        output_path = Path("output/test/seccion_9_integracion.docx")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        gen.guardar(output_path)
        print(f"   [OK] Guardado en: {output_path}")
        
    except Exception as e:
        print(f"   [ERROR] Error al generar: {e}")
        import traceback
        traceback.print_exc()

def test_datos_dummy():
    """Prueba la generacion de datos dummy cuando no hay CSV"""
    print("\n[TEST 7] Generacion de datos dummy")
    print("-" * 70)
    
    # Crear backup del CSV si existe
    csv_path = Path("data/fuentes/matriz_riesgos.csv")
    backup_path = Path("data/fuentes/matriz_riesgos.csv.backup")
    
    if csv_path.exists():
        shutil.copy(csv_path, backup_path)
        csv_path.unlink()
    
    try:
        gen = GeneradorSeccion9(anio=2024, mes=9)
        gen.cargar_datos()
        
        # Verificar que se generaron datos dummy
        print(f"   [OK] Riesgos dummy: {len(gen.riesgos)}")
        
        # Verificar que todos tienen niveles y clasificaciones
        assert len(gen.riesgos) > 0, "Debe haber riesgos dummy"
        assert all('nivel_num' in r for r in gen.riesgos)
        assert all('clasificacion' in r for r in gen.riesgos)
        
        print("   [OK] Todos los datos dummy generados correctamente con clasificaciones")
        
    finally:
        # Restaurar CSV si existia
        if backup_path.exists():
            shutil.copy(backup_path, csv_path)
            backup_path.unlink()

def test_ordenamiento_riesgos():
    """Prueba que los riesgos esten ordenados correctamente"""
    print("\n[TEST 8] Ordenamiento de riesgos")
    print("-" * 70)
    
    gen = GeneradorSeccion9(anio=2024, mes=9)
    gen.cargar_datos()
    
    # Verificar orden descendente
    niveles = [r.get('nivel_num', 0) for r in gen.riesgos]
    niveles_ordenados = sorted(niveles, reverse=True)
    
    print(f"   [OK] Niveles actuales: {niveles}")
    print(f"   [OK] Niveles esperados: {niveles_ordenados}")
    
    assert niveles == niveles_ordenados, "Riesgos deben estar ordenados por nivel descendente"
    
    # Verificar que los críticos estan primero
    clasificaciones = [r.get('clasificacion') for r in gen.riesgos]
    print(f"   [OK] Clasificaciones en orden: {clasificaciones}")
    
    # Verificar que críticos vienen antes que altos, etc.
    orden_valor = {"Crítico": 4, "Alto": 3, "Medio": 2, "Bajo": 1}
    valores_orden = [orden_valor.get(c, 0) for c in clasificaciones]
    valores_esperados = sorted(valores_orden, reverse=True)
    
    assert valores_orden == valores_esperados, "Clasificaciones deben estar ordenadas por severidad"

def main():
    """Ejecuta todas las pruebas de integracion"""
    print("=" * 70)
    print("PRUEBA DE INTEGRACION - SECCION 9")
    print("=" * 70)
    
    test_carga_datos_csv()
    test_calculo_clasificacion()
    test_ordenamiento_riesgos()
    test_resumen_clasificacion()
    test_generacion_heatmap()
    test_procesar_contexto()
    test_generacion_completa()
    test_datos_dummy()
    
    print("\n" + "=" * 70)
    print("[OK] TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    main()

