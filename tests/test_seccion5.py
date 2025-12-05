"""
Script de prueba para validar la generacion de la Seccion 5
"""
from src.generadores.seccion_5_laboratorio import GeneradorSeccion5
from pathlib import Path

def test_seccion5():
    """Prueba la generacion de la Seccion 5 para septiembre 2025"""
    print("=" * 70)
    print("GENERADOR SECCION 5 - INFORME DE LABORATORIO")
    print("=" * 70)
    
    # Crear generador
    print("\n[1] Generando documento para Septiembre 2025...")
    gen = GeneradorSeccion5(anio=2025, mes=9)
    
    # Cargar datos
    print("[2] Cargando datos...")
    gen.cargar_datos()
    print("   [OK] Datos cargados")
    
    # Verificar datos cargados
    print("\n[3] Validando datos cargados...")
    
    estadisticas = gen.datos.get('estadisticas', {})
    equipos_recibidos = estadisticas.get('equipos_recibidos', 0)
    equipos_reparados = estadisticas.get('equipos_reparados', 0)
    equipos_no_reparables = estadisticas.get('equipos_no_reparables', 0)
    equipos_rma = estadisticas.get('equipos_rma', 0)
    
    equipos_reparados_list = gen.datos.get('equipos_reparados', [])
    equipos_no_operativos_list = gen.datos.get('equipos_no_operativos', [])
    equipos_rma_list = gen.datos.get('equipos_rma_proceso', [])
    equipos_pendientes_list = gen.datos.get('equipos_pendientes_parte', [])
    resumen_partes = gen.datos.get('resumen_partes_requeridas', [])
    
    print(f"   [OK] Equipos recibidos: {equipos_recibidos}")
    print(f"   [OK] Equipos reparados: {equipos_reparados} ({len(equipos_reparados_list)} en lista)")
    print(f"   [OK] Equipos no reparables: {equipos_no_reparables} ({len(equipos_no_operativos_list)} en lista)")
    print(f"   [OK] Equipos en RMA: {equipos_rma} ({len(equipos_rma_list)} en lista)")
    print(f"   [OK] Equipos pendientes por parte: {len(equipos_pendientes_list)}")
    print(f"   [OK] Resumen de partes: {len(resumen_partes)}")
    
    # Calcular tasa de reparacion
    tasa_reparacion = (equipos_reparados / equipos_recibidos * 100) if equipos_recibidos > 0 else 0
    
    # Generar documento
    print("\n[4] Generando documento Word...")
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Guardar en output para prueba
        output_dir = Path("output/test")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "seccion_5_test.docx"
        gen.guardar(output_path)
        print(f"   [OK] Guardado en: {output_path}")
        
        # Verificar estructura del documento
        print("\n[5] Verificando estructura del documento...")
        print(f"   [OK] Paragrafos: {len(doc.paragraphs)}")
        print(f"   [OK] Tablas: {len(doc.tables)}")
        
        # Contar secciones
        secciones = [p.text for p in doc.paragraphs if p.style.name.startswith('Heading')]
        print(f"   [OK] Secciones encontradas: {len(secciones)}")
        for i, seccion in enumerate(secciones[:6], 1):  # Mostrar primeras 6
            print(f"      {i}. {seccion[:60]}...")
        
    except Exception as e:
        print(f"   [ERROR] Error al generar: {e}")
        import traceback
        traceback.print_exc()
    
    # Resumen
    print("\n" + "=" * 70)
    print("ESTADISTICAS DEL PERIODO:")
    print("=" * 70)
    mes = gen.datos.get('mes', 'Septiembre')
    anio = gen.datos.get('anio', 2025)
    print(f"   Periodo: {mes} {anio}")
    print(f"   Equipos recibidos en laboratorio: {equipos_recibidos}")
    print(f"   Equipos reparados exitosamente: {equipos_reparados}")
    print(f"   Equipos no reparables: {equipos_no_reparables}")
    print(f"   Equipos en proceso RMA: {equipos_rma}")
    print(f"   Tasa de exito en reparacion: {tasa_reparacion:.1f}%")
    print(f"   Equipos pendientes por repuesto: {len(equipos_pendientes_list)}")
    print("=" * 70)
    print("[OK] PRUEBA COMPLETADA")
    print("=" * 70)

if __name__ == "__main__":
    test_seccion5()

