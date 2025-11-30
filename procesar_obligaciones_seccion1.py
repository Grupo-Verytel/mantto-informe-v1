"""
Script para procesar obligaciones de la sección 1 y generar observaciones dinámicamente
"""
import sys
from pathlib import Path
import logging
from src.services.obligaciones_service import ObligacionesService
import config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Función principal"""
    # Parámetros por defecto
    anio = 2025
    mes = 9  # Septiembre
    
    # Permitir pasar parámetros desde línea de comandos
    if len(sys.argv) > 1:
        anio = int(sys.argv[1])
    if len(sys.argv) > 2:
        mes = int(sys.argv[2])
    
    logger.info("=" * 80)
    logger.info(f"PROCESANDO OBLIGACIONES - {config.MESES[mes]} {anio}")
    logger.info("=" * 80)
    
    # Crear servicio
    service = ObligacionesService()
    
    # Procesar todas las obligaciones
    try:
        obligaciones_procesadas = service.procesar_todas_las_obligaciones(
            anio=anio,
            mes=mes,
            regenerar_todas=False  # Solo regenerar las que tienen regenerar_observacion=True
        )
        
        # Guardar resultados
        archivo_guardado = service.guardar_obligaciones_procesadas(
            obligaciones_procesadas,
            anio=anio,
            mes=mes,
            crear_backup=True
        )
        
        logger.info("=" * 80)
        logger.info("PROCESO COMPLETADO")
        logger.info("=" * 80)
        logger.info(f"Archivo guardado: {archivo_guardado}")
        
        # Resumen
        total_generales = len(obligaciones_procesadas.get("obligaciones_generales", []))
        total_especificas = len(obligaciones_procesadas.get("obligaciones_especificas", []))
        total_ambientales = len(obligaciones_procesadas.get("obligaciones_ambientales", []))
        total_anexos = len(obligaciones_procesadas.get("obligaciones_anexos", []))
        
        logger.info(f"\nResumen:")
        logger.info(f"  - Obligaciones Generales: {total_generales}")
        logger.info(f"  - Obligaciones Específicas: {total_especificas}")
        logger.info(f"  - Obligaciones Ambientales: {total_ambientales}")
        logger.info(f"  - Obligaciones de Anexos: {total_anexos}")
        
        # Contar observaciones generadas
        observaciones_generadas = 0
        for tipo in ["obligaciones_generales", "obligaciones_especificas", 
                     "obligaciones_ambientales", "obligaciones_anexos"]:
            for obligacion in obligaciones_procesadas.get(tipo, []):
                if obligacion.get("observaciones"):
                    observaciones_generadas += 1
        
        logger.info(f"  - Observaciones generadas: {observaciones_generadas}")
        
    except Exception as e:
        logger.error(f"Error al procesar obligaciones: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

