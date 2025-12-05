from typing import Dict, Any
from ..services.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from datetime import datetime
from ..data.repositories.build_section2 import get_section2
from bson import ObjectId

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
                new_section = {
                    "id": section_id,
                    "level": level,
                    "title": title,
                    "content": content,
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
            
            collection = self._get_collection()
            
            document = await collection.find_one({"anio": anio, "mes": mes})     
            if not document:
                return None     
                
            document = self.serialize_mongo(document)
            return document
        except Exception as e:
            logger.error(f"Error al obtener toda la sección: {str(e)}", exc_info=True)
            raise
    
 
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

    def serialize_mongo(self, doc):
        if not doc:
         return doc
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
        return doc