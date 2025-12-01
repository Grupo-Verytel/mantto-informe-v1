from typing import Dict, Any
from fastapi import HTTPException, status
import logging
from ..services.section2_service import Section2Service
from ..generadores.seccion_2_mesa_servicio import GeneradorSeccion2

logger = logging.getLogger(__name__)


class Section2Controller:
    
    def __init__(self):
        self.service = Section2Service()
        self.generador = GeneradorSeccion2()

    async def get_section_by_index(
        self, 
        data: Dict[str, Any],         
    ) -> Dict[str, Any]:
        try:
            return await self.service.get_section_by_index(data)
        except Exception as e:
            logger.error(f"Error en controlador al obtener sección: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la sección: {str(e)}"
            )
    
    async def get_all_section(
        self, 
        data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        try:
            return await self.service.get_all_section(data)
        except Exception as e:
            logger.error(f"Error en controlador al obtener toda la sección: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la sección completa: {str(e)}"
            )
    
    async def send_data_section(
        self, 
        data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        try:
            
            """ EVALUAMOS A QUE SECCION SE REQUIERE ACTUALIZAR """
            id_section = data.get("section_id")

            if id_section == "2":
                data_section = self.generador._seccion_2(data)
            elif id_section == "2.1":
                data_section = await self.generador._seccion_2_1_mesa_servicio(data)
            elif id_section == "2.2":
                data_section = self.generador._seccion_2_2_herramientas(data)
            elif id_section == "2.3":
                data_section = await self.generador._seccion_2_3_visitas_diagnostico(data)
            elif id_section == "2.4":
                data_section = await self.generador._seccion_2_4_tickets(data)
            elif id_section == "2.5":
                data_section = self.generador._seccion_2_5_escalamientos(data)
            elif id_section == "2.5.1":
                data_section = self.generador._seccion_2_5_1_enel(data)
            elif id_section == "2.5.2":
                data_section = self.generador._seccion_2_5_2_caida_masiva(data)
            elif id_section == "2.5.3":
                data_section = self.generador._seccion_2_5_3_conectividad(data)
            elif id_section == "2.6":
                data_section = self.generador._seccion_2_6_hojas_vida(data)
            elif id_section == "2.7":
                data_section = self.generador._seccion_2_7_estado_sistema(data)
            else:
                secciones_validas = ["2", "2.1", "2.2", "2.3", "2.4", "2.5", "2.5.1", "2.5.2", "2.5.3", "2.6", "2.7"]
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El section_id '{id_section}' no es válido. Secciones válidas: {', '.join(secciones_validas)}"
                )

            return await self.service.send_data_section(data_section)

        except Exception as e:
            logger.error(f"Error en controlador al guardar datos: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al guardar los datos: {str(e)}"
            )

    async def generate_document(
        self, 
        data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        try:
            # Obtener el documento desde el servicio
            document_response = await self.service.generate_document(data)
            
            if not document_response.get("success"):
                return document_response
            
            document_data = document_response.get("data")
            if not document_data:
                return {
                    "success": False,
                    "message": f"No se encontró el documento para año {data.get('anio')}, mes {data.get('mes')}",
                    "data": None
                }
            
            # Generar el nombre del archivo de salida
            from pathlib import Path
            import config
            anio = data.get("anio")
            mes = data.get("mes")
            
            # Ruta fija: output/seccion_2
            output_dir = config.OUTPUT_DIR / "seccion_2"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Nombre del archivo basado en el name_file del documento o uno por defecto
            name_file = document_data.get("name_file", f"INFORME_MENSUAL_{mes}_{anio}_V1")
            # Asegurar que tenga extensión .docx
            if not name_file.endswith('.docx'):
                name_file = f"{name_file}.docx"
            output_path = output_dir / name_file
            
            # Generar y guardar el documento (generar() ahora guarda automáticamente si se pasa output_path)
            self.generador.generar(document_data, output_path)
            
            return {
                "success": True,
                "message": "Documento generado exitosamente",
                "data": {
                    "file_name": name_file,
                    "file_path": str(output_path),
                    "relative_path": f"seccion_2/{name_file}"
                }
            }

        except Exception as e:
            logger.error(f"Error en controlador al generar sección: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar la sección: {str(e)}"
            )