"""
Script de prueba para validar la generacion de la Seccion 3 (ANS)
SECCION CRITICA - Impacto contractual y financiero
"""
from src.generadores.seccion_3_ans import GeneradorSeccion3
from pathlib import Path

def test_seccion3():
    """Prueba la generacion de la Seccion 3 para septiembre 2025"""
    print("=" * 70)
    print("GENERADOR SECCION 3 - ANS (ACUERDOS DE NIVEL DE SERVICIO)")
    print("=" * 70)
    print("\nSECCION CRITICA - IMPACTO CONTRACTUAL")
    print(f"   Umbral ANS: 98.9%")
    print("=" * 70)
    
    # Crear generador
    print("\n[1] Generando documento para Septiembre 2025...")
    gen = GeneradorSeccion3(anio=2025, mes=9)
    
    # Cargar datos
    print("[2] Cargando datos...")
    gen.cargar_datos()
    print("   [OK] Datos cargados")
    
    # Verificar datos cargados
    print("\n[3] Validando datos cargados...")
    
    disponibilidad = gen.disponibilidad
    cumple_ans = gen.cumple_ans
    
    print(f"   [OK] Disponibilidad: {disponibilidad:.2f}%")
    print(f"   [OK] Umbral ANS: {gen.UMBRAL_ANS}%")
    estado_texto = "CUMPLE" if cumple_ans else "NO CUMPLE"
    print(f"   [OK] Estado: {estado_texto}")
    
    if not cumple_ans:
        penalidad = gen._calcular_penalidad()
        print(f"   [OK] Deficit: {penalidad['deficit']:.2f}%")
        print(f"   [OK] Penalidad: {penalidad['porcentaje_penalidad']:.1f}% del contrato")
        print(f"   [OK] Valor penalidad: ${penalidad['valor_penalidad']:,.0f} COP")
    
    total_camaras = gen.datos.get('total_camaras', 0)
    horas_totales = gen.datos.get('horas_totales', 0)
    horas_operativas = gen.datos.get('horas_operativas', 0)
    horas_no_operativas = gen.datos.get('horas_no_operativas', 0)
    localidades = gen.datos.get('disponibilidad_por_localidad', [])
    historico = gen.datos.get('historico_ans', [])
    
    print(f"   [OK] Total camaras: {total_camaras:,}")
    print(f"   [OK] Horas totales: {horas_totales:,}")
    print(f"   [OK] Horas operativas: {horas_operativas:,}")
    print(f"   [OK] Horas no operativas: {horas_no_operativas:,}")
    print(f"   [OK] Localidades: {len(localidades)}")
    print(f"   [OK] Historico: {len(historico)} meses")
    
    # Verificar calculo de disponibilidad
    print("\n[4] Verificando calculo de disponibilidad...")
    disponibilidad_calculada = (horas_operativas / horas_totales * 100) if horas_totales > 0 else 0
    print(f"   [OK] Disponibilidad calculada: {disponibilidad_calculada:.2f}%")
    print(f"   [OK] Disponibilidad en datos: {disponibilidad:.2f}%")
    
    if abs(disponibilidad_calculada - disponibilidad) < 0.01:
        print("   [OK] Calculo correcto")
    else:
        print("   [WARN] Diferencia en calculo")
    
    # Generar documento
    print("\n[5] Generando documento Word...")
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Guardar en output para prueba
        output_dir = Path("output/test")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "seccion_3_test.docx"
        gen.guardar(output_path)
        print(f"   [OK] Guardado en: {output_path}")
        
        # Verificar estructura del documento
        print("\n[6] Verificando estructura del documento...")
        print(f"   [OK] Paragrafos: {len(doc.paragraphs)}")
        print(f"   [OK] Tablas: {len(doc.tables)}")
        
        # Contar secciones
        secciones = [p.text for p in doc.paragraphs if p.style.name.startswith('Heading')]
        print(f"   [OK] Secciones encontradas: {len(secciones)}")
        for i, seccion in enumerate(secciones[:5], 1):  # Mostrar primeras 5
            print(f"      {i}. {seccion[:60]}...")
        
    except Exception as e:
        print(f"   [ERROR] Error al generar: {e}")
        import traceback
        traceback.print_exc()
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DEL PERIODO")
    print("=" * 70)
    mes = gen.datos.get('mes', 'Septiembre')
    anio = gen.datos.get('anio', 2025)
    print(f"   Periodo: {mes} {anio}")
    print(f"   Disponibilidad: {disponibilidad:.2f}%")
    print(f"   Umbral ANS: {gen.UMBRAL_ANS}%")
    estado_texto = "CUMPLE" if cumple_ans else "NO CUMPLE"
    print(f"   Estado: {estado_texto}")
    
    if not cumple_ans:
        penalidad = gen._calcular_penalidad()
        print(f"   Deficit: {penalidad['deficit']:.2f}%")
        print(f"   Penalidad: {penalidad['porcentaje_penalidad']:.1f}%")
        print(f"   Valor penalidad: ${penalidad['valor_penalidad']:,.0f} COP")
    
    print(f"   Total camaras: {total_camaras:,}")
    print(f"   Localidades evaluadas: {len(localidades)}")
    print(f"   Meses en historico: {len(historico)}")
    
    # Estadisticas del historico
    if historico:
        meses_cumplidos = sum(1 for h in historico if h.get('disponibilidad', 0) >= gen.UMBRAL_ANS)
        promedio = sum(h.get('disponibilidad', 0) for h in historico) / len(historico)
        print(f"   Meses cumplidos: {meses_cumplidos}/{len(historico)}")
        print(f"   Disponibilidad promedio: {promedio:.2f}%")
    
    print("=" * 70)
    print("[OK] PRUEBA COMPLETADA")
    print("=" * 70)

if __name__ == "__main__":
    test_seccion3()

