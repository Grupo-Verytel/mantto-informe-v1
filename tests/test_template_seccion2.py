"""
Script de prueba para validar el template de Sección 2
"""
from pathlib import Path
import config
from docxtpl import DocxTemplate

def test_template():
    template_path = config.TEMPLATES_DIR / "seccion_2_mesa_servicio.docx"
    
    if not template_path.exists():
        print(f"[ERROR] Template no encontrado: {template_path}")
        return
    
    print(f"[INFO] Template encontrado: {template_path}")
    
    # Crear contexto de prueba
    contexto = {
        "mes": "Noviembre",
        "anio": 2025,
        "mes_numero": 11
    }
    
    print(f"[INFO] Contexto de prueba: {contexto}")
    
    # Cargar y renderizar template
    try:
        template = DocxTemplate(str(template_path))
        print(f"[INFO] Template cargado exitosamente")
        
        template.render(contexto)
        print(f"[INFO] Template renderizado exitosamente")
        
        # Guardar resultado
        output_path = config.OUTPUT_DIR / "seccion_2" / "test_template.docx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        doc = template.get_docx()
        doc.save(str(output_path))
        print(f"[OK] Documento de prueba guardado en: {output_path}")
        print(f"[INFO] Abre el archivo y verifica que {{mes}} y {{anio}} se hayan reemplazado")
        
    except Exception as e:
        print(f"[ERROR] Error al procesar template: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_template()

