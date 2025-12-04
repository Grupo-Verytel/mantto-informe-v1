"""
Controller para generar la sección 4 del informe
"""
from typing import Dict, Any, Optional
from pathlib import Path
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
import logging
from ..services.seccion4_service import Seccion4Service
from ..services.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


class Seccion4Controller:
    """Controller para generar la sección 4"""
    
    def __init__(self):
        self.service = Seccion4Service()
    
    async def generar_seccion4(
        self,
        data: Dict[str, Any],
        db: Optional[AsyncIOMotorDatabase] = None
    ) -> Dict[str, Any]:
        """
        Genera el documento de la sección 4 desde MongoDB
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 11,
            "output_path": "ruta/opcional/archivo.docx"  # Opcional
        }
        
        Retorna:
        {
            "success": true,
            "message": "Sección 4 generada exitosamente",
            "file_path": "ruta/completa/archivo.docx",
            "anio": 2025,
            "mes": 11
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
            
            # Obtener base de datos si no se proporciona
            if db is None:
                from ..services.database import get_database
                db = get_database()
            
            # Determinar ruta de salida
            output_path = None
            if output_path_str:
                output_path = Path(output_path_str)
            
            # Generar sección 4
            archivo_generado = await self.service.generar_seccion4(
                anio=anio,
                mes=mes,
                output_path=output_path,
                db=db
            )
            
            return {
                "success": True,
                "message": "Sección 4 generada exitosamente",
                "file_path": str(archivo_generado),
                "anio": anio,
                "mes": mes
            }
        
        except FileNotFoundError as e:
            logger.error(f"Error al generar sección 4: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template no encontrado: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error al generar sección 4: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar sección 4: {str(e)}"
            )
    
    async def descargar_seccion4(
        self,
        data: Dict[str, Any],
        db: Optional[AsyncIOMotorDatabase] = None
    ) -> FileResponse:
        """
        Genera y descarga el documento de la sección 4
        
        Body esperado:
        {
            "anio": 2025,
            "mes": 11
        }
        
        Retorna:
        Archivo Word descargable
        """
        try:
            anio = data.get("anio")
            mes = data.get("mes")
            
            if not anio or not mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="anio y mes son requeridos"
                )
            
            # Obtener base de datos si no se proporciona
            if db is None:
                from ..services.database import get_database
                db = get_database()
            
            # Generar sección 4
            archivo_generado = await self.service.generar_seccion4(
                anio=anio,
                mes=mes,
                db=db
            )
            
            # Retornar archivo para descarga
            return FileResponse(
                path=str(archivo_generado),
                filename=archivo_generado.name,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        
        except Exception as e:
            logger.error(f"Error al generar/descargar sección 4: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar sección 4: {str(e)}"
            )

