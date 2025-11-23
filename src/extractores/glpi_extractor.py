"""
Extractor de datos del sistema GLPI
"""
from typing import List, Dict, Any
from datetime import datetime
import json
from pathlib import Path
import config


class GLPIExtractor:
    """Extrae datos del sistema GLPI"""
    
    def __init__(self, api_url: str = None, api_token: str = None):
        """Inicializa el extractor con configuración de API"""
        self.api_url = api_url or getattr(config, 'GLPI_API_URL', None)
        self.api_token = api_token or getattr(config, 'GLPI_API_TOKEN', None)
    
    def get_tickets_por_proyecto(self, mes: int, año: int) -> List[Dict]:
        """Tickets agrupados por proyecto"""
        # Por ahora retorna datos de ejemplo
        # TODO: Implementar query real a GLPI
        datos_json = self._cargar_datos_desde_json(mes, año, "tickets_por_proyecto", None)
        if datos_json:
            return datos_json
        
        # Datos de ejemplo si no hay JSON
        return [
            {"proyecto": "CIUDADANA", "generados": 150, "cerrados": 145, "abiertos": 5},
            {"proyecto": "COLEGIOS", "generados": 25, "cerrados": 24, "abiertos": 1},
            {"proyecto": "TRANSMILENIO", "generados": 18, "cerrados": 18, "abiertos": 0},
        ]
    
    def get_tickets_por_estado(self, mes: int, año: int) -> List[Dict]:
        """Tickets agrupados por estado"""
        datos_json = self._cargar_datos_desde_json(mes, año, "tickets_por_estado", None)
        if datos_json:
            return datos_json
        
        # Datos de ejemplo si no hay JSON
        return [
            {"estado": "CERRADO", "cantidad": 198, "porcentaje": 91.7},
            {"estado": "EN PROCESO", "cantidad": 12, "porcentaje": 5.6},
            {"estado": "PENDIENTE", "cantidad": 5, "porcentaje": 2.3},
            {"estado": "ESCALADO", "cantidad": 1, "porcentaje": 0.5},
        ]
    
    def get_tickets_por_subsistema(self, mes: int, año: int) -> List[Dict]:
        """Tickets agrupados por subsistema"""
        datos_json = self._cargar_datos_desde_json(mes, año, "tickets_por_subsistema", None)
        if datos_json:
            return datos_json
        
        # Datos de ejemplo si no hay JSON
        return [
            {"subsistema": "DOMO PTZ", "cantidad": 80, "porcentaje": 37.2},
            {"subsistema": "CÁMARA FIJA", "cantidad": 65, "porcentaje": 30.2},
            {"subsistema": "DVR/NVR", "cantidad": 45, "porcentaje": 20.9},
            {"subsistema": "RED/COMUNICACIÓN", "cantidad": 25, "porcentaje": 11.6},
        ]
    
    def get_escalamientos_enel(self, mes: int, año: int) -> List[Dict]:
        """Escalamientos a ENEL"""
        datos_json = self._cargar_datos_desde_json(mes, año, "escalamientos_enel_detalle", None)
        if datos_json:
            return datos_json
        
        # Datos de ejemplo si no hay JSON
        return [
            {
                "fecha": "2025-09-05",
                "punto": "SCJ17E100029",
                "localidad": "ENGATIVÁ",
                "direccion": "KR 78A NO. 70-54",
                "tiempo_resolucion": "4h 30m"
            },
        ]
    
    def get_escalamientos_conectividad(self, mes: int, año: int) -> List[Dict]:
        """Escalamientos por conectividad"""
        datos_json = self._cargar_datos_desde_json(mes, año, "escalamientos_conectividad_detalle", None)
        if datos_json:
            return datos_json
        
        # Datos de ejemplo si no hay JSON
        return [
            {
                "fecha": "2025-09-08",
                "punto": "COL-2849",
                "localidad": "KENNEDY",
                "descripcion": "Pérdida de enlace RF",
                "tiempo_resolucion": "3h 20m"
            },
        ]
    
    def _cargar_datos_desde_json(self, mes: int, año: int, campo: str, default: Any = None) -> Any:
        """
        Carga datos desde archivo JSON de fuentes
        
        Args:
            mes: Mes (1-12)
            año: Año (ej: 2025)
            campo: Nombre del campo a extraer del JSON
            default: Valor por defecto si no se encuentra
        
        Returns:
            Valor del campo o default
        """
        archivo = config.FUENTES_DIR / f"mesa_servicio_{mes}_{año}.json"
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get(campo, default)
            except Exception as e:
                print(f"[WARNING] Error al cargar {archivo}: {e}")
                return default
        
        return default


# Singleton
_glpi_extractor_instance = None

def get_glpi_extractor() -> GLPIExtractor:
    """Retorna instancia singleton"""
    global _glpi_extractor_instance
    if _glpi_extractor_instance is None:
        _glpi_extractor_instance = GLPIExtractor()
    return _glpi_extractor_instance
