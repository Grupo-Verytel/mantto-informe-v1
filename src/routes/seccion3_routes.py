
from typing import Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, status, Body
from src.controllers.seccion3_controller import Section3Controller

router = APIRouter(prefix="/section3", tags=["Sección 3 - "])

controller_section3 = Section3Controller()


class Metricas(BaseModel):
    disponibilidad_sistema: Optional[float] = None
    calidad_reportes_entregados: Optional[
        Annotated[list[float], Field(min_length=4, max_length=4)]
    ] = None
    oportunidad_reportes_entregados: Optional[float] = None
    rto: Optional[
        Annotated[list[float], Field(min_length=4, max_length=4)]
    ] = None
    tiempo_restauracion_servicios_data_center: Optional[float] = None
    oportunidad_mantenimiento_preventivo: Optional[float] = None


class ReportMonth(BaseModel):
    cant: Metricas
    valor: Metricas



@router.get("/preview", status_code=status.HTTP_200_OK)
async def preview_section3 (year: int, month: int): 
    return await controller_section3.preview_section3(year, month)
    
@router.post("/", status_code=status.HTTP_200_OK)
async def set_data_setion (body : ReportMonth, year: int, month: int):
    return await controller_section3.set_data_setion(body, month, year)
    
# @router.get("/get_all_section", status_code=status.HTTP_200_OK)
# async def get_all_section(
#     data: Dict[str, Any] = Body(...),    
# ) -> Dict[str, Any]:   
    


# @router.post("/send_data_section", status_code=status.HTTP_200_OK)
# async def send_data_section(
#     data: Dict[str, Any] = Body(...),    
# ) -> Dict[str, Any]:   
    

# @router.post("/generate_document", status_code=status.HTTP_200_OK)
# async def generate_document(
#     data: Dict[str, Any] = Body(...),    
# ) -> Dict[str, Any]:   
     

  
