"""
Generador Sección 1: Información General del Contrato
Tipo: 🟦 CONTENIDO FIJO (mayoría) + 🟩 EXTRACCIÓN (comunicados, personal)
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import os
from .base import GeneradorSeccion
from src.utils.formato_moneda import formato_moneda_cop
from src.ia.extractor_observaciones import get_extractor_observaciones
import config

class GeneradorSeccion1(GeneradorSeccion):
    """Genera la sección 1: Información General del Contrato"""
    
    @property
    def nombre_seccion(self) -> str:
        return "1. INFORMACIÓN GENERAL DEL CONTRATO"
    
    @property
    def template_file(self) -> str:
        return "seccion_1_info_general.docx"
    
    def __init__(self, anio: int, mes: int, usar_llm_observaciones: bool = True):
        super().__init__(anio, mes)
        self.comunicados_emitidos: List[Dict] = []
        self.comunicados_recibidos: List[Dict] = []
        self.personal_minimo: List[Dict] = []
        self.personal_apoyo: List[Dict] = []
        self.obligaciones_generales_raw: List[Dict] = []
        self.obligaciones_especificas_raw: List[Dict] = []
        self.obligaciones_ambientales_raw: List[Dict] = []
        self.obligaciones_anexos_raw: List[Dict] = []
        self.usar_llm_observaciones = usar_llm_observaciones
        self.extractor_observaciones = None
        if usar_llm_observaciones:
            try:
                # Obtener credenciales de SharePoint desde config (que ya carga del .env)
                sharepoint_site_url = getattr(config, 'SHAREPOINT_SITE_URL', None) or os.getenv("SHAREPOINT_SITE_URL")
                sharepoint_client_id = getattr(config, 'SHAREPOINT_CLIENT_ID', None) or os.getenv("SHAREPOINT_CLIENT_ID")
                sharepoint_client_secret = getattr(config, 'SHAREPOINT_CLIENT_SECRET', None) or os.getenv("SHAREPOINT_CLIENT_SECRET")
                sharepoint_base_path = getattr(config, 'SHAREPOINT_BASE_PATH', None) or os.getenv("SHAREPOINT_BASE_PATH")
                
                self.extractor_observaciones = get_extractor_observaciones(
                    sharepoint_site_url=sharepoint_site_url,
                    sharepoint_client_id=sharepoint_client_id,
                    sharepoint_client_secret=sharepoint_client_secret,
                    sharepoint_base_path=sharepoint_base_path
                )
            except Exception as e:
                print(f"[WARNING] No se pudo inicializar extractor de observaciones: {e}")
                self.usar_llm_observaciones = False
    
    def cargar_datos(self) -> None:
        """Carga datos fijos y variables de la sección 1"""
        # 1.1 - 1.5: Contenido fijo (ya está en config.CONTRATO)
        
        # 1.5: Obligaciones (EXTRACCIÓN + LLM para observaciones)
        self._cargar_obligaciones()
        
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
    
    def _cargar_obligaciones(self) -> None:
        """Carga obligaciones desde JSON y genera observaciones dinámicas con LLM"""
        # Intentar cargar desde archivo JSON mensual
        archivo_obligaciones = config.FUENTES_DIR / f"obligaciones_{self.mes}_{self.anio}.json"
        if not archivo_obligaciones.exists():
            archivo_obligaciones = config.FUENTES_DIR / f"obligaciones_{config.MESES[self.mes].lower()}_{self.anio}.json"
        
        if archivo_obligaciones.exists():
            try:
                with open(archivo_obligaciones, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.obligaciones_generales_raw = data.get("obligaciones_generales", [])
                    self.obligaciones_especificas_raw = data.get("obligaciones_especificas", [])
                    self.obligaciones_ambientales_raw = data.get("obligaciones_ambientales", [])
                    self.obligaciones_anexos_raw = data.get("obligaciones_anexos", [])
                    
                    # Generar observaciones dinámicas si está habilitado
                    if self.usar_llm_observaciones and self.extractor_observaciones:
                        print("[INFO] Generando observaciones dinámicas desde anexos usando LLM...")
                        self.obligaciones_generales_raw = [
                            self.extractor_observaciones.procesar_obligacion(obl)
                            for obl in self.obligaciones_generales_raw
                        ]
                        self.obligaciones_especificas_raw = [
                            self.extractor_observaciones.procesar_obligacion(obl)
                            for obl in self.obligaciones_especificas_raw
                        ]
                        self.obligaciones_ambientales_raw = [
                            self.extractor_observaciones.procesar_obligacion(obl)
                            for obl in self.obligaciones_ambientales_raw
                        ]
                        self.obligaciones_anexos_raw = [
                            self.extractor_observaciones.procesar_obligacion(obl)
                            for obl in self.obligaciones_anexos_raw
                        ]
            except Exception as e:
                print(f"[WARNING] Error al cargar obligaciones desde {archivo_obligaciones}: {e}")
        else:
            print(f"[INFO] Archivo de obligaciones no encontrado: {archivo_obligaciones}")
            # Las listas quedan vacías - se usarán datos fijos del texto
    
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
            
            # TABLA 1: Información General del Contrato (formato lista para docxtpl)
            "tabla_1_filas": self._formatear_tabla_1(),
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
            
            # Variables para textos de anexos (opcionales)
            "ruta_acta_inicio": self._obtener_ruta_acta_inicio(),
            "numero_adicion": self._obtener_numero_adicion(),
            "ruta_poliza": self._obtener_ruta_poliza(),
            
            # 1.1 Objeto del contrato (FIJO)
            "objeto_contrato": config.CONTRATO["objeto_corto"],
            
            # 1.2 Alcance (FIJO)
            "alcance": self._cargar_contenido_fijo("alcance.txt"),
            
            # 1.3 Descripción infraestructura (FIJO + TABLAS)
            "descripcion_infraestructura": self._cargar_contenido_fijo("infraestructura.txt"),
            "subsistemas": config.SUBSISTEMAS,
            "componentes": self._cargar_tabla_componentes(),  # Renombrado para consistencia
            "centros": self._cargar_tabla_centros_monitoreo(),  # Renombrado para consistencia
            "forma_pago": self._cargar_tabla_forma_pago(),  # Renombrado para consistencia
            "tabla_componentes": self._cargar_tabla_componentes(),  # Mantener compatibilidad
            "tabla_centros_monitoreo": self._cargar_tabla_centros_monitoreo(),  # Mantener compatibilidad
            "tabla_forma_pago": self._cargar_tabla_forma_pago(),  # Mantener compatibilidad
            "nota_infraestructura": self._obtener_nota_infraestructura(),
            
            # 1.4 Glosario (FIJO)
            "glosario": self._cargar_glosario(),
            "glosario_tablas": self._formatear_glosario_tablas(),
            
            # 1.5 Obligaciones (FIJO texto + DINÁMICO tablas)
            "obligaciones_generales": self._cargar_contenido_fijo("obligaciones_generales.txt"),
            "obligaciones_especificas": self._cargar_contenido_fijo("obligaciones_especificas.txt"),
            "obligaciones_ambientales": self._cargar_contenido_fijo("obligaciones_ambientales.txt"),
            "obligaciones_anexos": self._cargar_contenido_fijo("obligaciones_anexos.txt"),
            
            # Tablas de obligaciones (DINÁMICAS - con cumplimiento)
            "tabla_obligaciones_generales": self._formatear_obligaciones_generales(),
            "tabla_obligaciones_especificas": self._formatear_obligaciones_especificas(),
            "tabla_obligaciones_ambientales": self._formatear_obligaciones_ambientales(),
            "tabla_obligaciones_anexos": self._formatear_obligaciones_anexos(),
            
            # 1.6 Comunicados (EXTRACCIÓN)
            "comunicados_emitidos": self.comunicados_emitidos,
            "comunicados_recibidos": self.comunicados_recibidos,
            "total_comunicados_emitidos": len(self.comunicados_emitidos),
            "total_comunicados_recibidos": len(self.comunicados_recibidos),
            "tabla_comunicados_emitidos": self._formatear_comunicados_emitidos(),
            "tabla_comunicados_recibidos": self._formatear_comunicados_recibidos(),
            
            # 1.7 - 1.8 Personal (FIJO estructura + EXTRACCIÓN datos)
            "personal_minimo": self.personal_minimo,
            "personal_apoyo": self.personal_apoyo,
            "tabla_personal_minimo": self._formatear_personal_minimo(),
            "tabla_personal_apoyo": self._formatear_personal_apoyo(),
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
                "numero": 1,
                "sistema": "CIUDADANA",
                "ubicaciones": 4451,
                "puntos_camara": 4451,
                "centros_monitoreo_c4": 4451,
                "visualizadas_localmente": 0
            },
            {
                "numero": 2,
                "sistema": "COLEGIOS",
                "ubicaciones": 98,
                "puntos_camara": 235,
                "centros_monitoreo_c4": 235,
                "visualizadas_localmente": 0
            },
            {
                "numero": 3,
                "sistema": "TRANSMILENIO",
                "ubicaciones": 71,
                "puntos_camara": 164,
                "centros_monitoreo_c4": 164,
                "visualizadas_localmente": 0
            },
            {
                "numero": 4,
                "sistema": "CAI",
                "ubicaciones": 157,
                "puntos_camara": 510,
                "centros_monitoreo_c4": 89,
                "visualizadas_localmente": 421
            },
            {
                "numero": 5,
                "sistema": "ESTADIO EL CAMPIN",
                "ubicaciones": 1,
                "puntos_camara": 58,
                "centros_monitoreo_c4": 0,
                "visualizadas_localmente": 58
            },
            {
                "numero": 6,
                "sistema": "CTP",
                "ubicaciones": 1,
                "puntos_camara": 104,
                "centros_monitoreo_c4": 0,
                "visualizadas_localmente": 104
            },
            {
                "numero": 7,
                "sistema": "ESTACIONES DE POLICÍA",
                "ubicaciones": 24,
                "puntos_camara": 302,
                "centros_monitoreo_c4": 0,
                "visualizadas_localmente": 302
            },
            {
                "numero": 8,
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
    
    def _formatear_tabla_1(self) -> List[Dict[str, str]]:
        """Formatea la tabla 1 como lista de filas (Campo | Valor)"""
        return [
            {"campo": "NIT", "valor": config.CONTRATO["nit_entidad"]},
            {"campo": "RAZÓN SOCIAL", "valor": config.CONTRATO["razon_social"]},
            {"campo": "CIUDAD", "valor": config.CONTRATO["ciudad"]},
            {"campo": "DIRECCIÓN", "valor": config.CONTRATO["direccion"]},
            {"campo": "TELÉFONO", "valor": config.CONTRATO["telefono"]},
            {"campo": "NÚMERO DE CONTRATO", "valor": config.CONTRATO["numero"]},
            {"campo": "FECHA DE INICIO", "valor": self._formatear_fecha(config.CONTRATO["fecha_inicio"])},
            {"campo": "PLAZO DE EJECUCIÓN", "valor": config.CONTRATO["plazo_ejecucion"]},
            {"campo": "FECHA DE TERMINACIÓN", "valor": self._formatear_fecha(config.CONTRATO["fecha_fin"])},
            {"campo": "VALOR INICIAL", "valor": formato_moneda_cop(config.CONTRATO["valor_inicial"])},
            {"campo": "ADICIÓN N° 01", "valor": formato_moneda_cop(config.CONTRATO["adicion_1"])},
            {"campo": "VALOR TOTAL", "valor": formato_moneda_cop(config.CONTRATO["valor_total"])},
            {"campo": "OBJETO", "valor": config.CONTRATO["objeto"]},
            {"campo": "FECHA FIRMA ACTA DE INICIO", "valor": self._formatear_fecha(config.CONTRATO["fecha_inicio"])},
            {"campo": "FECHA DE SUSCRIPCIÓN", "valor": self._formatear_fecha(config.CONTRATO["fecha_suscripcion"])},
            {"campo": "VIGENCIA PÓLIZA INICIAL", "valor": f"{self._formatear_fecha(config.CONTRATO['vigencia_poliza_inicial_inicio'])} - {self._formatear_fecha(config.CONTRATO['vigencia_poliza_inicial_fin'])}"},
            {"campo": "VIGENCIA PÓLIZA ACTA DE INICIO", "valor": f"{self._formatear_fecha(config.CONTRATO['vigencia_poliza_acta_inicio'])} - {self._formatear_fecha(config.CONTRATO['vigencia_poliza_acta_fin'])}"},
        ]
    
    def _formatear_comunicados_emitidos(self) -> List[Dict]:
        """Formatea comunicados emitidos para tabla (ÍTEM, FECHA, CONSECUTIVO ETB, DESCRIPCIÓN)"""
        return [
            {
                "item": i+1,
                "fecha": com.get("fecha", ""),
                "consecutivo": com.get("numero", ""),
                "descripcion": com.get("asunto", "")
            }
            for i, com in enumerate(self.comunicados_emitidos)
        ]
    
    def _formatear_comunicados_recibidos(self) -> List[Dict]:
        """Formatea comunicados recibidos para tabla (ÍTEM, FECHA, CONSECUTIVO ETB, DESCRIPCIÓN)"""
        return [
            {
                "item": i+1,
                "fecha": com.get("fecha", ""),
                "consecutivo": com.get("numero", ""),
                "descripcion": com.get("asunto", "")
            }
            for i, com in enumerate(self.comunicados_recibidos)
        ]
    
    def _formatear_personal_minimo(self) -> List[Dict]:
        """Formatea personal mínimo para tabla"""
        return [
            {
                "cargo": p.get("cargo", ""),
                "cantidad": p.get("cantidad", 0),
                "nombre": p.get("nombre", "Por definir")
            }
            for p in self.personal_minimo
        ]
    
    def _formatear_personal_apoyo(self) -> List[Dict]:
        """Formatea personal de apoyo para tabla"""
        return [
            {
                "cargo": p.get("cargo", ""),
                "cantidad": p.get("cantidad", 0),
                "nombre": p.get("nombre", "Por definir")
            }
            for p in self.personal_apoyo
        ]
    
    def _formatear_glosario_tablas(self) -> List[Dict]:
        """Formatea glosario para múltiples tablas (se divide en grupos)"""
        glosario = self._cargar_glosario()
        # Retornar lista completa - el template dividirá en tablas si es necesario
        return glosario
    
    def _formatear_obligaciones_generales(self) -> List[Dict]:
        """Formatea obligaciones generales para tabla con cumplimiento"""
        # Retornar obligaciones cargadas (ya procesadas con observaciones)
        return self.obligaciones_generales_raw
    
    def _formatear_obligaciones_especificas(self) -> List[Dict]:
        """Formatea obligaciones específicas para tabla con cumplimiento"""
        return self.obligaciones_especificas_raw
    
    def _formatear_obligaciones_ambientales(self) -> List[Dict]:
        """Formatea obligaciones ambientales para tabla con cumplimiento"""
        return self.obligaciones_ambientales_raw
    
    def _formatear_obligaciones_anexos(self) -> List[Dict]:
        """Formatea obligaciones anexos para tabla con cumplimiento"""
        return self.obligaciones_anexos_raw
    
    def _obtener_ruta_acta_inicio(self) -> str:
        """Obtiene la ruta del acta de inicio (dinámico según mes)"""
        mes_nombre = config.MESES[self.mes]
        return f"01{mes_nombre[:3].upper()} - 30{mes_nombre[:3].upper()}/ 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 2,5,6,9,13/ ANEXOS OTROS/ SCJ-1809-2024 ACTA DE INICIO.PDF"
    
    def _obtener_numero_adicion(self) -> str:
        """Obtiene el número de adición si aplica (dinámico)"""
        # TODO: Cargar desde fuente de datos o config
        return "01"  # Por defecto
    
    def _obtener_ruta_poliza(self) -> str:
        """Obtiene la ruta de modificación de póliza si aplica (dinámico)"""
        mes_nombre = config.MESES[self.mes]
        return f"01{mes_nombre[:3].upper()} - 30{mes_nombre[:3].upper()} / 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 4/ ANEXOS OTROS/ MODIFICACIÓN PÓLIZA.PDF"
    
    def _obtener_nota_infraestructura(self) -> str:
        """Obtiene nota adicional sobre infraestructura si aplica (dinámico)"""
        # Ejemplo: "Se aclara que se desmonta La Estación de Transmilenio Calle 26 con 12 cámaras por obras del metro"
        # TODO: Cargar desde fuente de datos
        return ""


