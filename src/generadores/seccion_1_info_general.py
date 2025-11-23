"""
Generador Sección 1: Información General del Contrato
Tipo: 🟦 CONTENIDO FIJO (mayoría) + 🟩 EXTRACCIÓN (comunicados, personal)
"""
from pathlib import Path
from typing import Dict, Any, List
import json
from .base import GeneradorSeccion
from src.utils.formato_moneda import formato_moneda_cop
import config

class GeneradorSeccion1(GeneradorSeccion):
    """Genera la sección 1: Información General del Contrato"""
    
    @property
    def nombre_seccion(self) -> str:
        return "1. INFORMACIÓN GENERAL DEL CONTRATO"
    
    @property
    def template_file(self) -> str:
        return "seccion_1_info_general.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.comunicados_emitidos: List[Dict] = []
        self.comunicados_recibidos: List[Dict] = []
        self.personal_minimo: List[Dict] = []
        self.personal_apoyo: List[Dict] = []
    
    def cargar_datos(self) -> None:
        """Carga datos fijos y variables de la sección 1"""
        # 1.1 - 1.5: Contenido fijo (ya está en config.CONTRATO)
        
        # 1.6: Comunicados (EXTRACCIÓN)
        self._cargar_comunicados()
        
        # 1.7 - 1.8: Personal (FIJO + EXTRACCIÓN)
        self._cargar_personal()
    
    def _cargar_comunicados(self) -> None:
        """Carga comunicados emitidos y recibidos del mes"""
        # TODO: Conectar con SharePoint o cargar de Excel
        # Por ahora, cargar de archivo JSON si existe
        archivo_comunicados = config.FUENTES_DIR / f"comunicados_{self.mes}_{self.anio}.json"
        
        if archivo_comunicados.exists():
            with open(archivo_comunicados, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.comunicados_emitidos = data.get("emitidos", [])
                self.comunicados_recibidos = data.get("recibidos", [])
        else:
            # Datos de ejemplo para desarrollo
            self.comunicados_emitidos = [
                {
                    "numero": "GSC-7444-2025",
                    "fecha": "23/09/2025",
                    "asunto": "INGRESOS ELEMENTOS ALMACÉN SEPTIEMBRE 2025",
                    "adjuntos": "Anexo_1.pdf"
                },
                {
                    "numero": "GSC-7445-2025", 
                    "fecha": "25/09/2025",
                    "asunto": "INFORME SEMANAL SEMANA 38",
                    "adjuntos": "Informe_S38.pdf"
                }
            ]
            self.comunicados_recibidos = [
                {
                    "numero": "ETB-2024-0892",
                    "fecha": "15/09/2025",
                    "asunto": "SOLICITUD INFORMACIÓN ADICIONAL",
                    "adjuntos": "-"
                }
            ]
    
    def _cargar_personal(self) -> None:
        """Carga información del personal del contrato"""
        archivo_personal = config.FIJOS_DIR / "personal_requerido.json"
        
        if archivo_personal.exists():
            with open(archivo_personal, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.personal_minimo = data.get("minimo", [])
                self.personal_apoyo = data.get("apoyo", [])
        else:
            # Estructura de ejemplo
            self.personal_minimo = [
                {"cargo": "Director de Proyecto", "cantidad": 1, "nombre": "Por definir"},
                {"cargo": "Coordinador Técnico", "cantidad": 1, "nombre": "Por definir"},
                {"cargo": "Ingeniero de Soporte", "cantidad": 2, "nombre": "Por definir"},
                {"cargo": "Técnico de Campo", "cantidad": 8, "nombre": "Por definir"},
            ]
            self.personal_apoyo = [
                {"cargo": "Técnico de Laboratorio", "cantidad": 2, "nombre": "Por definir"},
                {"cargo": "Auxiliar Administrativo", "cantidad": 1, "nombre": "Por definir"},
            ]
    
    def _cargar_contenido_fijo(self, archivo: str) -> str:
        """Carga contenido fijo desde archivo de texto"""
        ruta = config.FIJOS_DIR / archivo
        if ruta.exists():
            with open(ruta, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        # Texto introductorio oficial
        texto_intro = (
            f"Se celebra el número de proceso {config.CONTRATO['numero_proceso']} bajo número de contrato "
            f"{config.CONTRATO['numero']} con vigencia de doce (12) meses luego de suscripción de acta de inicio "
            f"suscrita el {self._formatear_fecha(config.CONTRATO['fecha_inicio'])}, fecha a partir de la cual el "
            f"sistema de video vigilancia de Bogotá D.C. queda con contrato de mantenimiento de videovigilancia. "
            f"Se detalla la información general del contrato."
        )
        
        return {
            # Texto introductorio
            "texto_intro": texto_intro,
            
            # TABLA 1: Información General del Contrato
            "tabla_1_info_general": {
                "nit": config.CONTRATO["nit_entidad"],
                "razon_social": config.CONTRATO["razon_social"],
                "ciudad": config.CONTRATO["ciudad"],
                "direccion": config.CONTRATO["direccion"],
                "telefono": config.CONTRATO["telefono"],
                "numero_contrato": config.CONTRATO["numero"],
                "fecha_inicio": self._formatear_fecha(config.CONTRATO["fecha_inicio"]),
                "plazo_ejecucion": config.CONTRATO["plazo_ejecucion"],
                "fecha_terminacion": self._formatear_fecha(config.CONTRATO["fecha_fin"]),
                "valor_inicial": formato_moneda_cop(config.CONTRATO["valor_inicial"]),
                "adicion_1": formato_moneda_cop(config.CONTRATO["adicion_1"]),
                "valor_total": formato_moneda_cop(config.CONTRATO["valor_total"]),
                "objeto": config.CONTRATO["objeto"],
                "fecha_firma_acta": self._formatear_fecha(config.CONTRATO["fecha_inicio"]),
                "fecha_suscripcion": self._formatear_fecha(config.CONTRATO["fecha_suscripcion"]),
                "vigencia_poliza_inicial": f"{self._formatear_fecha(config.CONTRATO['vigencia_poliza_inicial_inicio'])} {self._formatear_fecha(config.CONTRATO['vigencia_poliza_inicial_fin'])}",
                "vigencia_poliza_acta": f"{self._formatear_fecha(config.CONTRATO['vigencia_poliza_acta_inicio'])} {self._formatear_fecha(config.CONTRATO['vigencia_poliza_acta_fin'])}",
            },
            
            # 1.1 Objeto del contrato (FIJO)
            "objeto_contrato": config.CONTRATO["objeto_corto"],
            
            # 1.2 Alcance (FIJO)
            "alcance": self._cargar_contenido_fijo("alcance.txt"),
            
            # 1.3 Descripción infraestructura (FIJO + TABLAS)
            "descripcion_infraestructura": self._cargar_contenido_fijo("infraestructura.txt"),
            "subsistemas": config.SUBSISTEMAS,
            "tabla_componentes": self._cargar_tabla_componentes(),
            "tabla_centros_monitoreo": self._cargar_tabla_centros_monitoreo(),
            "tabla_forma_pago": self._cargar_tabla_forma_pago(),
            
            # 1.4 Glosario (FIJO)
            "glosario": self._cargar_glosario(),
            
            # 1.5 Obligaciones (FIJO)
            "obligaciones_generales": self._cargar_contenido_fijo("obligaciones_generales.txt"),
            "obligaciones_especificas": self._cargar_contenido_fijo("obligaciones_especificas.txt"),
            "obligaciones_ambientales": self._cargar_contenido_fijo("obligaciones_ambientales.txt"),
            "obligaciones_anexos": self._cargar_contenido_fijo("obligaciones_anexos.txt"),
            
            # 1.6 Comunicados (EXTRACCIÓN)
            "comunicados_emitidos": self.comunicados_emitidos,
            "comunicados_recibidos": self.comunicados_recibidos,
            "total_comunicados_emitidos": len(self.comunicados_emitidos),
            "total_comunicados_recibidos": len(self.comunicados_recibidos),
            
            # 1.7 - 1.8 Personal (FIJO estructura + EXTRACCIÓN datos)
            "personal_minimo": self.personal_minimo,
            "personal_apoyo": self.personal_apoyo,
        }
    
    def _cargar_glosario(self) -> List[Dict[str, str]]:
        """Carga el glosario de términos"""
        archivo = config.FIJOS_DIR / "glosario.json"
        if archivo.exists():
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Glosario por defecto
        return [
            {"termino": "ANS", "definicion": "Acuerdo de Nivel de Servicio"},
            {"termino": "CCTV", "definicion": "Circuito Cerrado de Televisión"},
            {"termino": "DVR", "definicion": "Digital Video Recorder"},
            {"termino": "NVR", "definicion": "Network Video Recorder"},
            {"termino": "GLPI", "definicion": "Gestionnaire Libre de Parc Informatique"},
            {"termino": "NUSE", "definicion": "Número Único de Seguridad y Emergencias"},
        ]
    
    def _formatear_fecha(self, fecha_str: str) -> str:
        """Formatea fecha YYYY-MM-DD a formato DD DE MES DE YYYY"""
        from datetime import datetime
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            meses = {
                1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
                5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
                9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
            }
            return f"{fecha.day} de {meses[fecha.month]} de {fecha.year}"
        except:
            return fecha_str
    
    def _cargar_tabla_componentes(self) -> List[Dict]:
        """Carga tabla de componentes por subsistema"""
        # Datos según el informe oficial de Septiembre 2025
        return [
            {
                "sistema": "CIUDADANA",
                "ubicaciones": 4451,
                "puntos_camara": 4451,
                "centros_monitoreo_c4": 4451,
                "visualizadas_localmente": 0
            },
            {
                "sistema": "COLEGIOS",
                "ubicaciones": 98,
                "puntos_camara": 235,
                "centros_monitoreo_c4": 235,
                "visualizadas_localmente": 0
            },
            {
                "sistema": "TRANSMILENIO",
                "ubicaciones": 71,
                "puntos_camara": 164,
                "centros_monitoreo_c4": 164,
                "visualizadas_localmente": 0
            },
            {
                "sistema": "CAI",
                "ubicaciones": 157,
                "puntos_camara": 510,
                "centros_monitoreo_c4": 89,
                "visualizadas_localmente": 421
            },
            {
                "sistema": "ESTADIO EL CAMPIN",
                "ubicaciones": 1,
                "puntos_camara": 58,
                "centros_monitoreo_c4": 0,
                "visualizadas_localmente": 58
            },
            {
                "sistema": "CTP",
                "ubicaciones": 1,
                "puntos_camara": 104,
                "centros_monitoreo_c4": 0,
                "visualizadas_localmente": 104
            },
            {
                "sistema": "ESTACIONES DE POLICÍA",
                "ubicaciones": 24,
                "puntos_camara": 302,
                "centros_monitoreo_c4": 0,
                "visualizadas_localmente": 302
            },
            {
                "sistema": "TOTAL",
                "ubicaciones": 4803,
                "puntos_camara": 5824,
                "centros_monitoreo_c4": 4939,
                "visualizadas_localmente": 885
            }
        ]
    
    def _cargar_tabla_centros_monitoreo(self) -> List[Dict]:
        """Carga tabla de centros de monitoreo"""
        return [
            {"numero": 1, "nombre": "CENTRO DE COMANDO, CONTROL, CÓMPUTO Y COMUNICACIONES - C4", "direccion": "CALLE 20 NO 68 A 06", "localidad": "PUENTE ARANDA"},
            {"numero": 2, "nombre": "CENTRO DE MONITOREO ENGATIVÁ", "direccion": "KR 78A NO. 70 – 54", "localidad": "ENGATIVÁ"},
            {"numero": 3, "nombre": "CENTRO DE MONITOREO BARRIOS UNIDOS", "direccion": "ESTACIÓN POLICÍA CALLE 72 # 62-81", "localidad": "BARRIOS UNIDOS"},
            {"numero": 4, "nombre": "CENTRO DE MONITOREO TEUSAQUILLO", "direccion": "ESTACIÓN POLICÍA CRA 13 # 39-86", "localidad": "TEUSAQUILLO"},
            {"numero": 5, "nombre": "CENTRO DE MONITOREO KENNEDY", "direccion": "TRANSVERSAL 78 K CON CALLE 41 D SUR", "localidad": "KENNEDY"},
            {"numero": 6, "nombre": "CENTRO DE MONITOREO CHAPINERO", "direccion": "KR 1 CALLE 57-00", "localidad": "CHAPINERO"},
            {"numero": 7, "nombre": "CENTRO DE MONITOREO CIUDAD BOLÍVAR", "direccion": "DIAGONAL 70 SUR CON TRANSVERSAL 54", "localidad": "CIUDAD BOLÍVAR"},
            {"numero": 8, "nombre": "CENTRO DE MONITOREO PUENTE ARANDA", "direccion": "CRA 39 CON CALLE 10", "localidad": "PUENTE ARANDA"},
            {"numero": 9, "nombre": "CENTRO DE MONITOREO USAQUÉN", "direccion": "CL. 165 #8A-99", "localidad": "USAQUÉN"},
            {"numero": 10, "nombre": "CENTRO DE MONITOREO RAFAEL URIBE", "direccion": "Calle 27 Sur #24-39", "localidad": "RAFAEL URIBE URIBE"},
            {"numero": 11, "nombre": "CENTRO DE MONITOREO SANTA FE", "direccion": "Carrera 5 # 29-11", "localidad": "SANTA FE"},
        ]
    
    def _cargar_tabla_forma_pago(self) -> List[Dict]:
        """Carga tabla de forma de pago"""
        return [
            {
                "numero": 1,
                "descripcion": "Mantenimientos preventivos por UBICACIÓN, aprobados mediante cronograma con interventoría / supervisión.",
                "tipo_servicio": "Por Demanda"
            },
            {
                "numero": 2,
                "descripcion": "Servicio de mantenimiento correctivo y soporte al sistema de video vigilancia de Bogotá",
                "tipo_servicio": "Mensualidad"
            },
            {
                "numero": 3,
                "descripcion": "Bolsa de repuestos, elementos aprobados por interventoría / supervisión.",
                "tipo_servicio": "Por Demanda"
            }
        ]


