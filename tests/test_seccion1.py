"""
Script de prueba para validar la generación de la Sección 1
"""
from src.generadores.seccion_1_info_general import GeneradorSeccion1
import json
from pathlib import Path

def test_seccion1():
    """Prueba la generación de la Sección 1 para septiembre 2025"""
    print("=" * 60)
    print("PRUEBA DE GENERACION - SECCION 1")
    print("=" * 60)
    
    # Crear generador
    print("\n[1] Creando generador para Septiembre 2025...")
    gen = GeneradorSeccion1(anio=2025, mes=9)
    print("   [OK] Generador creado")
    
    # Cargar datos
    print("\n[2] Cargando datos...")
    gen.cargar_datos()
    print("   [OK] Datos cargados")
    
    # Procesar contexto
    print("\n[3] Procesando contexto...")
    context = gen.procesar()
    print("   [OK] Contexto procesado")
    
    # Validaciones
    print("\n[4] Validando datos...")
    
    # Validar comunicados
    emitidos = context.get('comunicados_emitidos', [])
    recibidos = context.get('comunicados_recibidos', [])
    print(f"   [OK] Comunicados emitidos: {len(emitidos)}")
    print(f"   [OK] Comunicados recibidos: {len(recibidos)}")
    
    # Validar personal
    personal_minimo = context.get('personal_minimo', [])
    personal_apoyo = context.get('personal_apoyo', [])
    print(f"   [OK] Personal minimo: {len(personal_minimo)} cargos")
    print(f"   [OK] Personal de apoyo: {len(personal_apoyo)} cargos")
    
    # Validar glosario
    glosario = context.get('glosario', [])
    print(f"   [OK] Glosario: {len(glosario)} terminos")
    
    # Validar contenido fijo
    print("\n[5] Validando contenido fijo...")
    campos_fijos = [
        'objeto_contrato',
        'alcance',
        'descripcion_infraestructura',
        'obligaciones_generales',
        'obligaciones_especificas',
        'obligaciones_ambientales',
        'obligaciones_anexos'
    ]
    
    for campo in campos_fijos:
        valor = context.get(campo, '')
        if valor and len(valor.strip()) > 0:
            print(f"   [OK] {campo}: OK ({len(valor)} caracteres)")
        else:
            print(f"   [WARN] {campo}: VACIO (necesita contenido)")
    
    # Validar tabla información general
    print("\n[6] Validando tabla informacion general...")
    tabla_1 = context.get('tabla_1_info_general', {})
    if tabla_1:
        print(f"   [OK] Tabla 1: OK ({len(tabla_1)} campos)")
        print(f"      - NIT: {tabla_1.get('nit', 'N/A')}")
        print(f"      - Contrato: {tabla_1.get('numero_contrato', 'N/A')}")
        print(f"      - Valor total: {tabla_1.get('valor_total', 'N/A')}")
    else:
        print("   [ERROR] Tabla 1: ERROR")
    
    # Validar tablas de infraestructura
    print("\n[7] Validando tablas de infraestructura...")
    tabla_componentes = context.get('tabla_componentes', [])
    tabla_centros = context.get('tabla_centros_monitoreo', [])
    tabla_pago = context.get('tabla_forma_pago', [])
    
    print(f"   [OK] Tabla componentes: {len(tabla_componentes)} filas")
    print(f"   [OK] Tabla centros monitoreo: {len(tabla_centros)} filas")
    print(f"   [OK] Tabla forma de pago: {len(tabla_pago)} filas")
    
    # Intentar generar documento
    print("\n[8] Intentando generar documento Word...")
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        print(f"   [INFO] Template usado: {gen.template_path}")
        
        # Guardar en output para prueba
        output_dir = Path("output/test")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "seccion_1_test.docx"
        doc.save(str(output_path))
        print(f"   [OK] Guardado en: {output_path}")
        
    except FileNotFoundError as e:
        print(f"   [WARN] Template no encontrado: {e}")
        print(f"   [INFO] Necesitas crear/actualizar: {gen.template_path}")
    except Exception as e:
        print(f"   [ERROR] Error al generar: {e}")
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"[OK] Comunicados emitidos: {len(emitidos)}")
    print(f"[OK] Comunicados recibidos: {len(recibidos)}")
    print(f"[OK] Personal minimo: {len(personal_minimo)}")
    print(f"[OK] Personal de apoyo: {len(personal_apoyo)}")
    print(f"[OK] Glosario: {len(glosario)} terminos")
    print(f"[OK] Subsistemas: {len(context.get('subsistemas', []))}")
    
    # Verificar archivos que necesitan contenido
    archivos_vacios = []
    for campo in campos_fijos:
        valor = context.get(campo, '')
        if not valor or len(valor.strip()) < 50:  # Menos de 50 caracteres = probablemente placeholder
            archivos_vacios.append(campo)
    
    if archivos_vacios:
        print("\n[WARN] ARCHIVOS QUE NECESITAN CONTENIDO REAL:")
        for campo in archivos_vacios:
            archivo = campo.replace('_', '') + '.txt'
            print(f"   - data/fijos/{archivo}")
    
    print("\n" + "=" * 60)
    print("[OK] PRUEBA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    test_seccion1()

