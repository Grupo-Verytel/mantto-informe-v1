"""
Controller para procesar comunicados emitidos de la sección 1.6.1
"""
from typing import Dict, Any
from fastapi import HTTPException, status
import logging
from ..services.comunicados_emitidos_service import ComunicadosEmitidosService

logger = logging.getLogger(__name__)


class ComunicadosController:
    """Controller para procesar comunicados emitidos y recibidos"""
    
    def __init__(self):
        self.service = ComunicadosEmitidosService()
    
    async def procesar_comunicados_emitidos(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Procesa comunicados emitidos desde SharePoint
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 9,
            "seccion": 1,  # Opcional, por defecto 1
            "subseccion": "1.6.1",  # Opcional, por defecto "1.6.1"
            "regenerar_todas": false,  # Si true, regenera toda la información
            "user_id": 1  # Opcional: ID del usuario que realiza la operación
        }
        
        Retorna:
        {
            "anio": 2025,
            "mes": 9,
            "seccion": 1,
            "subseccion": "1.6.1",
            "comunicados_emitidos": [
                {
                    "item": 1,
                    "radicado": "GSC-7444-2025",
                    "fecha": "23/09/2025",
                    "asunto": "INGRESOS ELEMENTOS ALMACÉN SEPTIEMBRE 2025",
                    "nombre_archivo": "GSC-7444-2025.pdf",
                    "ruta_completa": "ruta/completa/archivo.pdf"
                },
                ...
            ],
            "mongodb_id": "..."
        }
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            seccion = data.get("seccion", 1)
            subseccion = data.get("subseccion", "1.6.1")
            regenerar_todas = data.get("regenerar_todas", False)
            
            if not anio or not mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="anio y mes son requeridos"
                )
            
            # Procesar comunicados emitidos
            comunicados = self.service.procesar_comunicados_emitidos(
                anio=anio,
                mes=mes,
                regenerar_todas=regenerar_todas
            )
            
            # Formatear respuesta
            respuesta = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion,
                "subseccion": subseccion,
                "comunicados_emitidos": comunicados
            }
            
            # Guardar en MongoDB
            try:
                user_id = data.get("user_id")
                documento_mongo = await self.service.guardar_comunicados_en_mongodb(
                    comunicados=comunicados,
                    anio=anio,
                    mes=mes,
                    seccion=seccion,
                    subseccion=subseccion,
                    tipo="emitidos",
                    user_id=user_id
                )
                respuesta["mongodb_id"] = str(documento_mongo.get("_id")) if documento_mongo else None
            except Exception as e:
                logger.warning(f"No se pudo guardar en MongoDB: {e}")
                # No fallar la petición si MongoDB falla
            
            return respuesta
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error en controlador al procesar comunicados emitidos: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar comunicados emitidos: {str(e)}"
            )
    
    async def procesar_comunicados_recibidos(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Procesa comunicados recibidos desde SharePoint
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 9,
            "seccion": 1,  # Opcional, por defecto 1
            "subseccion": "1.6.2",  # Opcional, por defecto "1.6.2"
            "regenerar_todas": false,  # Si true, regenera toda la información
            "user_id": 1  # Opcional: ID del usuario que realiza la operación
        }
        
        Retorna:
        {
            "anio": 2025,
            "mes": 9,
            "seccion": 1,
            "subseccion": "1.6.2",
            "comunicados_recibidos": [
                {
                    "item": 1,
                    "radicado": "GSC-7444-2025",
                    "fecha": "23/09/2025",
                    "asunto": "INGRESOS ELEMENTOS ALMACÉN SEPTIEMBRE 2025",
                    "nombre_archivo": "GSC-7444-2025.pdf",
                    "ruta_completa": "ruta/completa/archivo.pdf"
                },
                ...
            ],
            "mongodb_id": "..."
        }
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            seccion = data.get("seccion", 1)
            subseccion = data.get("subseccion", "1.6.2")
            regenerar_todas = data.get("regenerar_todas", False)
            
            if not anio or not mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="anio y mes son requeridos"
                )
            
            # Procesar comunicados recibidos
            comunicados = self.service.procesar_comunicados_recibidos(
                anio=anio,
                mes=mes,
                regenerar_todas=regenerar_todas
            )
            
            # Formatear respuesta
            respuesta = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion,
                "subseccion": subseccion,
                "comunicados_recibidos": comunicados
            }
            
            # Guardar en MongoDB
            try:
                user_id = data.get("user_id")
                documento_mongo = await self.service.guardar_comunicados_en_mongodb(
                    comunicados=comunicados,
                    anio=anio,
                    mes=mes,
                    seccion=seccion,
                    subseccion=subseccion,
                    tipo="recibidos",
                    user_id=user_id
                )
                respuesta["mongodb_id"] = str(documento_mongo.get("_id")) if documento_mongo else None
            except Exception as e:
                logger.warning(f"No se pudo guardar en MongoDB: {e}")
                # No fallar la petición si MongoDB falla
            
            return respuesta
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error en controlador al procesar comunicados recibidos: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar comunicados recibidos: {str(e)}"
            )

