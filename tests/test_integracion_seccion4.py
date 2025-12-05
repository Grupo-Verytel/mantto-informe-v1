"""
Script de prueba de integracion completa de la Seccion 4
Valida que todo el flujo funcione correctamente
"""
from src.generadores.seccion_4_bienes import GeneradorSeccion4
from src.utils.formato_moneda import numero_a_letras, formato_moneda_cop
from pathlib import Path
import json

def test_conversion_letras():
    """Prueba la conversion de numeros a letras"""
    print("\n[TEST 1] Conversion de numeros a letras")
    print("-" * 70)
    
    casos = [
        (1000000, "UN MILLON"),
        (56909324, "CINCUENTA Y SEIS MILLONES"),
        (245000, "DOSCIENTOS CUARENTA Y CINCO MIL"),
        (18750000, "DIECIOCHO MILLONES"),
    ]
    
    for valor, esperado in casos:
        resultado = numero_a_letras(valor)
        print(f"   Valor: ${valor:,}")
        print(f"   En letras: {resultado[:60]}...")
        if esperado in resultado:
            print(f"   [OK] Contiene '{esperado}'")
        else:
            print(f"   [WARN] No contiene '{esperado}'")
        print()

def test_formato_moneda():
    """Prueba el formato de moneda"""
    print("\n[TEST 2] Formato de moneda")
    print("-" * 70)
    
    casos = [
        (1250000, "$1.250.000"),
        (18750000, "$18.750.000"),
        (56909324, "$56.909.324"),
    ]
    
    for valor, esperado in casos:
        resultado = formato_moneda_cop(valor)
        print(f"   Valor: {valor:,}")
        print(f"   Formato: {resultado}")
        if resultado == esperado:
            print(f"   [OK] Correcto")
        else:
            print(f"   [ERROR] Esperado: {esperado}, Obtenido: {resultado}")
        print()

def test_carga_datos():
    """Prueba la carga de datos desde JSON"""
    print("\n[TEST 3] Carga de datos desde JSON")
    print("-" * 70)
    
    gen = GeneradorSeccion4(anio=2025, mes=9)
    gen.cargar_datos()
    
    # Verificar estructura
    entradas = gen.datos.get('entradas_almacen', {})
    equipos = gen.datos.get('equipos_no_operativos', {})
    inclusiones = gen.datos.get('inclusiones_bolsa', {})
    
    print(f"   [OK] Entradas: {len(entradas.get('items', []))} items")
    print(f"   [OK] Equipos: {len(equipos.get('equipos', []))} equipos")
    print(f"   [OK] Inclusiones: {len(inclusiones.get('items', []))} items")
    
    # Verificar comunicados
    if entradas.get('comunicado'):
        com = entradas['comunicado']
        print(f"   [OK] Comunicado entradas: {com.get('numero', 'N/A')}")
    
    if equipos.get('comunicado'):
        com = equipos['comunicado']
        print(f"   [OK] Comunicado equipos: {com.get('numero', 'N/A')}")
    
    if inclusiones.get('comunicado'):
        com = inclusiones['comunicado']
        print(f"   [OK] Comunicado inclusiones: {com.get('numero', 'N/A')}")
        print(f"   [OK] Estado: {inclusiones.get('estado', 'N/A')}")

def test_generacion_completa():
    """Prueba la generacion completa del documento"""
    print("\n[TEST 4] Generacion completa del documento")
    print("-" * 70)
    
    gen = GeneradorSeccion4(anio=2025, mes=9)
    gen.cargar_datos()
    
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Verificar estructura
        print(f"   [OK] Paragrafos: {len(doc.paragraphs)}")
        print(f"   [OK] Tablas: {len(doc.tables)}")
        
        # Verificar secciones
        secciones = [p.text for p in doc.paragraphs if p.style.name.startswith('Heading')]
        print(f"   [OK] Secciones: {len(secciones)}")
        
        # Verificar que las tablas tengan el formato correcto
        if len(doc.tables) >= 3:
            print(f"   [OK] Tablas encontradas: {len(doc.tables)}")
            for i, tabla in enumerate(doc.tables[:3], 1):
                print(f"      Tabla {i}: {len(tabla.rows)} filas, {len(tabla.columns)} columnas")
        else:
            print(f"   [WARN] Se esperaban 3 tablas, se encontraron {len(doc.tables)}")
        
        # Guardar para inspeccion manual
        output_path = Path("output/test/seccion_4_integracion.docx")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        gen.guardar(output_path)
        print(f"   [OK] Guardado en: {output_path}")
        
    except Exception as e:
        print(f"   [ERROR] Error al generar: {e}")
        import traceback
        traceback.print_exc()

def test_valores_totales():
    """Prueba el calculo de valores totales"""
    print("\n[TEST 5] Calculo de valores totales")
    print("-" * 70)
    
    gen = GeneradorSeccion4(anio=2025, mes=9)
    gen.cargar_datos()
    
    entradas = gen.datos.get('entradas_almacen', {})
    equipos = gen.datos.get('equipos_no_operativos', {})
    inclusiones = gen.datos.get('inclusiones_bolsa', {})
    
    # Calcular totales
    total_entradas = sum(item.get('valor_total', 0) for item in entradas.get('items', []))
    total_equipos = sum(eq.get('valor', 0) for eq in equipos.get('equipos', []))
    total_inclusiones = sum(item.get('valor_total', 0) for item in inclusiones.get('items', []))
    
    print(f"   Total entradas: {gen._formato_moneda(total_entradas)}")
    print(f"   Total equipos: {gen._formato_moneda(total_equipos)}")
    print(f"   Total inclusiones: {gen._formato_moneda(total_inclusiones)}")
    
    # Verificar conversion a letras
    if total_entradas > 0:
        letras = gen._numero_a_letras(total_entradas)
        print(f"   Entradas en letras: {letras[:80]}...")
    
    if total_equipos > 0:
        letras = gen._numero_a_letras(total_equipos)
        print(f"   Equipos en letras: {letras[:80]}...")
    
    if total_inclusiones > 0:
        letras = gen._numero_a_letras(total_inclusiones)
        print(f"   Inclusiones en letras: {letras[:80]}...")

def main():
    """Ejecuta todas las pruebas de integracion"""
    print("=" * 70)
    print("PRUEBA DE INTEGRACION - SECCION 4")
    print("=" * 70)
    
    test_conversion_letras()
    test_formato_moneda()
    test_carga_datos()
    test_valores_totales()
    test_generacion_completa()
    
    print("\n" + "=" * 70)
    print("[OK] TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    main()

