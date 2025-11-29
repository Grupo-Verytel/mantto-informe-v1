"""
Rutas para procesar comunicados emitidos de la sección 1.6.1
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.controllers.comunicados_controller import ComunicadosController

router = APIRouter(prefix="/api/comunicados", tags=["comunicados"])
controller = ComunicadosController()


@router.post("/emitidos")
async def procesar_comunicados_emitidos(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa comunicados emitidos desde SharePoint para la sección 1.6.1
    
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
    
    La lógica es:
    1. Se conecta a la carpeta específica en SharePoint: 
       "01SEP - 30SEP / 01 OBLIGACIONES GENERALES / OBLIGACIÓN 7 y 10 / COMUNICADOS EMITIDOS"
    2. Lista todos los archivos en esa carpeta
    3. Para cada archivo:
       - Extrae el radicado del nombre del archivo
       - Descarga y extrae el texto del archivo
       - Usa LLM para extraer la fecha del encabezado y el asunto
    4. Guarda los resultados en MongoDB
    """
    return await controller.procesar_comunicados_emitidos(data)


@router.post("/recibidos")
async def procesar_comunicados_recibidos(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa comunicados recibidos desde SharePoint para la sección 1.6.2
    
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
    
    La lógica es:
    1. Se conecta a la carpeta específica en SharePoint: 
       "01SEP - 30SEP / 01 OBLIGACIONES GENERALES / OBLIGACIÓN 7 y 10 / COMUNICADOS RECIBIDOS"
    2. Lista todos los archivos en esa carpeta
    3. Para cada archivo:
       - Extrae el radicado del nombre del archivo
       - Descarga y extrae el texto del archivo
       - Usa LLM para extraer la fecha del encabezado y el asunto
    4. Guarda los resultados en MongoDB
    """
    return await controller.procesar_comunicados_recibidos(data)

