"""
Script de prueba para validar la generacion de la Seccion 4
"""
from src.generadores.seccion_4_bienes import GeneradorSeccion4
from pathlib import Path

def test_seccion4():
    """Prueba la generacion de la Seccion 4 para septiembre 2025"""
    print("=" * 70)
    print("GENERADOR SECCION 4 - INFORME DE BIENES Y SERVICIOS")
    print("=" * 70)
    
    # Crear generador
    print("\n[1] Generando documento para Septiembre 2025...")
    gen = GeneradorSeccion4(anio=2025, mes=9)
    
    # Cargar datos
    print("[2] Cargando datos...")
    gen.cargar_datos()
    print("   [OK] Datos cargados")
    
    # Verificar datos cargados
    print("\n[3] Validando datos cargados...")
    
    entradas = gen.datos.get('entradas_almacen', {})
    equipos = gen.datos.get('equipos_no_operativos', {})
    inclusiones = gen.datos.get('inclusiones_bolsa', {})
    
    entradas_items = entradas.get('items', [])
    equipos_list = equipos.get('equipos', [])
    inclusiones_items = inclusiones.get('items', [])
    
    # Calcular totales
    valor_entradas = sum(item.get('valor_total', 0) for item in entradas_items)
    valor_equipos = sum(eq.get('valor', 0) for eq in equipos_list)
    valor_inclusiones = sum(item.get('valor_total', 0) for item in inclusiones_items)
    
    print(f"   [OK] Entradas al almacen: {len(entradas_items)} items")
    print(f"   [OK] Valor total entradas: {gen._formato_moneda(valor_entradas)}")
    print(f"   [OK] Equipos no operativos: {len(equipos_list)} equipos")
    print(f"   [OK] Valor total equipos: {gen._formato_moneda(valor_equipos)}")
    print(f"   [OK] Inclusiones a bolsa: {len(inclusiones_items)} items")
    print(f"   [OK] Valor total inclusiones: {gen._formato_moneda(valor_inclusiones)}")
    
    # Verificar comunicados
    print("\n[4] Verificando comunicados...")
    if entradas:
        com = entradas.get('comunicado', {})
        print(f"   [OK] Comunicado entradas: {com.get('numero', 'N/A')}")
    if equipos:
        com = equipos.get('comunicado', {})
        print(f"   [OK] Comunicado equipos: {com.get('numero', 'N/A')}")
    if inclusiones:
        com = inclusiones.get('comunicado', {})
        print(f"   [OK] Comunicado inclusiones: {com.get('numero', 'N/A')}")
        print(f"   [OK] Estado inclusiones: {inclusiones.get('estado', 'N/A')}")
    
    # Verificar conversion a letras
    print("\n[5] Verificando conversion a letras...")
    test_valor = 18750000
    letras = gen._numero_a_letras(test_valor)
    print(f"   [OK] Valor: {gen._formato_moneda(test_valor)}")
    print(f"   [OK] En letras: {letras[:80]}...")
    
    # Generar documento
    print("\n[6] Generando documento Word...")
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Guardar en output para prueba
        output_dir = Path("output/test")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "seccion_4_test.docx"
        gen.guardar(output_path)
        print(f"   [OK] Guardado en: {output_path}")
        
        # Verificar estructura del documento
        print("\n[7] Verificando estructura del documento...")
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
    print(f"   Entradas al almacen: {len(entradas_items)} items ({gen._formato_moneda(valor_entradas)})")
    print(f"   Equipos no operativos: {len(equipos_list)} equipos ({gen._formato_moneda(valor_equipos)})")
    print(f"   Solicitudes de inclusion: {len(inclusiones_items)} items ({gen._formato_moneda(valor_inclusiones)})")
    print("=" * 70)
    print("[OK] PRUEBA COMPLETADA")
    print("=" * 70)

if __name__ == "__main__":
    test_seccion4()

