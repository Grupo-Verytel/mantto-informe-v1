"""
Rutas para procesar obligaciones de la sección 1.5
"""
from typing import Dict, Any
from fastapi import APIRouter, status, Body
from ..controllers.obligaciones_controller import ObligacionesController

router = APIRouter(prefix="/obligaciones", tags=["Obligaciones - Sección 1.5"])

obligaciones_controller = ObligacionesController()


@router.post("/procesar", status_code=status.HTTP_200_OK)
async def procesar_obligaciones(
    data: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    """
    Procesa obligaciones y genera observaciones dinámicamente desde anexos de SharePoint
    
    Body:
    {
        "anio": 2025,
        "mes": 9,
        "seccion": 1,  # Opcional, por defecto 1
        "subseccion": "1.5.1",  # Opcional: "1.5.1", "1.5.2", "1.5.3", "1.5.4"
        "regenerar_todas": false,  # Si true, regenera todas las observaciones
        "user_id": 1  # Opcional: ID del usuario que realiza la operación
    }
    
    Subsecciones disponibles:
    - 1.5.1: Obligaciones Generales
    - 1.5.2: Obligaciones Específicas
    - 1.5.3: Obligaciones Ambientales
    - 1.5.4: Obligaciones de Anexos (verifica existencia de archivos en SharePoint)
    
    El proceso:
    1. Carga obligaciones desde data/fuentes/obligaciones_{mes}_{anio}.json (PLANTILLA - no se modifica)
    2. Si se especifica subseccion, solo procesa esa subsección
    3. Para cada obligación con regenerar_observacion=true:
       - Descarga anexo desde SharePoint (si aplica)
       - Extrae texto del anexo (PDF/Word/Excel)
       - Genera observación usando LLM
    4. Guarda resultados SOLO en MongoDB (el archivo JSON es una plantilla y no se modifica)
    
    Respuesta:
    Si se especifica subseccion, retorna solo esa subsección:
    {
        "anio": 2025,
        "mes": 9,
        "seccion": 1,
        "obligaciones_generales": [...]  // o obligaciones_especificas, etc.
    }
    """
    return await obligaciones_controller.procesar_obligaciones(data)

