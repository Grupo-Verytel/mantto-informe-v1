"""
Rutas para generar la sección 1 del informe
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.controllers.seccion1_controller import Seccion1Controller

router = APIRouter(prefix="/api/seccion1", tags=["seccion1"])
controller = Seccion1Controller()


@router.post("/generar")
async def generar_seccion1(data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    La lógica es:
    1. Carga variables estáticas desde config.py
    2. Carga datos de tablas desde MongoDB:
       - obligaciones_generales (subsección 1.5.1)
       - obligaciones_especificas (subsección 1.5.2)
       - obligaciones_ambientales (subsección 1.5.3)
       - obligaciones_anexos (subsección 1.5.4)
       - comunicados_emitidos (subsección 1.6.1)
       - comunicados_recibidos (subsección 1.6.2)
    3. Genera el documento Word usando el template con Jinja2
    4. Guarda el archivo en el directorio de salida
    """
    return await controller.generar_seccion1(data)


@router.post("/descargar")
async def descargar_seccion1(data: Dict[str, Any]):
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
    return await controller.descargar_seccion1(data)

