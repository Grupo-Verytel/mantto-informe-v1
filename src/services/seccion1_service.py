"""
Service para generar la sección 1 del informe desde MongoDB
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
from src.generadores.seccion_1_info_general import GeneradorSeccion1
from src.repositories.obligaciones_repository import ObligacionesRepository
from src.repositories.comunicados_repository import ComunicadosRepository
import config

logger = logging.getLogger(__name__)


class Seccion1Service:
    """Service para generar la sección 1 del informe"""
    
    def __init__(self):
        self.obligaciones_repo = ObligacionesRepository()
        self.comunicados_repo = ComunicadosRepository()
    
    async def cargar_datos_desde_mongodb(
        self,
        anio: int,
        mes: int,
        generador: GeneradorSeccion1
    ) -> None:
        """
        Carga datos desde MongoDB y los asigna al generador
        
        Args:
            anio: Año del informe
            mes: Mes del informe
            generador: Instancia del generador de sección 1
        """
        try:
            # Cargar obligaciones desde MongoDB
            # Buscar todas las subsecciones de obligaciones (1.5.1, 1.5.2, 1.5.3, 1.5.4)
            obligaciones_doc = await self.obligaciones_repo.obtener_obligaciones(
                anio=anio,
                mes=mes,
                seccion=1,
                subseccion=None  # Obtener todas las subsecciones
            )
            
            if obligaciones_doc:
                # Las obligaciones se guardan con las claves: obligaciones_generales, obligaciones_especificas, etc.
                generador.obligaciones_generales_raw = obligaciones_doc.get("obligaciones_generales", [])
                generador.obligaciones_especificas_raw = obligaciones_doc.get("obligaciones_especificas", [])
                generador.obligaciones_ambientales_raw = obligaciones_doc.get("obligaciones_ambientales", [])
                generador.obligaciones_anexos_raw = obligaciones_doc.get("obligaciones_anexos", [])
                logger.info(f"Datos de obligaciones cargados desde MongoDB: "
                          f"generales={len(generador.obligaciones_generales_raw)}, "
                          f"especificas={len(generador.obligaciones_especificas_raw)}, "
                          f"ambientales={len(generador.obligaciones_ambientales_raw)}, "
                          f"anexos={len(generador.obligaciones_anexos_raw)}")
            else:
                logger.warning(f"No se encontraron obligaciones en MongoDB para {anio}-{mes}")
                # Intentar cargar por subsecciones individuales si no hay documento consolidado
                logger.info("Intentando cargar obligaciones por subsecciones individuales...")
                
                # Cargar obligaciones generales (1.5.1)
                doc_1_5_1 = await self.obligaciones_repo.obtener_obligaciones(anio, mes, 1, "1.5.1")
                if doc_1_5_1:
                    generador.obligaciones_generales_raw = doc_1_5_1.get("obligaciones_generales", [])
                
                # Cargar obligaciones específicas (1.5.2)
                doc_1_5_2 = await self.obligaciones_repo.obtener_obligaciones(anio, mes, 1, "1.5.2")
                if doc_1_5_2:
                    generador.obligaciones_especificas_raw = doc_1_5_2.get("obligaciones_especificas", [])
                
                # Cargar obligaciones ambientales (1.5.3)
                doc_1_5_3 = await self.obligaciones_repo.obtener_obligaciones(anio, mes, 1, "1.5.3")
                if doc_1_5_3:
                    generador.obligaciones_ambientales_raw = doc_1_5_3.get("obligaciones_ambientales", [])
                
                # Cargar obligaciones anexos (1.5.4)
                doc_1_5_4 = await self.obligaciones_repo.obtener_obligaciones(anio, mes, 1, "1.5.4")
                if doc_1_5_4:
                    generador.obligaciones_anexos_raw = doc_1_5_4.get("obligaciones_anexos", [])
            
            # Cargar comunicados emitidos desde MongoDB (subsección 1.6.1)
            comunicados_emitidos_doc = await self.comunicados_repo.obtener_comunicados(
                anio=anio,
                mes=mes,
                seccion=1,
                subseccion="1.6.1"
            )
            
            if comunicados_emitidos_doc:
                comunicados_emitidos = comunicados_emitidos_doc.get("comunicados_emitidos", [])
                # Convertir formato de MongoDB al formato esperado por el generador
                generador.comunicados_emitidos = [
                    {
                        "numero": com.get("radicado", ""),
                        "fecha": com.get("fecha", ""),
                        "asunto": com.get("asunto", ""),
                        "adjuntos": com.get("nombre_archivo", "")
                    }
                    for com in comunicados_emitidos
                ]
                logger.info(f"Comunicados emitidos cargados desde MongoDB: {len(generador.comunicados_emitidos)}")
            else:
                logger.warning(f"No se encontraron comunicados emitidos en MongoDB para {anio}-{mes}")
            
            # Cargar comunicados recibidos desde MongoDB (subsección 1.6.2)
            comunicados_recibidos_doc = await self.comunicados_repo.obtener_comunicados(
                anio=anio,
                mes=mes,
                seccion=1,
                subseccion="1.6.2"
            )
            
            if comunicados_recibidos_doc:
                comunicados_recibidos = comunicados_recibidos_doc.get("comunicados_recibidos", [])
                # Convertir formato de MongoDB al formato esperado por el generador
                generador.comunicados_recibidos = [
                    {
                        "numero": com.get("radicado", ""),
                        "fecha": com.get("fecha", ""),
                        "asunto": com.get("asunto", ""),
                        "adjuntos": com.get("nombre_archivo", "")
                    }
                    for com in comunicados_recibidos
                ]
                logger.info(f"Comunicados recibidos cargados desde MongoDB: {len(generador.comunicados_recibidos)}")
            else:
                logger.warning(f"No se encontraron comunicados recibidos en MongoDB para {anio}-{mes}")
                
        except Exception as e:
            logger.error(f"Error al cargar datos desde MongoDB: {e}")
            import traceback
            traceback.print_exc()
    
    async def generar_seccion1(
        self,
        anio: int,
        mes: int,
        usar_llm_observaciones: bool = False,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Genera el documento de la sección 1 desde MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            usar_llm_observaciones: Si True, usa LLM para generar observaciones (por defecto False, usa las de MongoDB)
            output_path: Ruta donde guardar el documento. Si None, usa directorio de salida por defecto
            
        Returns:
            Path al archivo generado
        """
        # Crear generador con carga desde MongoDB
        generador = GeneradorSeccion1(
            anio=anio,
            mes=mes,
            usar_llm_observaciones=usar_llm_observaciones,
            cargar_desde_mongodb=True
        )
        
        # Cargar datos desde MongoDB
        await self.cargar_datos_desde_mongodb(anio, mes, generador)
        
        # Determinar ruta de salida
        if output_path is None:
            output_path = config.OUTPUT_DIR / f"seccion_1_{anio}_{mes:02d}.docx"
        
        # Asegurar que el directorio existe
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generar y guardar el documento
        generador.guardar(output_path)
        
        logger.info(f"Sección 1 generada exitosamente en: {output_path}")
        return output_path

