"""
Controller para procesar obligaciones de la sección 1.5
"""
from typing import Dict, Any
from fastapi import HTTPException, status
import logging
from ..services.obligaciones_service import ObligacionesService

logger = logging.getLogger(__name__)


class ObligacionesController:
    """Controller para procesar obligaciones"""
    
    def __init__(self):
        self.service = ObligacionesService()
    
    async def procesar_obligaciones(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Procesa obligaciones y genera observaciones dinámicamente
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 9,
            "seccion": 1,  # Opcional, por defecto 1
            "subseccion": "1.5.1",  # Opcional: "1.5.1", "1.5.2", "1.5.3", "1.5.4"
            "regenerar_todas": false,  # Si true, regenera todas las observaciones
            "guardar_json": true  # Si true, guarda el JSON actualizado
        }
        
        Si se especifica subseccion, solo procesa esa subsección.
        Si no se especifica, procesa todas las obligaciones.
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            seccion = data.get("seccion", 1)
            subseccion = data.get("subseccion")
            regenerar_todas = data.get("regenerar_todas", False)
            guardar_json = data.get("guardar_json", True)
            
            if not anio or not mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="anio y mes son requeridos"
                )
            
            # Si se especifica subsección, procesar solo esa
            if subseccion:
                obligaciones_procesadas = self.service.procesar_subseccion(
                    anio=anio,
                    mes=mes,
                    subseccion=subseccion,
                    regenerar_todas=regenerar_todas
                )
                
                # Formatear respuesta según el formato solicitado
                tipo_obligacion = self.service.obtener_tipo_obligacion_por_subseccion(subseccion)
                
                respuesta = {
                    "anio": anio,
                    "mes": mes,
                    "seccion": seccion
                }
                # Agregar las obligaciones con el nombre del tipo (no la subsección)
                respuesta[tipo_obligacion] = obligaciones_procesadas.get(tipo_obligacion, [])
                
                # Guardar si se solicita (solo actualizar la subsección en el JSON)
                if guardar_json:
                    # Cargar JSON completo, actualizar solo la subsección, y guardar
                    obligaciones_completas = self.service.cargar_obligaciones_desde_json(anio, mes)
                    obligaciones_completas[tipo_obligacion] = obligaciones_procesadas.get(tipo_obligacion, [])
                    self.service.guardar_obligaciones_procesadas(
                        obligaciones_completas,
                        anio=anio,
                        mes=mes,
                        crear_backup=True
                    )
                
                # Guardar en MongoDB
                try:
                    user_id = data.get("user_id")  # Opcional, puede venir en el request
                    documento_mongo = await self.service.guardar_obligaciones_en_mongodb(
                        obligaciones=obligaciones_procesadas,
                        anio=anio,
                        mes=mes,
                        seccion=seccion,
                        subseccion=subseccion,
                        user_id=user_id
                    )
                    respuesta["mongodb_id"] = str(documento_mongo.get("_id")) if documento_mongo else None
                except Exception as e:
                    logger.warning(f"No se pudo guardar en MongoDB: {e}")
                    # No fallar la petición si MongoDB falla
                
                return respuesta
            else:
                # Procesar todas las obligaciones (comportamiento anterior)
                obligaciones_procesadas = self.service.procesar_todas_las_obligaciones(
                    anio=anio,
                    mes=mes,
                    regenerar_todas=regenerar_todas
                )
                
                # Guardar si se solicita
                if guardar_json:
                    self.service.guardar_obligaciones_procesadas(
                        obligaciones_procesadas,
                        anio=anio,
                        mes=mes,
                        crear_backup=True
                    )
                
                # Guardar en MongoDB (sin subsección específica)
                try:
                    user_id = data.get("user_id")  # Opcional, puede venir en el request
                    documento_mongo = await self.service.guardar_obligaciones_en_mongodb(
                        obligaciones=obligaciones_procesadas,
                        anio=anio,
                        mes=mes,
                        seccion=seccion,
                        subseccion=None,  # Todas las subsecciones
                        user_id=user_id
                    )
                except Exception as e:
                    logger.warning(f"No se pudo guardar en MongoDB: {e}")
                    # No fallar la petición si MongoDB falla
                
                # Formatear respuesta con todas las obligaciones
                respuesta = {
                    "anio": anio,
                    "mes": mes,
                    "seccion": seccion
                }
                respuesta.update(obligaciones_procesadas)
                
                return respuesta
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error en controlador al procesar obligaciones: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar obligaciones: {str(e)}"
            )

