"""
Rutas para generar la sección 4 del informe
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.controllers.seccion4_controller import Seccion4Controller
from src.services.database import get_database

router = APIRouter(prefix="/api/seccion4", tags=["seccion4"])
controller = Seccion4Controller()


@router.post("/generar")
async def generar_seccion4(
    data: Dict[str, Any],
    db: AsyncIOMotorDatabase = Depends(get_database)
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
    
    La lógica es:
    1. Carga datos de inventario desde MongoDB (colección "inventarios")
    2. Transforma los datos al formato esperado por el generador
    3. Genera el documento Word usando python-docx
    4. Guarda el archivo en el directorio de salida
    """
    return await controller.generar_seccion4(data, db)


@router.post("/descargar")
async def descargar_seccion4(
    data: Dict[str, Any],
    db: AsyncIOMotorDatabase = Depends(get_database)
):
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
    return await controller.descargar_seccion4(data, db)

