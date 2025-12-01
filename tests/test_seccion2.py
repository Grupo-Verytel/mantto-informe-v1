"""
Script de prueba para validar la generacion de la Seccion 2
"""
from src.generadores.seccion_2_mesa_servicio import GeneradorSeccion2
from pathlib import Path

def test_seccion2():
    """Prueba la generacion de la Seccion 2 para septiembre 2025"""
    print("=" * 60)
    print("PRUEBA DE GENERACION - SECCION 2")
    print("=" * 60)
    
    # Crear generador
    print("\n[1] Creando generador para Septiembre 2025...")
    gen = GeneradorSeccion2(anio=2025, mes=9)
    print("   [OK] Generador creado")
    
    # Cargar datos
    print("\n[2] Cargando datos...")
    gen.cargar_datos()
    print("   [OK] Datos cargados")
    
    # Verificar datos cargados
    print("\n[3] Validando datos cargados...")
    
    total_tickets = gen.datos.get('total_tickets', 0)
    tickets_por_proyecto = gen.datos.get('tickets_por_proyecto', [])
    tickets_por_estado = gen.datos.get('tickets_por_estado', [])
    tickets_por_subsistema = gen.datos.get('tickets_por_subsistema', [])
    escalamientos_enel = gen.datos.get('escalamientos_enel', 0)
    escalamientos_conectividad = gen.datos.get('escalamientos_conectividad', 0)
    visitas_diagnostico = gen.datos.get('visitas_diagnostico', [])
    hojas_vida = gen.datos.get('hojas_vida', [])
    estado_sistema = gen.datos.get('estado_sistema', {})
    estado_por_localidad = gen.datos.get('estado_por_localidad', [])
    
    print(f"   [OK] Total tickets: {total_tickets}")
    print(f"   [OK] Tickets por proyecto: {len(tickets_por_proyecto)}")
    print(f"   [OK] Tickets por estado: {len(tickets_por_estado)}")
    print(f"   [OK] Tickets por subsistema: {len(tickets_por_subsistema)}")
    print(f"   [OK] Escalamientos ENEL: {escalamientos_enel}")
    print(f"   [OK] Escalamientos conectividad: {escalamientos_conectividad}")
    print(f"   [OK] Visitas diagnostico: {len(visitas_diagnostico)}")
    print(f"   [OK] Hojas de vida: {len(hojas_vida)}")
    print(f"   [OK] Estado sistema: {estado_sistema.get('total', 0)} camaras")
    print(f"   [OK] Estado por localidad: {len(estado_por_localidad)} localidades")
    
    # Verificar datos del extractor GLPI
    print("\n[4] Verificando extractor GLPI...")
    glpi = gen.glpi_extractor
    
    tickets_proyecto_glpi = glpi.get_tickets_por_proyecto(9, 2025)
    tickets_estado_glpi = glpi.get_tickets_por_estado(9, 2025)
    tickets_subsistema_glpi = glpi.get_tickets_por_subsistema(9, 2025)
    escalamientos_enel_glpi = glpi.get_escalamientos_enel(9, 2025)
    escalamientos_conectividad_glpi = glpi.get_escalamientos_conectividad(9, 2025)
    
    print(f"   [OK] GLPI - Tickets por proyecto: {len(tickets_proyecto_glpi)}")
    print(f"   [OK] GLPI - Tickets por estado: {len(tickets_estado_glpi)}")
    print(f"   [OK] GLPI - Tickets por subsistema: {len(tickets_subsistema_glpi)}")
    print(f"   [OK] GLPI - Escalamientos ENEL: {len(escalamientos_enel_glpi)}")
    print(f"   [OK] GLPI - Escalamientos conectividad: {len(escalamientos_conectividad_glpi)}")
    
    # Generar documento
    print("\n[5] Generando documento Word...")
    try:
        doc = gen.generar()
        print("   [OK] Documento generado exitosamente")
        
        # Guardar en output para prueba
        output_dir = Path("output/test")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "seccion_2_test.docx"
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
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"[OK] Total tickets: {total_tickets}")
    print(f"[OK] Tickets cerrados: {gen.datos.get('tickets_cerrados', 0)}")
    print(f"[OK] Tasa de cierre: {gen.datos.get('tasa_cierre', 0):.1f}%")
    print(f"[OK] Escalamientos ENEL: {escalamientos_enel}")
    print(f"[OK] Escalamientos conectividad: {escalamientos_conectividad}")
    print(f"[OK] Visitas diagnostico: {len(visitas_diagnostico)}")
    print(f"[OK] Hojas de vida: {len(hojas_vida)}")
    print(f"[OK] Disponibilidad sistema: {estado_sistema.get('porcentaje_operativas', 0):.2f}%")
    
    print("\n" + "=" * 60)
    print("[OK] PRUEBA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    test_seccion2()

