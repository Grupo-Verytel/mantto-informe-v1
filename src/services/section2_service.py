from typing import Dict, Any
from ..services.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from datetime import datetime
from ..data.repositories.build_section2 import get_section2, build_section2
from bson import ObjectId
from ..generadores.seccion_2_mesa_servicio import GeneradorSeccion2

logger = logging.getLogger(__name__)


class Section2Service:
    
    def __init__(self):
        self.collection_name = "section2"
    
    def _get_collection(self):
        db = get_database()
        return db[self.collection_name]
    
    async def send_data_section(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            section_id = data.get("section_id")
            content = data.get("content")
            user_id = data.get("user_id", 1)
            name_file = data.get("name_file", f"INFORME_MENSUAL_{mes}_{anio}_V1.docx")
            
            level = data.get("level", 2)
            title = data.get("title", section_id)
            
            collection = self._get_collection()
            datetime_now = datetime.now()
            
            document = await get_section2(anio, mes, user_id, name_file)
            
            if not document:
                return {
                    "success": False,
                    "message": f"No se pudo obtener o crear el documento para año {anio}, mes {mes}",
                    "data": None
                }
            
            section_exists = any(item.get("id") == section_id for item in document.get("index", []))
            
            # Verificar el estado actual de preloaded para esta sección
            preloaded_actual = False
            if section_exists:
                for item in document.get("index", []):
                    if item.get("id") == section_id:
                        preloaded_actual = item.get("preloaded", False)
                        break
            
            if section_exists:
                update_fields = {
                    "index.$.content": content,
                    "index.$.updated_at": datetime_now,
                    "updated_at": datetime_now
                }
                
                if "level" in data:
                    update_fields["index.$.level"] = level
                if "title" in data:
                    update_fields["index.$.title"] = title
                if "user_updated" in data:
                    update_fields["index.$.user_updated"] = user_id
                
                # Si preloaded es False, actualizarlo a True después de guardar exitosamente
                if not preloaded_actual:
                    update_fields["index.$.preloaded"] = True
                    logger.info(f"Actualizando preloaded a True para sección {section_id} después de guardar datos")
                
                result = await collection.update_one(
                    {
                        "anio": anio,
                        "mes": mes,
                        "index.id": section_id
                    },
                    {
                        "$set": update_fields
                    }
                )
                
                if result.modified_count == 0:
                    return {
                        "success": False,
                        "message": f"No se pudo actualizar la sección {section_id}",
                        "data": None
                    }
            else:
                # Nueva sección: marcar como precargada (True) ya que se está guardando con datos
                new_section = {
                    "id": section_id,
                    "level": level,
                    "title": title,
                    "content": content,
                    "preloaded": True,  # Marcar como True ya que se está guardando con datos procesados
                    "user_created": user_id,
                    "user_updated": user_id,
                    "created_at": datetime_now,
                    "updated_at": datetime_now
                }
                
                result = await collection.update_one(
                    {
                        "anio": anio,
                        "mes": mes
                    },
                    {
                        "$push": {
                            "index": new_section
                        },
                        "$set": {
                            "updated_at": datetime_now
                        }
                    }
                )
                
                if result.modified_count == 0:
                    return {
                        "success": False,
                        "message": f"No se pudo agregar la sección {section_id}",
                        "data": None
                    }
            
            return {
                "success": True,
                "message": f"Datos de la sección {section_id} guardados exitosamente",
                "data": {
                    "id": section_id,
                    "anio": anio,
                    "mes": mes,
                    "content": content
                }
            }
        except Exception as e:
            logger.error(f"Error al guardar datos de la sección: {str(e)}", exc_info=True)
            raise


    async def get_section_by_index(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            section_id = data.get("section_id")
            
            collection = self._get_collection()
            
            document = await collection.find_one({"anio": anio, "mes": mes})
            
            if not document:
                return {
                    "success": False,
                    "message": f"No se encontró el documento para año {anio}, mes {mes}",
                    "data": None
                }
            
            section_item = None
            for item in document.get("index", []):
                if item.get("id") == section_id:
                    section_item = item
                    break
            
            if not section_item:
                return {
                    "success": False,
                    "message": f"No se encontró la sección {section_id}",
                    "data": None
                }
            
            return {
                "success": True,
                "message": f"Sección {section_id} obtenida exitosamente",
                "data": section_item
            }
        except Exception as e:
            logger.error(f"Error al obtener sección por índice: {str(e)}", exc_info=True)
            raise
    
    async def get_all_section(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            anio = int(data.get("anio"))
            mes = int(data.get("mes"))
            user_id = int(data.get("user_id", 1))
            name_file = data.get("name_file", f"INFORME_MENSUAL_{mes}_{anio}_V1.docx")
            
            collection = self._get_collection()
            
            document = await collection.find_one({"anio": anio, "mes": mes})     
            if not document:
                await build_section2(anio, mes, user_id, name_file)
                document = await collection.find_one({"anio": anio, "mes": mes})
                
            document = self.serialize_mongo(document)

            if document and document.get("preloaded") == False:
                # Precargar todas las secciones usando el generador
                await self.preload_all_sections(anio, mes, user_id, name_file)
                # Actualizar el campo preloaded a True
                await collection.update_one(
                    {"anio": anio, "mes": mes},
                    {"$set": {"preloaded": True, "updated_at": datetime.now()}}
                )
                # Obtener el documento actualizado
                document = await collection.find_one({"anio": anio, "mes": mes})
                document = self.serialize_mongo(document)

            return document
        except Exception as e:
            logger.error(f"Error al obtener toda la sección: {str(e)}", exc_info=True)
            raise
    
    async def preload_all_sections(self, anio: int, mes: int, user_id: int = 1, name_file: str = None) -> Dict[str, Any]:
        """
        Precarga las secciones del módulo 2 que requieren llamados a SharePoint o GLPI usando el generador.
        Usa el método preload_seccion_2 del generador y luego guarda cada sección usando send_data_section.
        
        Args:
            anio: Año del informe
            mes: Mes del informe
            user_id: ID del usuario que realiza la operación
            name_file: Nombre del archivo
            
        Returns:
            Diccionario con el resultado de la precarga
        """
        resultados = {
            "success": True,
            "anio": anio,
            "mes": mes,
            "secciones_precargadas": [],
            "errores": []
        }
        
        try:
            logger.info(f"Iniciando precarga de secciones del módulo 2 para {anio}-{mes} usando el generador")
            
            collection = self._get_collection()
            generador = GeneradorSeccion2()
            
            # Obtener el documento completo para pasar los datos al generador
            document = await collection.find_one({"anio": anio, "mes": mes})
            if not document:
                logger.error(f"No se encontró el documento para {anio}-{mes}")
                resultados["success"] = False
                resultados["errores"].append(f"No se encontró el documento para {anio}-{mes}")
                return resultados
            
            # Preparar datos para el método preload_seccion_2 del generador
            preload_data = {
                "anio": anio,
                "mes": mes,
                "user_id": user_id,
                "name_file": name_file or f"INFORME_MENSUAL_{mes}_{anio}_V1.docx",
                "document": document  # Pasar el documento completo para que el generador pueda acceder al índice
            }
            
            # Llamar al método preload_seccion_2 del generador que procesa todas las secciones
            logger.info("Llamando al método preload_seccion_2 del generador...")
            secciones_procesadas = await generador.preload_seccion_2(preload_data)
            
            # Secciones que requieren precarga (solo las que hacen llamados a SharePoint/GLPI)
            secciones_precargar = ["2.1", "2.3", "2.4", "2.5", "2.5.1", "2.5.2", "2.5.3", "2.6"]
            
            # Guardar cada sección procesada usando send_data_section
            for section_id in secciones_precargar:
                try:
                    if section_id not in secciones_procesadas:
                        logger.warning(f"No se procesó la sección {section_id} en el generador")
                        continue
                    
                    processed_data = secciones_procesadas[section_id]
                    
                    # Guardar la sección usando send_data_section (igual que en el flujo normal)
                    save_data = {
                        "anio": anio,
                        "mes": mes,
                        "section_id": section_id,
                        "content": processed_data.get("content", {}),
                        "user_id": user_id,
                        "name_file": name_file or f"INFORME_MENSUAL_{mes}_{anio}_V1.docx",
                        "level": processed_data.get("level", 2),
                        "title": processed_data.get("title", section_id)
                    }
                    
                    save_result = await self.send_data_section(save_data)
                    
                    if save_result.get("success"):
                        # Actualizar el campo preloaded a True después de guardar
                        await collection.update_one(
                            {
                                "anio": anio,
                                "mes": mes,
                                "index.id": section_id
                            },
                            {
                                "$set": {
                                    "index.$.preloaded": True
                                }
                            }
                        )
                        resultados["secciones_precargadas"].append(section_id)
                        logger.info(f"✓ Sección {section_id} precargada y guardada exitosamente")
                    else:
                        error_msg = f"No se pudo guardar la sección {section_id}: {save_result.get('message', 'Error desconocido')}"
                        logger.warning(error_msg)
                        resultados["errores"].append(error_msg)
                    
                except Exception as e:
                    error_msg = f"Error al guardar sección {section_id}: {str(e)}"
                    logger.error(error_msg, exc_info=True)
                    resultados["errores"].append(error_msg)
            
            # Si hay errores, marcar como parcialmente exitoso
            if resultados["errores"]:
                resultados["success"] = False
                logger.warning(f"Precarga completada con {len(resultados['errores'])} errores")
            else:
                logger.info(f"✓ Todas las secciones del módulo 2 precargadas exitosamente para {anio}-{mes}")
            
            return resultados
            
        except Exception as e:
            error_msg = f"Error crítico al precargar secciones: {str(e)}"
            logger.error(error_msg, exc_info=True)
            resultados["success"] = False
            resultados["errores"].append(error_msg)
            return resultados
    
 
    async def generate_document(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            anio = data.get("anio")
            mes = data.get("mes")

            document = await self.get_all_section({"anio": anio, "mes": mes})           
            if not document:
                return {
                    "success": False,
                    "message": f"No se encontró el documento para año {anio}, mes {mes}",
                    "data": None
                }            

            return {
                "success": True,
                "message": "Documento generado exitosamente",
                "data": document
            }
        except Exception as e:
            logger.error(f"Error al generar documento: {str(e)}", exc_info=True)
            raise

    async def generate_document_preview(self, data: Dict[str, Any]) -> bytes:
        """
        Genera el documento de la sección 2 y retorna los bytes del archivo para preview.
        
        Args:
            data: Diccionario con anio y mes
            
        Returns:
            bytes: Contenido del archivo .docx generado
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")

            document = await self.get_all_section({"anio": anio, "mes": mes})           
            if not document:
                raise ValueError(f"No se encontró el documento para año {anio}, mes {mes}")
            
            # Generar el documento usando el método del generador que retorna bytes
            generador = GeneradorSeccion2()
            file_bytes = generador.generar_preview(document)
            
            return file_bytes
                    
        except Exception as e:
            logger.error(f"Error al generar preview del documento: {str(e)}", exc_info=True)
            raise

    def serialize_mongo(self, doc):
        if not doc:
         return doc
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
        return doc