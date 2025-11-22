"""
Generador Sección 3: Informes de Medición de Niveles de Servicio (ANS)
Tipo: 🟨 ANÁLISIS IA (cumplimiento) + 🟩 EXTRACCIÓN DATOS (MySQL)

SECCIÓN CRÍTICA - Impacto contractual y financiero
- Umbral contractual: 98.9% de disponibilidad
- Si no cumple: calcular penalidades y explicar causas

Subsecciones:
- 3.1 Penalidad de ANS
- 3.2 Consolidado ANS (histórico y gráficos)
"""
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import json
from .base import GeneradorSeccion
import config
from ans_config.ans_config import UMBRAL_ANS, calcular_penalidad, PENALIDAD_CONFIG
from src.extractores.mysql_extractor import get_mysql_extractor


class GeneradorSeccion3(GeneradorSeccion):
    """Genera la Sección 3: Informes de Medición de Niveles de Servicio (ANS)"""
    
    # Colores
    COLOR_AZUL_OSCURO = RGBColor(31, 78, 121)
    COLOR_AZUL_MEDIO = RGBColor(46, 117, 182)
    COLOR_GRIS = RGBColor(64, 64, 64)
    COLOR_VERDE = RGBColor(0, 128, 0)
    COLOR_ROJO = RGBColor(192, 0, 0)
    COLOR_AMARILLO = RGBColor(255, 192, 0)
    
    @property
    def nombre_seccion(self) -> str:
        return "3. INFORMES DE MEDICIÓN DE NIVELES DE SERVICIO (ANS)"
    
    @property
    def template_file(self) -> str:
        return "seccion_3_ans.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.datos: Dict[str, Any] = {}
        self.doc: Optional[Document] = None
        self.mysql_extractor = get_mysql_extractor()
        self.disponibilidad: float = 0.0
        self.cumple_ans: bool = False
    
    def _configurar_estilos(self):
        """Configura los estilos del documento"""
        if self.doc is None:
            return
        style = self.doc.styles['Normal']
        style.font.name = 'Arial'
        style.font.size = Pt(11)
        
        h1 = self.doc.styles['Heading 1']
        h1.font.name = 'Arial'
        h1.font.size = Pt(14)
        h1.font.bold = True
        h1.font.color.rgb = self.COLOR_AZUL_OSCURO
        
        h2 = self.doc.styles['Heading 2']
        h2.font.name = 'Arial'
        h2.font.size = Pt(12)
        h2.font.bold = True
        h2.font.color.rgb = self.COLOR_AZUL_MEDIO
        
        h3 = self.doc.styles['Heading 3']
        h3.font.name = 'Arial'
        h3.font.size = Pt(11)
        h3.font.bold = True
        h3.font.color.rgb = self.COLOR_GRIS
    
    def _set_cell_shading(self, cell, color_hex: str):
        """Establece el color de fondo de una celda"""
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), color_hex)
        cell._tc.get_or_add_tcPr().append(shading)
    
    def _agregar_tabla(self, encabezados: list, filas: list, anchos: list = None,
                       colores_fila: list = None, alineaciones: list = None):
        """Agrega una tabla con formato profesional"""
        tabla = self.doc.add_table(rows=1, cols=len(encabezados))
        tabla.style = 'Table Grid'
        tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Encabezados
        hdr_cells = tabla.rows[0].cells
        for i, texto in enumerate(encabezados):
            hdr_cells[i].text = texto
            for paragraph in hdr_cells[i].paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(255, 255, 255)
            self._set_cell_shading(hdr_cells[i], "1F4E79")
        
        # Filas de datos
        for idx, fila_datos in enumerate(filas):
            row_cells = tabla.add_row().cells
            for i, texto in enumerate(fila_datos):
                row_cells[i].text = str(texto) if texto is not None else ""
                for paragraph in row_cells[i].paragraphs:
                    # Alineación personalizada
                    if alineaciones and i < len(alineaciones):
                        paragraph.alignment = alineaciones[i]
                    else:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in paragraph.runs:
                        run.font.size = Pt(10)
            
            # Aplicar color de fila
            if colores_fila and idx < len(colores_fila) and colores_fila[idx]:
                for cell in row_cells:
                    self._set_cell_shading(cell, colores_fila[idx])
        
        # Ajustar anchos
        if anchos:
            for i, ancho in enumerate(anchos):
                for cell in tabla.columns[i].cells:
                    cell.width = Inches(ancho)
        
        self.doc.add_paragraph()
        return tabla
    
    def _agregar_parrafo(self, texto: str, justificado: bool = True, 
                         negrita: bool = False, color: RGBColor = None):
        """Agrega un párrafo de texto"""
        p = self.doc.add_paragraph()
        run = p.add_run(texto)
        run.bold = negrita
        if color:
            run.font.color.rgb = color
        if justificado:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        return p
    
    def _calcular_penalidad(self) -> dict:
        """
        Calcula la penalidad por incumplimiento de ANS
        Usa la función de config.ans_config
        """
        valor_mensual = self.datos.get('valor_mensual_contrato', PENALIDAD_CONFIG['valor_mensual_contrato'])
        return calcular_penalidad(self.disponibilidad, UMBRAL_ANS, valor_mensual)
    
    def _generar_analisis_cumplimiento(self) -> str:
        """Genera el análisis de cumplimiento del ANS (placeholder para LLM)"""
        mes = config.MESES[self.mes]
        anio = self.anio
        
        if self.cumple_ans:
            return f"""Durante el mes de {mes} de {anio} se obtuvo un indicador de disponibilidad del {self.disponibilidad:.2f}%, CUMPLIENDO satisfactoriamente con el mínimo del {UMBRAL_ANS}% establecido en el contrato SCJ-1809-2024.

El cumplimiento del ANS se logró gracias a:
• Atención oportuna de los mantenimientos correctivos
• Ejecución del plan de mantenimiento preventivo según cronograma
• Gestión eficiente de los escalamientos a proveedores (ENEL, ETB)
• Monitoreo continuo del sistema de videovigilancia
• Disponibilidad de repuestos en la bolsa del contrato

Se destaca que la disponibilidad obtenida supera el umbral contractual en {self.disponibilidad - UMBRAL_ANS:.2f} puntos porcentuales."""
        
        else:
            # Análisis de incumplimiento
            causas = self.datos.get('causas_incumplimiento', [])
            causas_texto = "\n".join([f"• {c}" for c in causas]) if causas else "• Causas en proceso de análisis"
            
            acciones = self.datos.get('acciones_correctivas', [])
            acciones_texto = "\n".join([f"• {a}" for a in acciones]) if acciones else "• Acciones correctivas en definición"
            
            return f"""Durante el mes de {mes} de {anio} se obtuvo un indicador de disponibilidad del {self.disponibilidad:.2f}%, NO CUMPLIENDO con el mínimo del {UMBRAL_ANS}% establecido en el contrato SCJ-1809-2024.

El déficit de {UMBRAL_ANS - self.disponibilidad:.2f} puntos porcentuales se debe a las siguientes causas:
{causas_texto}

ACCIONES CORRECTIVAS IMPLEMENTADAS:
{acciones_texto}

El contratista se compromete a implementar las medidas necesarias para recuperar el nivel de servicio comprometido en el próximo periodo."""
    
    def _generar_intro_ans(self) -> str:
        """Genera el párrafo introductorio de la sección ANS"""
        mes = config.MESES[self.mes]
        anio = self.anio
        
        return f"""El Acuerdo de Nivel de Servicio (ANS) establecido en el contrato SCJ-1809-2024 define que el contratista debe garantizar una disponibilidad mínima del {UMBRAL_ANS}% del sistema de videovigilancia de Bogotá D.C.

A continuación se presenta el informe de medición del ANS correspondiente al mes de {mes} de {anio}, incluyendo el cálculo de disponibilidad por localidad, el análisis de cumplimiento y, de ser aplicable, el cálculo de penalidades."""
    
    def _seccion_3_1_penalidad_ans(self):
        """3.1 Penalidad de ANS"""
        self.doc.add_heading("3.1. PENALIDAD DE ANS", level=2)
        
        mes = config.MESES[self.mes]
        anio = self.anio
        
        # Párrafo introductorio
        self._agregar_parrafo(self._generar_intro_ans())
        
        # Fórmula de cálculo
        self._agregar_parrafo("FÓRMULA DE CÁLCULO DE DISPONIBILIDAD:", negrita=True)
        
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("Disponibilidad (%) = (Horas Operativas / Horas Totales del Mes) × 100")
        run.italic = True
        run.font.size = Pt(11)
        self.doc.add_paragraph()
        
        # Datos del cálculo
        horas_mes = self.datos.get('horas_totales_mes', 720)
        horas_operativas = self.datos.get('horas_operativas', 0)
        horas_no_operativas = self.datos.get('horas_no_operativas', 0)
        
        self._agregar_parrafo("DATOS DEL PERIODO:", negrita=True)
        
        filas_calculo = [
            ["Horas totales del mes", f"{horas_mes} horas"],
            ["Horas operativas", f"{horas_operativas:,.0f} horas"],
            ["Horas no operativas", f"{horas_no_operativas:,.0f} horas"],
            ["Disponibilidad calculada", f"{self.disponibilidad:.2f}%"],
            ["Umbral contractual (ANS)", f"{UMBRAL_ANS}%"],
        ]
        
        # Color de la última fila según cumplimiento
        colores = [None, None, None, 
                   "C6EFCE" if self.cumple_ans else "FFC7CE",  # Verde si cumple, rojo si no
                   "D9E1F2"]
        
        self._agregar_tabla(
            encabezados=["CONCEPTO", "VALOR"],
            filas=filas_calculo,
            anchos=[3.5, 2.5],
            colores_fila=colores
        )
        
        # Resultado del ANS
        self._agregar_parrafo("RESULTADO DEL ANS:", negrita=True)
        
        if self.cumple_ans:
            p = self._agregar_parrafo(
                f"✓ ANS CUMPLIDO - Disponibilidad: {self.disponibilidad:.2f}% (Umbral: {UMBRAL_ANS}%)",
                color=self.COLOR_VERDE,
                negrita=True
            )
        else:
            p = self._agregar_parrafo(
                f"✗ ANS NO CUMPLIDO - Disponibilidad: {self.disponibilidad:.2f}% (Umbral: {UMBRAL_ANS}%)",
                color=self.COLOR_ROJO,
                negrita=True
            )
        
        # Análisis de cumplimiento (IA)
        self._agregar_parrafo("ANÁLISIS DE CUMPLIMIENTO:", negrita=True)
        self._agregar_parrafo(self._generar_analisis_cumplimiento())
        
        # Tabla de disponibilidad por localidad
        self._agregar_parrafo("DISPONIBILIDAD POR LOCALIDAD:", negrita=True)
        
        disponibilidad_localidad = self.datos.get('disponibilidad_por_localidad', [])
        if disponibilidad_localidad:
            filas = []
            colores_localidad = []
            for loc in disponibilidad_localidad:
                disp = loc['disponibilidad']
                filas.append([
                    loc['localidad'],
                    loc['total_camaras'],
                    f"{loc['horas_operativas']:,.0f}",
                    f"{loc['horas_no_operativas']:,.0f}",
                    f"{disp:.2f}%"
                ])
                # Color según cumplimiento individual
                if disp >= UMBRAL_ANS:
                    colores_localidad.append("C6EFCE")  # Verde
                elif disp >= UMBRAL_ANS - 1:
                    colores_localidad.append("FFEB9C")  # Amarillo
                else:
                    colores_localidad.append("FFC7CE")  # Rojo
            
            self._agregar_tabla(
                encabezados=["LOCALIDAD", "CÁMARAS", "HRS OPERATIVAS", "HRS NO OPER.", "DISPONIBILIDAD"],
                filas=filas,
                anchos=[1.8, 0.9, 1.2, 1.2, 1.2],
                colores_fila=colores_localidad
            )
        
        # Cálculo de penalidad (si aplica)
        penalidad = self._calcular_penalidad()
        
        self._agregar_parrafo("CÁLCULO DE PENALIDAD:", negrita=True)
        
        if penalidad['aplica']:
            self._agregar_parrafo(
                f"De acuerdo con las condiciones contractuales, se aplica penalidad por incumplimiento del ANS:",
                color=self.COLOR_ROJO
            )
            
            filas_penalidad = [
                ["Déficit de disponibilidad", f"{penalidad['deficit']:.2f}%"],
                ["Porcentaje de penalidad", f"{penalidad['porcentaje_penalidad']:.2f}%"],
                ["Valor de la penalidad", f"${penalidad['valor_penalidad']:,.0f}"],
            ]
            
            self._agregar_tabla(
                encabezados=["CONCEPTO", "VALOR"],
                filas=filas_penalidad,
                anchos=[3.5, 2.5],
                colores_fila=["FFC7CE", "FFC7CE", "FFC7CE"]
            )
        else:
            self._agregar_parrafo(
                "No aplica penalidad. El ANS fue cumplido satisfactoriamente.",
                color=self.COLOR_VERDE
            )
    
    def _seccion_3_2_consolidado_ans(self):
        """3.2 Consolidado ANS"""
        self.doc.add_heading("3.2. CONSOLIDADO ANS", level=2)
        
        self._agregar_parrafo(
            "A continuación se presenta el histórico de cumplimiento del ANS desde el inicio del contrato:"
        )
        
        # Tabla histórico ANS
        historico = self.datos.get('historico_ans', [])
        if historico:
            filas = []
            colores = []
            for h in historico:
                cumple = h['disponibilidad'] >= UMBRAL_ANS
                filas.append([
                    h['mes'],
                    f"{h['disponibilidad']:.2f}%",
                    f"{UMBRAL_ANS}%",
                    "✓ Cumple" if cumple else "✗ No cumple",
                    h.get('observaciones', '-')
                ])
                colores.append("C6EFCE" if cumple else "FFC7CE")
            
            self._agregar_tabla(
                encabezados=["MES", "DISPONIBILIDAD", "UMBRAL", "ESTADO", "OBSERVACIONES"],
                filas=filas,
                anchos=[1.3, 1.1, 0.9, 1.0, 2.2],
                colores_fila=colores
            )
        
        # Resumen acumulado
        self._agregar_parrafo("RESUMEN ACUMULADO:", negrita=True)
        
        meses_cumplidos = sum(1 for h in historico if h['disponibilidad'] >= UMBRAL_ANS)
        total_meses = len(historico)
        promedio_disponibilidad = sum(h['disponibilidad'] for h in historico) / total_meses if total_meses > 0 else 0
        
        filas_resumen = [
            ["Total meses evaluados", str(total_meses)],
            ["Meses con ANS cumplido", str(meses_cumplidos)],
            ["Meses con ANS no cumplido", str(total_meses - meses_cumplidos)],
            ["Porcentaje de cumplimiento", f"{(meses_cumplidos/total_meses*100):.1f}%" if total_meses > 0 else "N/A"],
            ["Disponibilidad promedio", f"{promedio_disponibilidad:.2f}%"],
        ]
        
        self._agregar_tabla(
            encabezados=["INDICADOR", "VALOR"],
            filas=filas_resumen,
            anchos=[3.5, 2.0]
        )
        
        # Nota sobre gráficos
        self._agregar_parrafo(
            "Nota: Los gráficos de tendencia del ANS se encuentran en el Anexo 3.1 del presente informe.",
            negrita=False
        )
    
    def cargar_datos(self) -> None:
        """Carga los datos específicos de la sección 3 desde JSON y MySQL"""
        # Cargar datos desde archivo JSON
        # Intentar primero con formato numérico, luego con nombre de mes
        archivo = config.FUENTES_DIR / f"ans_{self.mes}_{self.anio}.json"
        if not archivo.exists():
            archivo = config.FUENTES_DIR / f"ans_{config.MESES[self.mes].lower()}_{self.anio}.json"
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    self.datos = json.load(f)
            except Exception as e:
                print(f"[WARNING] Error al cargar datos desde {archivo}: {e}")
                self.datos = {}
        else:
            print(f"[WARNING] Archivo de datos no encontrado: {archivo}")
            self.datos = {}
        
        # Cargar datos desde MySQL (usando extractor)
        disponibilidad_mes = self.mysql_extractor.get_disponibilidad_mes(self.anio, self.mes)
        if disponibilidad_mes and disponibilidad_mes.get('disponibilidad_porcentaje', 0) > 0:
            self.datos.update(disponibilidad_mes)
        
        disponibilidad_localidad = self.mysql_extractor.get_disponibilidad_por_localidad(self.anio, self.mes)
        if disponibilidad_localidad:
            self.datos['disponibilidad_por_localidad'] = disponibilidad_localidad
        
        historico = self.mysql_extractor.get_historico_ans(12)
        if historico:
            self.datos['historico_ans'] = historico
        
        # Calcular disponibilidad y cumplimiento
        self.disponibilidad = self.datos.get('disponibilidad_porcentaje', 0)
        self.cumple_ans = self.disponibilidad >= UMBRAL_ANS
        
        # Agregar mes y año a los datos para compatibilidad
        self.datos['mes'] = config.MESES[self.mes]
        self.datos['anio'] = self.anio
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa los datos y retorna el contexto para el template"""
        # Esta clase no usa templates, pero debe implementar el método abstracto
        return {}
    
    def generar(self) -> Document:
        """
        Genera el documento completo de la Sección 3
        Sobrescribe el método de la clase base para usar python-docx directamente
        """
        # Cargar datos si no se han cargado
        if not self.datos:
            self.cargar_datos()
        
        # Crear documento
        self.doc = Document()
        self._configurar_estilos()
        
        # Título principal
        self.doc.add_heading("3. INFORMES DE MEDICIÓN DE NIVELES DE SERVICIO (ANS)", level=1)
        
        # Generar subsecciones
        self._seccion_3_1_penalidad_ans()
        self._seccion_3_2_consolidado_ans()
        
        # Separador fin de sección
        self.doc.add_paragraph()
        p = self.doc.add_paragraph("═" * 60)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        p = self.doc.add_paragraph("Fin Sección 3 - Informes de Medición de Niveles de Servicio (ANS)")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True
        p.runs[0].font.color.rgb = RGBColor(128, 128, 128)
        
        return self.doc
    
    def guardar(self, output_path: Path) -> None:
        """
        Genera y guarda la sección
        Sobrescribe el método de la clase base para usar python-docx
        """
        if self.doc is None:
            self.generar()
        
        self.doc.save(str(output_path))
        print(f"[OK] {self.nombre_seccion} guardada en: {output_path}")
