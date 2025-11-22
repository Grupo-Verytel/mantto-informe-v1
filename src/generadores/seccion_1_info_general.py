"""
Generador Sección 1: Información General del Contrato
Tipo: 🟦 CONTENIDO FIJO (mayoría) + 🟩 EXTRACCIÓN (comunicados, personal)
"""
from pathlib import Path
from typing import Dict, Any, List
import json
from .base import GeneradorSeccion
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
        return {
            # 1.1 Objeto del contrato (FIJO)
            "objeto_contrato": self.contrato["objeto"],
            
            # 1.2 Alcance (FIJO)
            "alcance": self._cargar_contenido_fijo("alcance.txt"),
            
            # 1.3 Descripción infraestructura (FIJO)
            "descripcion_infraestructura": self._cargar_contenido_fijo("infraestructura.txt"),
            "subsistemas": config.SUBSISTEMAS,
            
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


