import logging
from typing import Dict, Any
from fastapi import HTTPException, status
from src.utils.date_path import _construir_ruta_mes
from config import MESES
from src.services.seccion3_service import Section3Service
from src.generadores.seccion_3_ans import GeneradorSeccion3
from pathlib import Path
import config

logger = logging.getLogger(__name__)


class Section3Controller:
    def __init__(self):
        self.service = Section3Service()
        self.generador = None  # Se inicializa cuando se necesite
    
    # 3  INFORMES DE MEDICIÓN DE NIVELES DE SERVICIO (ANS
    
    async def preview_section3(self, year: int, month: int):
        """Genera un documento Word con el nombre de la plantilla obteniendo los datos guardados en MongoDB"""
        try:
             
            self.generador = GeneradorSeccion3(year, month)
            document_response = await self.service.generate_document({
            "anio": year,
            "mes": month
             })
            if not document_response.get("success"):
               raise ValueError(document_response.get("message"))
            document_data = document_response.get("data", {})
            # Generar el nombre del archivo de salida
            output_dir = config.OUTPUT_DIR / "seccion_3"
            output_dir.mkdir(parents=True, exist_ok=True)
            

            
            name_file = document_data.get("name_file")
            # Asegurar que tenga extensión .docx
            if not name_file.endswith('.docx'):
                name_file = f"{name_file}.docx"
            output_path = output_dir / name_file
            
            # Generar y guardar el documento pasando el documento completo
            self.generador.generar(document=document_data, output_path=output_path)
            
            return {
                "success": True,
                "message": "Documento generado exitosamente",
                "data": {
                    "file_name": name_file,
                    "file_path": str(output_path),
                    "relative_path": f"seccion_3/{name_file}"
                }
            }
            
        except Exception as e:
            logger.error(f"Error en controlador al generar preview: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar el documento: {str(e)}"
            )
    
    async def set_data_setion(self, body, mes_numero: int, anio: int):
        """Guarda la información en MongoDB en la etiqueta content como lo hace la section2"""
        try:
            # Calcular valor total
            valor_total = 0
            if body.valor.disponibilidad_sistema:
                valor_total += float(body.valor.disponibilidad_sistema)
            if body.valor.calidad_reportes_entregados:
                for valor in body.valor.calidad_reportes_entregados:
                    if valor:
                        valor_total += float(valor)
            if body.valor.oportunidad_reportes_entregados:
                valor_total += float(body.valor.oportunidad_reportes_entregados)
            if body.valor.rto:
                for valor in body.valor.rto:
                    if valor:
                        valor_total += float(valor)
            if body.valor.tiempo_restauracion_servicios_data_center:
                valor_total += float(body.valor.tiempo_restauracion_servicios_data_center)
            if body.valor.oportunidad_mantenimiento_preventivo:
                valor_total += float(body.valor.oportunidad_mantenimiento_preventivo)
            
            # Preparar el contenido para guardar en MongoDB
            content = {
                'mes': mes_numero,
                'anio': anio,
                'ruta_folder': _construir_ruta_mes(mes_numero, anio),
                'nombre_archivo': f'{MESES[mes_numero]} {anio}',
            
                'cant_disponibilidad_sistema': body.cant.disponibilidad_sistema,
                'valor_disponibilidad_sistema': body.valor.disponibilidad_sistema,

                'cant_calidad_informes_1': body.cant.calidad_reportes_entregados[0] if body.cant.calidad_reportes_entregados and len(body.cant.calidad_reportes_entregados) > 0 else None,
                'valor_calidad_informes_1': body.valor.calidad_reportes_entregados[0] if body.valor.calidad_reportes_entregados and len(body.valor.calidad_reportes_entregados) > 0 else None,
                'cant_calidad_informes_2': body.cant.calidad_reportes_entregados[1] if body.cant.calidad_reportes_entregados and len(body.cant.calidad_reportes_entregados) > 1 else None,
                'valor_calidad_informes_2': body.valor.calidad_reportes_entregados[1] if body.valor.calidad_reportes_entregados and len(body.valor.calidad_reportes_entregados) > 1 else None,
                'cant_calidad_informes_3': body.cant.calidad_reportes_entregados[2] if body.cant.calidad_reportes_entregados and len(body.cant.calidad_reportes_entregados) > 2 else None,
                'valor_calidad_informes_3': body.valor.calidad_reportes_entregados[2] if body.valor.calidad_reportes_entregados and len(body.valor.calidad_reportes_entregados) > 2 else None,
                'cant_calidad_informes_4': body.cant.calidad_reportes_entregados[3] if body.cant.calidad_reportes_entregados and len(body.cant.calidad_reportes_entregados) > 3 else None,
                'valor_calidad_informes_4': body.valor.calidad_reportes_entregados[3] if body.valor.calidad_reportes_entregados and len(body.valor.calidad_reportes_entregados) > 3 else None,

                'cant_oportunidad_informes': body.cant.oportunidad_reportes_entregados,
                'valor_oportunidad_informes': body.valor.oportunidad_reportes_entregados,

                'cant_rto_1': body.cant.rto[0] if body.cant.rto and len(body.cant.rto) > 0 else None,
                'valor_rto_1': body.valor.rto[0] if body.valor.rto and len(body.valor.rto) > 0 else None,
                'cant_rto_2': body.cant.rto[1] if body.cant.rto and len(body.cant.rto) > 1 else None,
                'valor_rto_2': body.valor.rto[1] if body.valor.rto and len(body.valor.rto) > 1 else None,
                'cant_rto_3': body.cant.rto[2] if body.cant.rto and len(body.cant.rto) > 2 else None,
                'valor_rto_3': body.valor.rto[2] if body.valor.rto and len(body.valor.rto) > 2 else None,
                'cant_rto_4': body.cant.rto[3] if body.cant.rto and len(body.cant.rto) > 3 else None,
                'valor_rto_4': body.valor.rto[3] if body.valor.rto and len(body.valor.rto) > 3 else None,
                
                'cant_tiempo_restauracion': body.cant.tiempo_restauracion_servicios_data_center,
                'valor_tiempo_restauracion': body.valor.tiempo_restauracion_servicios_data_center,
                
                'cant_oportunidad_actividades': body.cant.oportunidad_mantenimiento_preventivo,
                'valor_oportunidad_actividades': body.valor.oportunidad_mantenimiento_preventivo,
       
                'valor_total': valor_total,
            }
            
            # Preparar los datos para el servicio (similar a section2)
            data_section = {
                "anio": anio,
                "mes": mes_numero,
                "section_id": "3",
                "level": 1,
                "title": "3. INFORMES DE MEDICIÓN DE NIVELES DE SERVICIO (ANS)",
                "content": content,
                "user_id": 1,  # Por defecto, se puede obtener del contexto de autenticación
                "name_file": f"INFORME_MENSUAL_{mes_numero}_{anio}_V1.docx"
            }
            
            # Guardar en MongoDB usando el servicio
            return await self.service.send_data_section(data_section)
            
        except Exception as e:
            logger.error(f"Error en controlador al guardar datos: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al guardar los datos: {str(e)}"
            )
