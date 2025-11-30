"""
Rutas para procesar datos de laboratorio de la sección 5
"""
from fastapi import APIRouter
from typing import Dict, Any
from src.controllers.seccion5_controller import Seccion5Controller

router = APIRouter(prefix="/api/seccion5", tags=["seccion5"])
controller = Seccion5Controller()


@router.post("/procesar-excel")
async def procesar_excel_laboratorio(data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    La lógica es:
    1. Conecta a SharePoint usando las credenciales configuradas
    2. Valida que existe el archivo ANEXO_{MES}.xlsx en la ruta especificada
    3. Descarga el archivo temporalmente
    4. Lee la hoja 2 del Excel
    5. Extrae los datos de la tabla (ID, FECHA, PUNTO, EQUIPO, SERIAL, ESTADO, RADICADO, APROBACION)
    6. Guarda los datos en MongoDB
    7. Retorna los datos procesados
    """
    return await controller.procesar_excel(data)


@router.post("/obtener-datos")
async def obtener_datos_laboratorio(data: Dict[str, Any]) -> Dict[str, Any]:
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
        "total_registros": 10,
        "anio": 2025,
        "mes": 9,
        "mongodb_id": "..."
    }
    """
    return await controller.obtener_datos(data)

