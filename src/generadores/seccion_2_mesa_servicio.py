from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from typing import Dict, List, Any, Optional
from datetime import datetime
import calendar
import json
import config
# Nota: get_glpi_extractor ahora es async, se debe llamar cuando se necesite

from docxtpl import DocxTemplate
from docx import Document
from pathlib import Path
from docxtpl import InlineImage
from docx.shared import Mm
import base64
from PIL import Image
from io import BytesIO
import logging
import re

logger = logging.getLogger(__name__)
from src.utils.date_path import _construir_ruta_mes

class GeneradorSeccion2:
 
    
    @property
    def nombre_seccion(self) -> str:
        return "2. INFORME DE MESA DE SERVICIO"
    
    @property
    def template_file(self) -> str:
        return "seccion_2_mesa_servicio.docx"
    
    def __init__(self, ):        
        self.glpi_extractor = None  # Se inicializa cuando se necesite (async)
        self.datos = {}
        self.doc = None
        self.anio = None
        self.mes = None

    def _seccion_2(self, data: Dict[str, Any]):       
     
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "image": data.get("content").get("image"),                
            },
        }
        return content_data

    async def _seccion_2_1_mesa_servicio(self, data: Dict[str, Any]):
        
        from src.services.glpi_service import get_glpi_service
        glpi_service = await get_glpi_service()

        content = data.get("content", {})
        anio = data.get("anio")
        mes = data.get("mes")
        table_2 = await glpi_service.get_actividades_por_subsistema(anio, mes)            
        
        content_data = {
            "anio": anio,
            "mes": mes,
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "route": content.get("route", "") or (date_path._construir_ruta_mes(mes, anio) if mes and anio else ""),
                "image": content.get("image", ""),
                "table_1": content.get("table_1", []),
                "table_2": table_2,
            },
        }
        
        return content_data
    
    def _seccion_2_2_herramientas(self, data: Dict[str, Any]):
        content = data.get("content", {})
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "email": content.get("email", ""),
            },
        }
        
        return content_data
    
    async def _seccion_2_3_visitas_diagnostico(self, data: Dict[str, Any]):
        content = data.get("content", {})
        anio = data.get("anio")
        mes = data.get("mes")
        
        # Obtener datos desde GLPI si no están en el content
        table_1 = content.get("table_1", [])
        if not table_1 and anio and mes:
            try:
                from src.services.glpi_service import get_glpi_service
                glpi_service = await get_glpi_service()
                table_1 = await glpi_service.get_visitas_diagnostico_subsistemas(anio, mes)
            except Exception as e:
                logger.warning(f"Error al obtener table_1 desde GLPI MySQL para sección 2.3: {e}. Usando datos de content.")
                table_1 = content.get("table_1", [])
        
        content_data = {
            "anio": anio,
            "mes": mes,
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "table_1": table_1,
                "comunicacion": content.get("comunicacion", ""),
                "oficio": content.get("oficio", ""),
            },
        }
        
        return content_data
    
    def _seccion_2_4_tickets(self, data: Dict[str, Any]):
        content = data.get("content", {})
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "table_1": content.get("table_1", []),
                "name_document": content.get("name_document", ""),
                "table_2": content.get("table_2", []),
            },
        }
        
        return content_data
    
    def _seccion_2_5_escalamientos(self, data: Dict[str, Any]):
        content = data.get("content", {})
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "table_1": content.get("table_1", []),
            },
        }
        
        return content_data
    
    def _seccion_2_5_1_enel(self, data: Dict[str, Any]):
        content = data.get("content", {})
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "table_1": content.get("table_1", []),
            },
        }
        
        return content_data
    
    def _seccion_2_5_2_caida_masiva(self, data: Dict[str, Any]):
        content = data.get("content", {})
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "table_1": content.get("table_1", []),
            },
        }
        
        return content_data
    
    def _seccion_2_5_3_conectividad(self, data: Dict[str, Any]):
        content = data.get("content", {})
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "table_1": content.get("table_1", []),
            },
        }
        
        return content_data
    
    def _seccion_2_6_hojas_vida(self, data: Dict[str, Any]):
        content = data.get("content", {})
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "name_document": content.get("name_document", ""),
            },
        }
        
        return content_data
    
    def _seccion_2_7_estado_sistema(self, data: Dict[str, Any]):
        content = data.get("content", {})
        content_data = {
            "anio": data.get("anio"),
            "mes": data.get("mes"),
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "section_id": data.get("section_id"),
            "level": data.get("level"),
            "content": {
                "table_1": content.get("table_1", []),
                "image": content.get("image", ""),
                "section_1": content.get("section_1", ""),
                "section_2": content.get("section_2", ""),
                "table_2": content.get("table_2", []),
                "section_3": content.get("section_3", ""),
                "table_3": content.get("table_3", []),
                "name_document": content.get("name_document", ""),
            },
        }
        
        return content_data
    
    def _procesar_imagen(self, template: DocxTemplate, image_b64: str) -> Any:
        """Convierte una imagen base64 a InlineImage o retorna string vacío"""
        if template and image_b64:
            try:
                return self.base64_to_inline_image(template, image_b64)
            except Exception as e:
                print(f"[WARNING] Error procesando imagen: {str(e)}")
                return ""
        return ""
    
    def _set_cell_shading(self, cell, hex_color: str):
        """
        Aplica color de fondo a una celda de tabla
        
        Args:
            cell: Celda de la tabla
            hex_color: Color en formato hexadecimal (ej: "1F4E79" para azul oscuro)
        """
        shading_elm = OxmlElement('w:shd')
        shading_elm.set(qn('w:fill'), hex_color)
        cell._element.get_or_add_tcPr().append(shading_elm)
    
    def _centrar_celda_vertical(self, cell):
        """Centra verticalmente el contenido de una celda"""
        tc = cell._element
        tcPr = tc.get_or_add_tcPr()
        vAlign = OxmlElement('w:vAlign')
        vAlign.set(qn('w:val'), 'center')
        tcPr.append(vAlign)
    
    def _enable_autofit(self, table):
        """
        Activa el autoajuste real para tablas en Word.
        Esto imita la opción: Tabla → Autoajustar → Ajustar al contenido.
        """
        tbl = table._element
        
        # Obtener o crear tblPr
        if tbl.tblPr is None:
            tblPr = OxmlElement('w:tblPr')
            tbl.insert(0, tblPr)
        else:
            tblPr = tbl.tblPr

        # Eliminar layout existente si existe
        tblLayout = tblPr.find(qn('w:tblLayout'))
        if tblLayout is not None:
            tblPr.remove(tblLayout)

        # Crear nuevo layout con autofit
        new_tblLayout = OxmlElement('w:tblLayout')
        new_tblLayout.set(qn('w:type'), 'autofit')  
        tblPr.append(new_tblLayout)

        # Permitir que cada celda se adapte eliminando anchos fijos
        for row in table.rows:
            for cell in row.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                tcW = tcPr.find(qn('w:tcW'))
                if tcW is not None:
                    tcPr.remove(tcW)
    
    def _preparar_datos_tabla(self, datos: List[Dict[str, Any]], headers: List[str], campos: List[str], 
                              agregar_totales: bool = False, columna_total_texto: int = 0) -> List[List[str]]:
        """
        Prepara los datos de una tabla en formato lista de listas para crear tablas programáticamente.
        
        Args:
            datos: Lista de diccionarios con los datos de las filas
            headers: Lista de encabezados de las columnas
            campos: Lista de nombres de campos en el mismo orden que los headers
            agregar_totales: Si True, agrega una fila de totales al final
            columna_total_texto: Índice de la columna donde poner el texto "TOTAL" (por defecto 0)
            
        Returns:
            Lista de listas donde la primera fila son los headers y las siguientes son los datos
        """
        table_data = [headers]
        
        for item in datos:
            fila = []
            for campo in campos:
                valor = item.get(campo, "")
                fila.append(str(valor) if valor is not None else "")
            table_data.append(fila)
        
        # Agregar fila de totales si se solicita
        if agregar_totales and datos:
            fila_total = []
            for idx, campo in enumerate(campos):
                if idx == columna_total_texto:
                    fila_total.append("TOTAL")
                else:
                    # Intentar sumar los valores numéricos de esta columna
                    try:
                        total = 0
                        for item in datos:
                            valor = item.get(campo, "")
                            if valor:
                                # Intentar convertir a número (puede ser string o número)
                                if isinstance(valor, str):
                                    # Remover espacios y caracteres no numéricos excepto punto y coma
                                    valor_limpio = valor.replace(",", "").replace(" ", "").strip()
                                    if valor_limpio:
                                        total += float(valor_limpio)
                                else:
                                    total += float(valor)
                        fila_total.append(str(int(total)) if total == int(total) else str(total))
                    except (ValueError, TypeError):
                        # Si no se puede sumar, dejar vacío
                        fila_total.append("")
            table_data.append(fila_total)
        
        return table_data
    
    def _reemplazar_placeholder_con_tabla(self, doc: Document, placeholder: str, table_data: List[List[str]]):
        """
        Busca un placeholder en el documento y lo reemplaza con una tabla creada programáticamente.
        
        Args:
            doc: Documento Word (después de renderizar)
            placeholder: Texto del placeholder a buscar (ej: "[[TABLE_21_1]]")
            table_data: Lista de listas con los datos de la tabla (primera fila son headers)
        """
        if not table_data or len(table_data) == 0:
            return
        
        # Estilos de tabla comunes en Word (en orden de preferencia)
        estilos_tabla = ['Table Grid', 'Light Shading', 'Light List', 'Medium Shading 1', 'Light Grid']
        
        # Buscar el placeholder en todos los párrafos
        for i, paragraph in enumerate(doc.paragraphs):
            if placeholder in paragraph.text:
                # Crear la tabla
                tabla = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
                
                # Intentar aplicar un estilo de tabla disponible
                estilo_aplicado = False
                for estilo in estilos_tabla:
                    try:
                        tabla.style = estilo
                        estilo_aplicado = True
                        break
                    except:
                        continue
                
                # Si ningún estilo funcionó, usar el estilo por defecto
                if not estilo_aplicado:
                    try:
                        tabla.style = 'Table Grid'
                    except:
                        pass
                
                # Activar autofit real (ajustar al contenido)
                self._enable_autofit(tabla)
                
                # Llenar la tabla
                total_rows = len(table_data)
                for row_idx, fila in enumerate(table_data):
                    for col_idx, valor in enumerate(fila):
                        celda = tabla.rows[row_idx].cells[col_idx]
                        celda.text = str(valor) if valor is not None else ""
                        
                        # Formatear headers (primera fila) - Azul oscuro con texto blanco
                        if row_idx == 0:
                            # Aplicar fondo azul oscuro (similar al estilo original)
                            self._set_cell_shading(celda, "1F4E79")
                            self._centrar_celda_vertical(celda)
                            for paragraph_celda in celda.paragraphs:
                                paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                for run in paragraph_celda.runs:
                                    run.bold = True
                                    run.font.size = Pt(8)
                                    run.font.color.rgb = RGBColor(255, 255, 255)  # Texto blanco
                        elif row_idx == total_rows - 1 and fila[0].upper() == "TOTAL":
                            # Fila de totales - Fondo azul claro con texto en negrita
                            self._set_cell_shading(celda, "D9E1F2")  # Azul claro
                            self._centrar_celda_vertical(celda)
                            for paragraph_celda in celda.paragraphs:
                                paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                for run in paragraph_celda.runs:
                                    run.bold = True
                                    run.font.size = Pt(8)
                                    run.font.color.rgb = RGBColor(0, 0, 0)  # Texto negro
                        else:
                            # Filas de datos - Fondo gris claro alternado
                            if row_idx % 2 == 0:
                                self._set_cell_shading(celda, "F2F2F2")  # Gris muy claro
                            else:
                                self._set_cell_shading(celda, "FFFFFF")  # Blanco
                            self._centrar_celda_vertical(celda)
                            for paragraph_celda in celda.paragraphs:
                                paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.LEFT
                                for run in paragraph_celda.runs:
                                    run.font.size = Pt(8)
                                    run.font.color.rgb = RGBColor(0, 0, 0)  # Texto negro
                
                # Insertar la tabla después del párrafo que contiene el placeholder
                parent = paragraph._element.getparent()
                # Obtener el índice del párrafo actual
                para_idx = parent.index(paragraph._element)
                # Insertar la tabla después del párrafo
                parent.insert(para_idx + 1, tabla._element)
                
                # Eliminar el placeholder del párrafo
                paragraph.text = paragraph.text.replace(placeholder, "").strip()
                
                # Si el párrafo quedó vacío, eliminarlo
                if not paragraph.text.strip():
                    parent.remove(paragraph._element)
                
                break
        
        # También buscar en tablas existentes (por si el placeholder está dentro de una celda de tabla)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if placeholder in paragraph.text:
                            # Limpiar la celda y crear la tabla dentro
                            cell.text = ""
                            
                            # Crear tabla dentro de la celda
                            inner_table = cell.add_table(rows=len(table_data), cols=len(table_data[0]))
                            
                            # Intentar aplicar un estilo de tabla disponible
                            estilo_aplicado = False
                            for estilo in estilos_tabla:
                                try:
                                    inner_table.style = estilo
                                    estilo_aplicado = True
                                    break
                                except:
                                    continue
                            
                            if not estilo_aplicado:
                                try:
                                    inner_table.style = 'Table Grid'
                                except:
                                    pass
                            
                            # Activar autofit real (ajustar al contenido)
                            self._enable_autofit(inner_table)
                            
                            # Llenar la tabla interna
                            total_rows_inner = len(table_data)
                            for row_idx, fila in enumerate(table_data):
                                for col_idx, valor in enumerate(fila):
                                    celda_inner = inner_table.rows[row_idx].cells[col_idx]
                                    celda_inner.text = str(valor) if valor is not None else ""
                                    
                                    if row_idx == 0:
                                        # Header - Azul oscuro con texto blanco
                                        self._set_cell_shading(celda_inner, "1F4E79")
                                        self._centrar_celda_vertical(celda_inner)
                                        for paragraph_celda in celda_inner.paragraphs:
                                            paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                            for run in paragraph_celda.runs:
                                                run.bold = True
                                                run.font.size = Pt(8)
                                                run.font.color.rgb = RGBColor(255, 255, 255)
                                    elif row_idx == total_rows_inner - 1 and fila[0].upper() == "TOTAL":
                                        # Fila de totales - Fondo azul claro con texto en negrita
                                        self._set_cell_shading(celda_inner, "D9E1F2")  # Azul claro
                                        self._centrar_celda_vertical(celda_inner)
                                        for paragraph_celda in celda_inner.paragraphs:
                                            paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                            for run in paragraph_celda.runs:
                                                run.bold = True
                                                run.font.size = Pt(8)
                                                run.font.color.rgb = RGBColor(0, 0, 0)  # Texto negro
                                    else:
                                        # Filas de datos - Fondo gris claro alternado
                                        if row_idx % 2 == 0:
                                            self._set_cell_shading(celda_inner, "F2F2F2")
                                        else:
                                            self._set_cell_shading(celda_inner, "FFFFFF")
                                        self._centrar_celda_vertical(celda_inner)
                                        for paragraph_celda in celda_inner.paragraphs:
                                            paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.LEFT
                                            for run in paragraph_celda.runs:
                                                run.font.size = Pt(8)
                                                run.font.color.rgb = RGBColor(0, 0, 0)
                            
                            break
    
    def _construir_contexto(self, document: Dict[str, Any], template: DocxTemplate) -> Dict[str, Any]:
        mes = document.get("mes")
        anio = document.get("anio")
        
        # Asegurar que mes y anio sean válidos
        mes_nombre = config.MESES.get(mes, "") if mes else ""

        index = document.get("index", [])
        if not isinstance(index, list):
            index = []
        
        # Construir la ruta del mes si no existe
        route_21 = ""
        if mes and anio:
            route_21 = date_path._construir_ruta_mes(mes, anio)
        
        # Inicializar contexto base
        contexto = {
            "mes": mes_nombre,
            "anio": anio,
            "mes_numero": mes,
        }
        
        # Sección 2 (index[0]) - INFORME DE MESA DE SERVICIO
        if len(index) > 0:
            content_2 = index[0].get("content", {})
            contexto["image_2"] = self._procesar_imagen(template, content_2.get("image", ""))
        
        # Sección 2.1 (index[1]) - INFORME DE MESA DE SERVICIO
        if len(index) > 1:
            content_21 = index[1].get("content", {})
            # Si la ruta está vacía en el documento, usar la construida
            route_doc = content_21.get("route", "")
            contexto["route_21"] = route_doc if route_doc else route_21
            contexto["image_21"] = self._procesar_imagen(template, content_21.get("image", ""))
            
            # Preparar datos de tablas en formato lista de listas
            table_1_data = content_21.get("table_1", [])
            if table_1_data:
                headers_21_1 = ["ÍTEM", "FECHA", "REFERENCIA", "RADICADO", "ESTADO", "APROBACIÓN"]
                campos_21_1 = ["item", "fecha", "referencia", "radicado", "estado", "aprobacion"]
                contexto["table_21_1"] = self._preparar_datos_tabla(table_1_data, headers_21_1, campos_21_1)
            else:
                contexto["table_21_1"] = []
            
            table_2_data = content_21.get("table_2", [])
            if table_2_data:
                headers_21_2 = ["SUBSISTEMA", "DIAGNÓSTICO", "DIAGNÓSTICO SUBSISTEMA", "LIMPIEZA ACRÍLICO", 
                                "MTO ACOMETIDA", "MTO CORRECTIVO", "MTO CORRECTIVO SUBSISTEMA", "PLAN DE CHOQUE", "TOTAL"]
                campos_21_2 = ["subsistema", "diagnostico", "diagnostico_subsistema", "limpieza_acrilico",
                              "mto_acometida", "mto_correctivo", "mto_correctivo_subsistema", "plan_de_choque", "total"]
                
                # Calcular el total de diagnósticos (suma de la columna "diagnostico")
                total_diagnostico = 0
                try:
                    for item in table_2_data:
                        valor = item.get("diagnostico", "")
                        if valor:
                            if isinstance(valor, str):
                                valor_limpio = valor.replace(",", "").replace(" ", "").strip()
                                if valor_limpio:
                                    total_diagnostico += float(valor_limpio)
                            else:
                                total_diagnostico += float(valor)
                except (ValueError, TypeError):
                    pass
                
                # Asignar el total de diagnósticos al contexto
                contexto["diagnostico_21"] = str(int(total_diagnostico)) if total_diagnostico == int(total_diagnostico) else str(total_diagnostico)
                
                # Agregar fila de totales (columna 0 es SUBSISTEMA donde pondremos "TOTAL")
                contexto["table_21_2"] = self._preparar_datos_tabla(
                    table_2_data, headers_21_2, campos_21_2, 
                    agregar_totales=True, columna_total_texto=0
                )
            else:
                contexto["table_21_2"] = []
                contexto["diagnostico_21"] = "0"            
        # Sección 2.2 (index[2]) - HERRAMIENTAS DE TRABAJO
        if len(index) > 2:
            content_22 = index[2].get("content", {})
            contexto["email_22"] = content_22.get("email", "")
        
        # Sección 2.3 (index[3]) - VISITAS DE DIAGNÓSTICOS A SUBSISTEMAS
        if len(index) > 3:
            content_23 = index[3].get("content", {})
            contexto["comunicacion_23"] = content_23.get("comunicacion", "")
            contexto["oficio_23"] = content_23.get("oficio", "")
            
            # Preparar datos de tabla en formato lista de listas
            table_23_data = content_23.get("table_1", [])
            if table_23_data:
                headers_23_1 = ["SUBSISTEMA", "EJECUTADAS"]
                campos_23_1 = ["subsistema", "ejecutadas"]
                # Agregar fila de totales (columna 0 es SUBSISTEMA donde pondremos "TOTAL")
                contexto["table_23_1"] = self._preparar_datos_tabla(
                    table_23_data, headers_23_1, campos_23_1,
                    agregar_totales=True, columna_total_texto=0
                )
            else:
                contexto["table_23_1"] = []
        
        # Sección 2.4 (index[4]) - INFORME CONSOLIDADO DEL ESTADO DE LOS TICKETS ADMINISTRATIVOS
        if len(index) > 4:
            content_24 = index[4].get("content", {})
            contexto["table_24_1"] = content_24.get("table_1", [])
            contexto["name_document_24"] = content_24.get("name_document", "")
            contexto["table_24_2"] = content_24.get("table_2", [])
        
        # Sección 2.5 (index[5]) - ESCALAMIENTOS
        if len(index) > 5:
            content_25 = index[5].get("content", {})
            contexto["table_25_1"] = content_25.get("table_1", [])
        
        # Sección 2.5.1 (index[6]) - ENEL
        if len(index) > 6:
            content_251 = index[6].get("content", {})
            contexto["table_251_1"] = content_251.get("table_1", [])
        
        # Sección 2.5.2 (index[7]) - CAÍDA MASIVA
        if len(index) > 7:
            content_252 = index[7].get("content", {})
            contexto["table_252_1"] = content_252.get("table_1", [])
        
        # Sección 2.5.3 (index[8]) - CONECTIVIDAD
        if len(index) > 8:
            content_253 = index[8].get("content", {})
            contexto["table_253_1"] = content_253.get("table_1", [])
        
        # Sección 2.6 (index[9]) - INFORME ACTUALIZADO DE HOJAS DE VIDA
        if len(index) > 9:
            content_26 = index[9].get("content", {})
            contexto["name_document_26"] = content_26.get("name_document", "")
        
        # Sección 2.7 (index[10]) - INFORME EJECUTIVO DEL ESTADO DEL SISTEMA
        if len(index) > 10:
            content_27 = index[10].get("content", {})
            contexto["table_27_1"] = content_27.get("table_1", [])
            contexto["image_27"] = self._procesar_imagen(template, content_27.get("image", ""))
            contexto["section_27_1"] = content_27.get("section_1", "")
            contexto["section_27_2"] = content_27.get("section_2", "")
            contexto["table_27_2"] = content_27.get("table_2", [])
            contexto["section_27_3"] = content_27.get("section_3", "")
            contexto["table_27_3"] = content_27.get("table_3", [])
            contexto["name_document_27"] = content_27.get("name_document", "")
        
        return contexto
    
    def generar(self, document: Dict[str, Any], output_path: Optional[Path] = None):       
        
        template_path = config.TEMPLATES_DIR / self.template_file
        template = DocxTemplate(str(template_path) )
                
        contexto = self._construir_contexto(document , template)
        if output_path:
            # Asegurar que el output_path tenga extensión .docx
            if not str(output_path).endswith('.docx'):
                output_path = Path(str(output_path) + '.docx')

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Preparar placeholders especiales para tablas
        # El usuario puede usar {{ table_21_1_placeholder }} o [[TABLE_21_1]] directamente en el Word
        contexto_tablas = contexto.copy()
        if contexto.get("table_21_1"):
            contexto_tablas["table_21_1_placeholder"] = "[[TABLE_21_1]]"
        if contexto.get("table_21_2"):
            contexto_tablas["table_21_2_placeholder"] = "[[TABLE_21_2]]"
        if contexto.get("table_23_1"):
            contexto_tablas["table_23_1_placeholder"] = "[[TABLE_23_1]]"
        
        # Renderizar el template con las variables básicas
        template.render(contexto_tablas)
        
        # Guardar temporalmente para poder trabajar con el documento renderizado
        temp_path = str(output_path).replace('.docx', '_temp.docx')
        template.save(temp_path)
        
        # Abrir el documento renderizado para insertar tablas programáticamente
        doc = Document(temp_path)
        
        # Reemplazar placeholders de tablas con tablas creadas programáticamente
        if contexto.get("table_21_1"):
            self._reemplazar_placeholder_con_tabla(doc, "[[TABLE_21_1]]", contexto["table_21_1"])
        
        if contexto.get("table_21_2"):
            self._reemplazar_placeholder_con_tabla(doc, "[[TABLE_21_2]]", contexto["table_21_2"])
        
        if contexto.get("table_23_1"):
            self._reemplazar_placeholder_con_tabla(doc, "[[TABLE_23_1]]", contexto["table_23_1"])
        
        # Guardar el documento final
        doc.save(str(output_path))
        
        # Eliminar archivo temporal
        try:
            Path(temp_path).unlink()
        except:
            pass

        print(f"[OK] Documento generado en: {output_path}")
        
        return template

    def base64_to_inline_image(self, template: DocxTemplate, base64_str: str, width_mm: int = 150) -> InlineImage:        
        if not base64_str or not isinstance(base64_str, str):
            return None

        if "," in base64_str:
            base64_str = base64_str.split(",")[1]

        # Decodificar
        image_bytes = base64.b64decode(base64_str)

        # Crear imagen en memoria
        stream = BytesIO(image_bytes)

        # Validar imagen opcionalmente
        try:
         Image.open(stream)
        except Exception as e:
            raise ValueError(f"La imagen Base64 no es válida: {str(e)}")

        # Crear InlineImage
        return InlineImage(template, stream, width=Mm(width_mm)) 