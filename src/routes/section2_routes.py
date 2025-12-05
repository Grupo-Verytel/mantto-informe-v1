"""
Rutas para la Sección 2: Informe de Mesa de Servicio
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, status, Body, Query
from fastapi.responses import Response
from ..controllers.section2_controller import Section2Controller

router = APIRouter(prefix="/section2", tags=["Sección 2 - Mesa de Servicio"])

section2_controller = Section2Controller()

# ============================================================================
# RUTAS
# ============================================================================

@router.get("/get_section_by_index", status_code=status.HTTP_200_OK)
async def get_section_by_index(
    data: Dict[str, Any] = Body(...),    
) -> Dict[str, Any]:   
    return await section2_controller.get_section_by_index(data)


@router.post("/get_all_section", status_code=status.HTTP_200_OK)
async def get_all_section(
    data: Dict[str, Any] = Body(...),    
) -> Dict[str, Any]:   
    return await section2_controller.get_all_section(data)


@router.post("/send_data_section", status_code=status.HTTP_200_OK)
async def send_data_section(
    data: Dict[str, Any] = Body(...),    
) -> Dict[str, Any]:   
    return await section2_controller.send_data_section(data)

@router.post("/generate_document", status_code=status.HTTP_200_OK)
async def generate_document(
    data: Dict[str, Any] = Body(...),    
) -> Dict[str, Any]:
    return await section2_controller.generate_document(data)


@router.post("/seccion_2_preview", status_code=status.HTTP_200_OK)
async def seccion_2_preview(
    data: Dict[str, Any] = Body(...),    
) -> Response:
    """
    Genera el documento de la sección 2 y lo retorna como bytes para preview.
    
    Body esperado:
    {
        "anio": 2025,
        "mes": 11
    }
    
    Retorna:
    Archivo .docx como bytes (para usar con docx-preview en el frontend)
    """
    return await section2_controller.seccion_2_preview(data)

  
