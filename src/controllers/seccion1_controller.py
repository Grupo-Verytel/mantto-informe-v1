"""
Controller para generar la sección 1 del informe
"""
from typing import Dict, Any, Optional
from pathlib import Path
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
import logging
from ..services.seccion1_service import Seccion1Service

logger = logging.getLogger(__name__)


class Seccion1Controller:
    """Controller para generar la sección 1"""
    
    def __init__(self):
        self.service = Seccion1Service()
    
    async def generar_seccion1(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Genera el documento de la sección 1 desde MongoDB
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 9,
            "usar_llm_observaciones": false,  # Opcional, por defecto false (usa datos de MongoDB)
            "output_path": "ruta/opcional/archivo.docx"  # Opcional
        }
        
        Retorna:
        {
            "success": true,
            "message": "Sección 1 generada exitosamente",
            "file_path": "ruta/completa/archivo.docx",
            "anio": 2025,
            "mes": 9
        }
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            usar_llm_observaciones = data.get("usar_llm_observaciones", False)
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
                output_path = Path(output_path_str)
            
            # Generar sección 1
            archivo_generado = await self.service.generar_seccion1(
                anio=anio,
                mes=mes,
                usar_llm_observaciones=usar_llm_observaciones,
                output_path=output_path
            )
            
            return {
                "success": True,
                "message": "Sección 1 generada exitosamente",
                "file_path": str(archivo_generado),
                "anio": anio,
                "mes": mes
            }
        
        except FileNotFoundError as e:
            logger.error(f"Error al generar sección 1: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template no encontrado: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error al generar sección 1: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar sección 1: {str(e)}"
            )
    
    async def descargar_seccion1(
        self,
        data: Dict[str, Any]
    ) -> FileResponse:
        """
        Genera y descarga el documento de la sección 1
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 9,
            "usar_llm_observaciones": false
        }
        
        Retorna:
        Archivo Word descargable
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            usar_llm_observaciones = data.get("usar_llm_observaciones", False)
            
            if not anio or not mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="anio y mes son requeridos"
                )
            
            # Generar sección 1
            archivo_generado = await self.service.generar_seccion1(
                anio=anio,
                mes=mes,
                usar_llm_observaciones=usar_llm_observaciones
            )
            
            # Retornar archivo para descarga
            return FileResponse(
                path=str(archivo_generado),
                filename=archivo_generado.name,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        
        except Exception as e:
            logger.error(f"Error al generar/descargar sección 1: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar sección 1: {str(e)}"
            )

