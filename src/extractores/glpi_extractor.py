"""
Extractor de datos de GLPI
TODO: Implementar conexión a API de GLPI real
"""
from typing import List, Dict, Any
from datetime import datetime
import json
from pathlib import Path
import config


class GLPIExtractor:
    """Extractor de datos de GLPI para el informe de mesa de servicio"""
    
    def __init__(self):
        """Inicializa el extractor"""
        # TODO: Agregar configuración de conexión a GLPI
        # self.api_url = config.GLPI_API_URL
        # self.api_token = config.GLPI_API_TOKEN
        pass
    
    def get_tickets_por_proyecto(self, mes: int, anio: int) -> List[Dict[str, Any]]:
        """
        Obtiene tickets agrupados por proyecto para un mes y año específicos
        
        Args:
            mes: Mes (1-12)
            anio: Año (ej: 2025)
        
        Returns:
            Lista de diccionarios con formato:
            [
                {
                    "proyecto": "Mantenimiento Preventivo",
                    "generados": 120,
                    "cerrados": 120,
                    "abiertos": 0
                },
                ...
            ]
        """
        # TODO: Implementar conexión a API de GLPI
        # Por ahora, cargar desde archivo JSON si existe
        return self._cargar_datos_desde_json(mes, anio, "tickets_por_proyecto", [])
    
    def get_tickets_por_estado(self, mes: int, anio: int) -> List[Dict[str, Any]]:
        """
        Obtiene tickets agrupados por estado para un mes y año específicos
        
        Args:
            mes: Mes (1-12)
            anio: Año (ej: 2025)
        
        Returns:
            Lista de diccionarios con formato:
            [
                {
                    "estado": "Cerrado",
                    "cantidad": 498,
                    "porcentaje": 91.9
                },
                ...
            ]
        """
        # TODO: Implementar conexión a API de GLPI
        return self._cargar_datos_desde_json(mes, anio, "tickets_por_estado", [])
    
    def get_tickets_por_subsistema(self, mes: int, anio: int) -> List[Dict[str, Any]]:
        """
        Obtiene tickets agrupados por subsistema para un mes y año específicos
        
        Args:
            mes: Mes (1-12)
            anio: Año (ej: 2025)
        
        Returns:
            Lista de diccionarios con formato:
            [
                {
                    "subsistema": "Domos Ciudadanos",
                    "cantidad": 285
                },
                ...
            ]
        """
        # TODO: Implementar conexión a API de GLPI
        return self._cargar_datos_desde_json(mes, anio, "tickets_por_subsistema", [])
    
    def get_escalamientos_enel(self, mes: int, anio: int) -> List[Dict[str, Any]]:
        """
        Obtiene escalamientos a ENEL para un mes y año específicos
        
        Args:
            mes: Mes (1-12)
            anio: Año (ej: 2025)
        
        Returns:
            Lista de diccionarios con formato:
            [
                {
                    "ticket": "TK-4521",
                    "localidad": "Kennedy",
                    "fecha": "08/09/2025",
                    "descripcion": "Falla de energía sector Patio Bonito",
                    "estado": "Cerrado"
                },
                ...
            ]
        """
        # TODO: Implementar conexión a API de GLPI
        return self._cargar_datos_desde_json(mes, anio, "escalamientos_enel_detalle", [])
    
    def get_escalamientos_conectividad(self, mes: int, anio: int) -> List[Dict[str, Any]]:
        """
        Obtiene escalamientos de conectividad para un mes y año específicos
        
        Args:
            mes: Mes (1-12)
            anio: Año (ej: 2025)
        
        Returns:
            Lista de diccionarios con formato:
            [
                {
                    "ticket": "TK-4533",
                    "localidad": "Chapinero",
                    "fecha": "05/09/2025",
                    "descripcion": "Pérdida de enlace de fibra",
                    "estado": "Cerrado"
                },
                ...
            ]
        """
        # TODO: Implementar conexión a API de GLPI
        return self._cargar_datos_desde_json(mes, anio, "escalamientos_conectividad_detalle", [])
    
    def _cargar_datos_desde_json(self, mes: int, anio: int, campo: str, default: Any = None) -> Any:
        """
        Carga datos desde archivo JSON de fuentes
        
        Args:
            mes: Mes (1-12)
            anio: Año (ej: 2025)
            campo: Nombre del campo a extraer del JSON
            default: Valor por defecto si no se encuentra
        
        Returns:
            Valor del campo o default
        """
        archivo = config.FUENTES_DIR / f"mesa_servicio_{mes}_{anio}.json"
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get(campo, default)
            except Exception as e:
                print(f"[WARNING] Error al cargar {archivo}: {e}")
                return default
        
        return default


# Instancia global del extractor
_extractor_instance = None

def get_glpi_extractor() -> GLPIExtractor:
    """Obtiene la instancia singleton del extractor GLPI"""
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = GLPIExtractor()
    return _extractor_instance
