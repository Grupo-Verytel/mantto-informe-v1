"""
Controller para procesar datos de laboratorio de la sección 5
"""
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
import logging
from ..services.seccion5_service import Seccion5Service

logger = logging.getLogger(__name__)


class Seccion5Controller:
    """Controller para procesar datos de laboratorio"""
    
    def __init__(self):
        self.service = Seccion5Service()
    
    async def procesar_excel(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Procesa el archivo Excel de laboratorio desde SharePoint y lo guarda en MongoDB
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 9,
            "ruta_sharepoint": "ruta/opcional/en/sharepoint",  # Opcional
            "user_id": 1  # Opcional
        }
        
        Retorna:
        {
            "success": true,
            "message": "Archivo procesado exitosamente...",
            "total_registros": 10,
            "datos": [...],
            "mongodb_id": "...",
            "archivo": "ANEXO_SEPTIEMBRE.xlsx",
            "ruta_sharepoint": "..."
        }
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            ruta_sharepoint = data.get("ruta_sharepoint")
            user_id = data.get("user_id")
            
            if not anio or not mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="anio y mes son requeridos"
                )
            
            if mes < 1 or mes > 12:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="mes debe estar entre 1 y 12"
                )
            
            # Procesar Excel desde SharePoint
            resultado = await self.service.procesar_excel_desde_sharepoint(
                anio=anio,
                mes=mes,
                ruta_sharepoint=ruta_sharepoint,
                user_id=user_id
            )
            
            if not resultado.get("success"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=resultado.get("message", "Error al procesar el archivo Excel")
                )
            
            return resultado
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error al procesar Excel de laboratorio: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar Excel de laboratorio: {str(e)}"
            )
    
    async def obtener_datos(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Obtiene los datos de laboratorio desde MongoDB
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 9
        }
        
        Retorna:
        {
            "success": true,
            "datos": [...],
            "total_registros": 10
        }
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            
            if not anio or not mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="anio y mes son requeridos"
                )
            
            if mes < 1 or mes > 12:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="mes debe estar entre 1 y 12"
                )
            
            # Obtener datos desde MongoDB
            documento = await self.service.obtener_datos_laboratorio(anio, mes)
            
            if not documento:
                return {
                    "success": True,
                    "message": "No se encontraron datos de laboratorio para el período especificado",
                    "datos": [],
                    "total_registros": 0
                }
            
            datos_laboratorio = documento.get("datos_laboratorio", [])
            
            return {
                "success": True,
                "datos": datos_laboratorio,
                "total_registros": len(datos_laboratorio),
                "anio": anio,
                "mes": mes,
                "mongodb_id": str(documento.get("_id", ""))
            }
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error al obtener datos de laboratorio: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener datos de laboratorio: {str(e)}"
            )
    
    async def generar_seccion5(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Genera el documento de la sección 5 desde MongoDB
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 9,
            "output_path": "ruta/opcional/archivo.docx"  # Opcional
        }
        
        Retorna:
        {
            "success": true,
            "message": "Sección 5 generada exitosamente",
            "file_path": "ruta/completa/archivo.docx",
            "anio": 2025,
            "mes": 9
        }
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            output_path_str = data.get("output_path")
            
            if not anio or not mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="anio y mes son requeridos"
                )
            
            if mes < 1 or mes > 12:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="mes debe estar entre 1 y 12"
                )
            
            # Determinar ruta de salida
            output_path = None
            if output_path_str:
                from pathlib import Path
                output_path = Path(output_path_str)
            
            # Generar sección 5
            archivo_generado = await self.service.generar_seccion5(
                anio=anio,
                mes=mes,
                output_path=output_path
            )
            
            return {
                "success": True,
                "message": "Sección 5 generada exitosamente",
                "file_path": str(archivo_generado),
                "anio": anio,
                "mes": mes
            }
        
        except FileNotFoundError as e:
            logger.error(f"Error al generar sección 5: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template no encontrado: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error al generar sección 5: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar sección 5: {str(e)}"
            )

