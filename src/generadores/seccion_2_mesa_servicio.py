"""
Generador Sección 2: Informe de Mesa de Servicio
Tipo: 🟨 ANÁLISIS IA + 🟩 EXTRACCIÓN DATOS (GLPI)

Subsecciones:
- 2.1 Informe de Mesa de Servicio
- 2.2 Herramientas de Trabajo
- 2.3 Visitas de Diagnósticos a Subsistemas
- 2.4 Informe Consolidado del Estado de los Tickets
- 2.5 Escalamientos (ENEL, Caída Masiva, Conectividad)
- 2.6 Informe Actualizado de Hojas de Vida
- 2.7 Informe Ejecutivo del Estado del Sistema
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
import json
from .base import GeneradorSeccion
import config
from src.extractores.glpi_extractor import get_glpi_extractor


class GeneradorSeccion2(GeneradorSeccion):
    """Genera la Sección 2: Informe de Mesa de Servicio"""
    
    # Colores ETB
    COLOR_AZUL_OSCURO = RGBColor(31, 78, 121)
    COLOR_AZUL_MEDIO = RGBColor(46, 117, 182)
    COLOR_GRIS = RGBColor(64, 64, 64)
    COLOR_VERDE = RGBColor(0, 128, 0)
    COLOR_ROJO = RGBColor(192, 0, 0)
    COLOR_AMARILLO = RGBColor(255, 192, 0)
    
    @property
    def nombre_seccion(self) -> str:
        return "2. INFORME DE MESA DE SERVICIO"
    
    @property
    def template_file(self) -> str:
        return "seccion_2_mesa_servicio.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.datos: Dict[str, Any] = {}
        self.doc: Optional[Document] = None
        self.glpi_extractor = get_glpi_extractor()
    
    def _configurar_estilos(self):
        """Configura los estilos del documento"""
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
                       colores_fila: list = None):
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
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in paragraph.runs:
                        run.font.size = Pt(10)
            
            # Aplicar color de fila si se especifica
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
    
    def _agregar_parrafo(self, texto: str, justificado: bool = True, negrita: bool = False):
        """Agrega un párrafo de texto"""
        p = self.doc.add_paragraph()
        run = p.add_run(texto)
        run.bold = negrita
        if justificado:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        return p
    
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
    
    def _generar_parrafo_ia(self, tipo: str) -> str:
        """
        Genera párrafos introductorios (placeholder para LLM)
        En producción, esto llamaría a un LLM para generar el texto
        """
        mes = config.MESES[self.mes]
        anio = self.anio
        
        plantillas = {
            "mesa_servicio": f"""Durante el mes de {mes} de {anio} se realizó el seguimiento constante a las actividades diarias relacionadas con la mesa de servicio, el centro de monitoreo (NUSE) y las actividades relacionadas con la operación del sistema de videovigilancia. Se mantuvieron los canales de comunicación activos con la interventoría y la supervisión del contrato, atendiendo oportunamente los requerimientos y solicitudes presentadas.""",
            
            "tickets": f"""Durante el mes de {mes} se gestionaron un total de {self.datos.get('total_tickets', 0)} tickets en el sistema GLPI. De estos, {self.datos.get('tickets_cerrados', 0)} fueron cerrados exitosamente, alcanzando una tasa de cierre del {self.datos.get('tasa_cierre', 0):.1f}%. Los subsistemas con mayor cantidad de incidencias fueron {self.datos.get('subsistema_mayor_incidencia', 'Domos Ciudadanos')}.""",
            
            "escalamiento_enel": f"""Durante el mes de {mes} de {anio} se realizaron escalamientos al operador de red ENEL por fallas en el suministro de energía eléctrica que afectaron la operatividad de los puntos de videovigilancia. Se gestionaron {self.datos.get('escalamientos_enel', 0)} casos de falla de energía.""",
            
            "caida_masiva": f"""Durante el mes de {mes} de {anio} {"se presentaron eventos de caída masiva que afectaron la disponibilidad del sistema" if self.datos.get('hubo_caida_masiva', False) else "no se presentaron eventos de caída masiva que afectaran significativamente la disponibilidad del sistema"}.""",
            
            "conectividad": f"""Durante el mes de {mes} de {anio} se realizaron escalamientos por fallas de conectividad al área técnica de ETB. Se gestionaron {self.datos.get('escalamientos_conectividad', 0)} casos relacionados con pérdida de comunicación en los puntos de videovigilancia.""",
            
            "estado_sistema": f"""Al cierre del mes de {mes} de {anio}, el sistema de videovigilancia presenta un total de {self.datos.get('camaras_operativas', 0)} cámaras operativas de un total de {self.datos.get('total_camaras', 0)} puntos, lo que representa una disponibilidad del {self.datos.get('disponibilidad_porcentaje', 0):.2f}%. Se encuentran {self.datos.get('camaras_no_operativas', 0)} cámaras no operativas y {self.datos.get('camaras_mantenimiento', 0)} en proceso de mantenimiento.""",
        }
        
        return plantillas.get(tipo, "")
    
    def _seccion_2_1_mesa_servicio(self):
        """2.1 Informe de Mesa de Servicio"""
        self.doc.add_heading("2.1. INFORME DE MESA DE SERVICIO", level=2)
        
        # Párrafo introductorio (IA)
        self._agregar_parrafo(self._generar_parrafo_ia("mesa_servicio"))
        
        # Tabla de informes enviados
        self._agregar_parrafo("A continuación se relacionan los informes enviados durante el periodo:", negrita=True)
        
        informes = self.datos.get('informes_mesa_servicio', [])
        if informes:
            filas = [[i['tipo'], i['fecha'], i['descripcion'], i['estado']] for i in informes]
            self._agregar_tabla(
                encabezados=["TIPO INFORME", "FECHA", "DESCRIPCIÓN", "ESTADO"],
                filas=filas,
                anchos=[1.5, 1.0, 3.5, 0.8]
            )
    
    def _seccion_2_2_herramientas(self):
        """2.2 Herramientas de Trabajo"""
        self.doc.add_heading("2.2. HERRAMIENTAS DE TRABAJO", level=2)
        
        texto_fijo = """El contratista cuenta con las siguientes herramientas para la gestión y operación del contrato:

• Sistema GLPI para la gestión de tickets e incidentes
• Plataforma de monitoreo de disponibilidad de cámaras
• Sistema VMS (Video Management System) para visualización de cámaras
• Herramientas de comunicación (correo, Teams, WhatsApp corporativo)
• Equipos de cómputo y dispositivos móviles para el personal de campo
• Vehículos y motocicletas para desplazamiento del personal técnico
• Equipos de medición y diagnóstico (multímetros, probadores de red, etc.)
• Herramientas manuales y equipos de protección personal"""
        
        self._agregar_parrafo(texto_fijo)
    
    def _seccion_2_3_visitas_diagnostico(self):
        """2.3 Visitas de Diagnósticos a Subsistemas"""
        self.doc.add_heading("2.3. VISITAS DE DIAGNÓSTICOS A SUBSISTEMAS", level=2)
        
        mes = config.MESES[self.mes]
        anio = self.anio
        
        self._agregar_parrafo(
            f"Durante el mes de {mes} de {anio} se realizaron visitas de diagnóstico a los diferentes "
            f"subsistemas del sistema de videovigilancia. A continuación se presenta el consolidado:"
        )
        
        visitas = self.datos.get('visitas_diagnostico', [])
        if visitas:
            filas = [[v['subsistema'], v['cantidad_visitas'], v['observaciones']] for v in visitas]
            self._agregar_tabla(
                encabezados=["SUBSISTEMA", "CANTIDAD VISITAS", "OBSERVACIONES"],
                filas=filas,
                anchos=[2.5, 1.2, 2.8]
            )
    
    def _seccion_2_4_tickets(self):
        """2.4 Informe Consolidado del Estado de los Tickets Administrativos"""
        self.doc.add_heading("2.4. INFORME CONSOLIDADO DEL ESTADO DE LOS TICKETS ADMINISTRATIVOS", level=2)
        
        # Párrafo resumen (IA)
        self._agregar_parrafo(self._generar_parrafo_ia("tickets"))
        
        # Tabla de tickets por proyecto
        self._agregar_parrafo("Tickets generados por proyecto:", negrita=True)
        
        tickets_proyecto = self.datos.get('tickets_por_proyecto', [])
        if tickets_proyecto:
            filas = [[t['proyecto'], t['generados'], t['cerrados'], t['abiertos']] for t in tickets_proyecto]
            self._agregar_tabla(
                encabezados=["PROYECTO", "GENERADOS", "CERRADOS", "ABIERTOS"],
                filas=filas,
                anchos=[3.0, 1.0, 1.0, 1.0]
            )
        
        # Tabla de tickets por estado
        self._agregar_parrafo("Tickets por estado:", negrita=True)
        
        tickets_estado = self.datos.get('tickets_por_estado', [])
        if tickets_estado:
            filas = [[t['estado'], t['cantidad'], f"{t['porcentaje']:.1f}%"] for t in tickets_estado]
            self._agregar_tabla(
                encabezados=["ESTADO", "CANTIDAD", "PORCENTAJE"],
                filas=filas,
                anchos=[3.0, 1.5, 1.5]
            )
        
        # Tabla de tickets por subsistema
        self._agregar_parrafo("Tickets por subsistema:", negrita=True)
        
        tickets_subsistema = self.datos.get('tickets_por_subsistema', [])
        if tickets_subsistema:
            filas = [[t['subsistema'], t['cantidad']] for t in tickets_subsistema]
            self._agregar_tabla(
                encabezados=["SUBSISTEMA", "CANTIDAD TICKETS"],
                filas=filas,
                anchos=[4.0, 2.0]
            )
    
    def _seccion_2_5_escalamientos(self):
        """2.5 Escalamientos"""
        self.doc.add_heading("2.5. ESCALAMIENTOS", level=2)
        
        # 2.5.1 ENEL
        self.doc.add_heading("2.5.1. ENEL", level=3)
        self._agregar_parrafo(self._generar_parrafo_ia("escalamiento_enel"))
        
        escalamientos_enel = self.datos.get('escalamientos_enel_detalle', [])
        if escalamientos_enel:
            filas = [[e['ticket'], e['localidad'], e['fecha'], e['descripcion'], e['estado']] 
                     for e in escalamientos_enel]
            self._agregar_tabla(
                encabezados=["TICKET", "LOCALIDAD", "FECHA", "DESCRIPCIÓN", "ESTADO"],
                filas=filas,
                anchos=[0.9, 1.2, 0.9, 2.5, 0.9]
            )
        else:
            self._agregar_parrafo("No se presentaron escalamientos a ENEL durante el periodo.")
        
        # 2.5.2 CAÍDA MASIVA
        self.doc.add_heading("2.5.2. CAÍDA MASIVA", level=3)
        self._agregar_parrafo(self._generar_parrafo_ia("caida_masiva"))
        
        caidas_masivas = self.datos.get('caidas_masivas', [])
        if caidas_masivas:
            for caida in caidas_masivas:
                self._agregar_parrafo(f"Evento del {caida['fecha']}:", negrita=True)
                self._agregar_parrafo(f"Descripción: {caida['descripcion']}")
                self._agregar_parrafo(f"Afectación: {caida['afectacion']}")
                self._agregar_parrafo(f"Causa: {caida['causa']}")
                self._agregar_parrafo(f"Acciones tomadas: {caida['acciones']}")
                self._agregar_parrafo(f"Tiempo de solución: {caida['tiempo_solucion']}")
        else:
            self._agregar_parrafo("No se presentaron eventos de caída masiva durante el periodo.")
        
        # 2.5.3 CONECTIVIDAD
        self.doc.add_heading("2.5.3. CONECTIVIDAD", level=3)
        self._agregar_parrafo(self._generar_parrafo_ia("conectividad"))
        
        escalamientos_conectividad = self.datos.get('escalamientos_conectividad_detalle', [])
        if escalamientos_conectividad:
            filas = [[e['ticket'], e['localidad'], e['fecha'], e['descripcion'], e['estado']] 
                     for e in escalamientos_conectividad]
            self._agregar_tabla(
                encabezados=["TICKET", "LOCALIDAD", "FECHA", "DESCRIPCIÓN", "ESTADO"],
                filas=filas,
                anchos=[0.9, 1.2, 0.9, 2.5, 0.9]
            )
        else:
            self._agregar_parrafo("No se presentaron escalamientos de conectividad durante el periodo.")
    
    def _seccion_2_6_hojas_vida(self):
        """2.6 Informe Actualizado de Hojas de Vida"""
        self.doc.add_heading("2.6. INFORME ACTUALIZADO DE HOJAS DE VIDA DE LOS PUNTOS Y SUBSISTEMAS", level=2)
        
        mes = config.MESES[self.mes]
        anio = self.anio
        
        self._agregar_parrafo(
            f"Durante el mes de {mes} de {anio} se mantuvieron actualizadas las hojas de vida de los "
            f"puntos de videovigilancia en el sistema GLPI. A continuación se presenta el estado de "
            f"actualización por subsistema:"
        )
        
        hojas_vida = self.datos.get('hojas_vida', [])
        if hojas_vida:
            filas = [[h['subsistema'], h['total_puntos'], h['actualizados'], 
                      f"{h['porcentaje_actualizado']:.1f}%"] for h in hojas_vida]
            self._agregar_tabla(
                encabezados=["SUBSISTEMA", "TOTAL PUNTOS", "ACTUALIZADOS", "% ACTUALIZACIÓN"],
                filas=filas,
                anchos=[2.5, 1.2, 1.2, 1.2]
            )
    
    def _seccion_2_7_estado_sistema(self):
        """2.7 Informe Ejecutivo del Estado del Sistema"""
        self.doc.add_heading("2.7. INFORME EJECUTIVO DEL ESTADO DEL SISTEMA", level=2)
        
        # Párrafo resumen (IA)
        self._agregar_parrafo(self._generar_parrafo_ia("estado_sistema"))
        
        # Tabla resumen del estado
        self._agregar_parrafo("Resumen del estado del sistema:", negrita=True)
        
        estado_sistema = self.datos.get('estado_sistema', {})
        filas = [
            ["Cámaras Operativas", estado_sistema.get('operativas', 0), 
             f"{estado_sistema.get('porcentaje_operativas', 0):.2f}%"],
            ["Cámaras No Operativas", estado_sistema.get('no_operativas', 0),
             f"{estado_sistema.get('porcentaje_no_operativas', 0):.2f}%"],
            ["En Mantenimiento", estado_sistema.get('mantenimiento', 0),
             f"{estado_sistema.get('porcentaje_mantenimiento', 0):.2f}%"],
            ["TOTAL", estado_sistema.get('total', 0), "100.00%"],
        ]
        
        # Colores para las filas según el estado
        colores = ["C6EFCE", "FFC7CE", "FFEB9C", "D9E1F2"]
        
        self._agregar_tabla(
            encabezados=["ESTADO", "CANTIDAD", "PORCENTAJE"],
            filas=filas,
            anchos=[2.5, 1.5, 1.5],
            colores_fila=colores
        )
        
        # Tabla por localidad
        self._agregar_parrafo("Estado por localidad:", negrita=True)
        
        estado_localidad = self.datos.get('estado_por_localidad', [])
        if estado_localidad:
            filas = [[l['localidad'], l['operativas'], l['no_operativas'], 
                      l['mantenimiento'], l['total']] for l in estado_localidad]
            self._agregar_tabla(
                encabezados=["LOCALIDAD", "OPERATIVAS", "NO OPERATIVAS", "MANTENIMIENTO", "TOTAL"],
                filas=filas,
                anchos=[2.0, 1.0, 1.0, 1.0, 0.8]
            )
    
    def cargar_datos(self) -> None:
        """Carga los datos específicos de la sección 2 desde JSON y GLPI"""
        # Cargar datos desde archivo JSON
        archivo = config.FUENTES_DIR / f"mesa_servicio_{self.mes}_{self.anio}.json"
        
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
        
        # Cargar datos desde GLPI (usando extractor)
        # Estos métodos pueden sobrescribir datos del JSON si están disponibles en GLPI
        tickets_proyecto = self.glpi_extractor.get_tickets_por_proyecto(self.mes, self.anio)
        if tickets_proyecto:
            self.datos['tickets_por_proyecto'] = tickets_proyecto
        
        tickets_estado = self.glpi_extractor.get_tickets_por_estado(self.mes, self.anio)
        if tickets_estado:
            self.datos['tickets_por_estado'] = tickets_estado
        
        tickets_subsistema = self.glpi_extractor.get_tickets_por_subsistema(self.mes, self.anio)
        if tickets_subsistema:
            self.datos['tickets_por_subsistema'] = tickets_subsistema
        
        escalamientos_enel = self.glpi_extractor.get_escalamientos_enel(self.mes, self.anio)
        if escalamientos_enel:
            self.datos['escalamientos_enel_detalle'] = escalamientos_enel
            self.datos['escalamientos_enel'] = len(escalamientos_enel)
        
        escalamientos_conectividad = self.glpi_extractor.get_escalamientos_conectividad(self.mes, self.anio)
        if escalamientos_conectividad:
            self.datos['escalamientos_conectividad_detalle'] = escalamientos_conectividad
            self.datos['escalamientos_conectividad'] = len(escalamientos_conectividad)
        
        # Calcular totales si no están en los datos
        if 'tickets_por_proyecto' in self.datos:
            total_generados = sum(t['generados'] for t in self.datos['tickets_por_proyecto'])
            total_cerrados = sum(t['cerrados'] for t in self.datos['tickets_por_proyecto'])
            self.datos['total_tickets'] = self.datos.get('total_tickets', total_generados)
            self.datos['tickets_cerrados'] = self.datos.get('tickets_cerrados', total_cerrados)
            if self.datos['total_tickets'] > 0:
                self.datos['tasa_cierre'] = (self.datos['tickets_cerrados'] / self.datos['total_tickets']) * 100
            else:
                self.datos['tasa_cierre'] = 0.0
        
        # Agregar mes y año a los datos para compatibilidad
        self.datos['mes'] = config.MESES[self.mes]
        self.datos['anio'] = self.anio
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa los datos y retorna el contexto para el template"""
        # Esta clase no usa templates, pero debe implementar el método abstracto
        return {}
    
    def generar(self) -> Document:
        """
        Genera el documento completo de la Sección 2
        Sobrescribe el método de la clase base para usar python-docx directamente
        """
        # Cargar datos si no se han cargado
        if not self.datos:
            self.cargar_datos()
        
        # Crear documento
        self.doc = Document()
        self._configurar_estilos()
        
        # Título principal
        self.doc.add_heading("2. INFORME DE MESA DE SERVICIO", level=1)
        
        # Generar cada subsección
        self._seccion_2_1_mesa_servicio()
        self._seccion_2_2_herramientas()
        self._seccion_2_3_visitas_diagnostico()
        self._seccion_2_4_tickets()
        self._seccion_2_5_escalamientos()
        self._seccion_2_6_hojas_vida()
        self._seccion_2_7_estado_sistema()
        
        # Separador fin de sección
        self.doc.add_paragraph()
        p = self.doc.add_paragraph("═" * 60)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        p = self.doc.add_paragraph("Fin Sección 2 - Informe de Mesa de Servicio")
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


