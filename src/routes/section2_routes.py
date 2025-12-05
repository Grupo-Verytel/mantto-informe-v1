"""
Rutas para la Sección 2: Informe de Mesa de Servicio
"""
from typing import Dict, Any
from fastapi import APIRouter, status, Body
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


@router.get("/get_all_section", status_code=status.HTTP_200_OK)
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

  
