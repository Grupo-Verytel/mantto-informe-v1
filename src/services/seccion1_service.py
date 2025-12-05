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
            # Cargar obligaciones desde MongoDB por subsecciones individuales
            # Siempre filtrar por anio, mes, seccion y subseccion
            logger.info(f"Cargando obligaciones desde MongoDB para {anio}-{mes}, sección 1...")
            
            # Cargar obligaciones generales (1.5.1)
            doc_1_5_1 = await self.obligaciones_repo.obtener_obligaciones(anio, mes, 1, "1.5.1")
            if doc_1_5_1:
                generador.obligaciones_generales_raw = doc_1_5_1.get("obligaciones_generales", [])
                logger.info(f"Obligaciones generales (1.5.1) cargadas: {len(generador.obligaciones_generales_raw)} elementos")
            else:
                logger.warning(f"No se encontraron obligaciones generales (1.5.1) para {anio}-{mes}")
                generador.obligaciones_generales_raw = []
            
            # Cargar obligaciones específicas (1.5.2)
            doc_1_5_2 = await self.obligaciones_repo.obtener_obligaciones(anio, mes, 1, "1.5.2")
            if doc_1_5_2:
                generador.obligaciones_especificas_raw = doc_1_5_2.get("obligaciones_especificas", [])
                logger.info(f"Obligaciones específicas (1.5.2) cargadas: {len(generador.obligaciones_especificas_raw)} elementos")
            else:
                logger.warning(f"No se encontraron obligaciones específicas (1.5.2) para {anio}-{mes}")
                generador.obligaciones_especificas_raw = []
            
            # Cargar obligaciones ambientales (1.5.3)
            doc_1_5_3 = await self.obligaciones_repo.obtener_obligaciones(anio, mes, 1, "1.5.3")
            if doc_1_5_3:
                generador.obligaciones_ambientales_raw = doc_1_5_3.get("obligaciones_ambientales", [])
                logger.info(f"Obligaciones ambientales (1.5.3) cargadas: {len(generador.obligaciones_ambientales_raw)} elementos")
            else:
                logger.warning(f"No se encontraron obligaciones ambientales (1.5.3) para {anio}-{mes}")
                generador.obligaciones_ambientales_raw = []
            
            # Cargar obligaciones anexos (1.5.4)
            doc_1_5_4 = await self.obligaciones_repo.obtener_obligaciones(anio, mes, 1, "1.5.4")
            if doc_1_5_4:
                obligaciones_anexos_raw = doc_1_5_4.get("obligaciones_anexos", [])
                logger.info(f"Datos raw de obligaciones_anexos: {obligaciones_anexos_raw}")
                
                # Para 1.5.4, procesar según el formato
                generador.obligaciones_anexos_raw = []
                for idx, anexo in enumerate(obligaciones_anexos_raw, start=1):
                    if isinstance(anexo, dict):
                        if "archivo_existe" in anexo:
                            # Formato simple: archivo_existe y anexo
                            if anexo.get("archivo_existe", False):
                                # Si el archivo existe, mostrar la ruta
                                ruta = anexo.get("anexo", "Archivo encontrado")
                                generador.obligaciones_anexos_raw.append({
                                    "item": idx,
                                    "obligacion": "Verificación de archivo anexo",
                                    "periodicidad": "Mensual",
                                    "cumplio": "Cumplió",
                                    "observaciones": f"Archivo encontrado: {ruta}",
                                    "anexo": ruta  # Mostrar la ruta completa
                                })
                            else:
                                # Si no existe, mostrar mensaje
                                generador.obligaciones_anexos_raw.append({
                                    "item": idx,
                                    "obligacion": "Verificación de archivo anexo",
                                    "periodicidad": "Mensual",
                                    "cumplio": "No Cumplió",
                                    "observaciones": "Archivo no encontrado",
                                    "anexo": "Archivo no encontrado"
                                })
                        else:
                            # Formato estándar de obligaciones (ya tiene item, obligacion, etc.)
                            generador.obligaciones_anexos_raw.append(anexo)
                    else:
                        # Si no es dict, crear estructura básica
                        generador.obligaciones_anexos_raw.append({
                            "item": idx,
                            "obligacion": str(anexo),
                            "periodicidad": "",
                            "cumplio": "",
                            "observaciones": "",
                            "anexo": str(anexo)
                        })
                logger.info(f"Obligaciones anexos (1.5.4) cargadas: {len(generador.obligaciones_anexos_raw)} elementos")
            else:
                logger.warning(f"No se encontraron obligaciones anexos (1.5.4) para {anio}-{mes}")
                generador.obligaciones_anexos_raw = []
            
            logger.info(f"Resumen de obligaciones cargadas: "
                      f"generales={len(generador.obligaciones_generales_raw)}, "
                      f"especificas={len(generador.obligaciones_especificas_raw)}, "
                      f"ambientales={len(generador.obligaciones_ambientales_raw)}, "
                      f"anexos={len(generador.obligaciones_anexos_raw)}")
            
            # Cargar comunicados emitidos desde MongoDB (subsección 1.6.1)
            # Filtrar por anio, mes, seccion=1, subseccion=1.6.1
            logger.info(f"Cargando comunicados emitidos desde MongoDB para {anio}-{mes}, sección 1, subsección 1.6.1...")
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
                        "item": com.get("item", idx + 1),
                        "numero": com.get("radicado", ""),
                        "fecha": com.get("fecha", ""),
                        "asunto": com.get("asunto", ""),
                        "adjuntos": com.get("nombre_archivo", "")
                    }
                    for idx, com in enumerate(comunicados_emitidos)
                ]
                logger.info(f"Comunicados emitidos (1.6.1) cargados: {len(generador.comunicados_emitidos)} elementos")
            else:
                logger.warning(f"No se encontraron comunicados emitidos (1.6.1) en MongoDB para {anio}-{mes}")
                generador.comunicados_emitidos = []
            
            # Cargar comunicados recibidos desde MongoDB (subsección 1.6.2)
            # Filtrar por anio, mes, seccion=1, subseccion=1.6.2
            logger.info(f"Cargando comunicados recibidos desde MongoDB para {anio}-{mes}, sección 1, subsección 1.6.2...")
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
                        "item": com.get("item", idx + 1),
                        "numero": com.get("radicado", ""),
                        "fecha": com.get("fecha", ""),
                        "asunto": com.get("asunto", ""),
                        "adjuntos": com.get("nombre_archivo", "")
                    }
                    for idx, com in enumerate(comunicados_recibidos)
                ]
                logger.info(f"Comunicados recibidos (1.6.2) cargados: {len(generador.comunicados_recibidos)} elementos")
            else:
                logger.warning(f"No se encontraron comunicados recibidos (1.6.2) en MongoDB para {anio}-{mes}")
                generador.comunicados_recibidos = []
                
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

