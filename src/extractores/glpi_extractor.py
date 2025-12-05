"""
Extractor de datos del sistema GLPI
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
from pathlib import Path
import config
from ..services.glpi_service import get_glpi_service, GLPIService
import logging

logger = logging.getLogger(__name__)


class GLPIExtractor:
    """Extrae datos del sistema GLPI"""
    
    def __init__(self, glpi_service: Optional[GLPIService] = None):
        """
        Inicializa el extractor con servicio GLPI
        
        Args:
            glpi_service: Instancia del servicio GLPI (opcional)
        """
        self.glpi_service = glpi_service
        self._use_mysql = bool(
            os.getenv("GLPI_MYSQL_HOST") and 
            os.getenv("GLPI_MYSQL_USER") and 
            os.getenv("GLPI_MYSQL_PASSWORD")
        )
    
    async def get_tickets_por_proyecto(self, mes: int, año: int) -> List[Dict]:
        """
        Tickets agrupados por proyecto
        
        Args:
            mes: Mes (1-12)
            año: Año
            
        Returns:
            Lista de tickets agrupados por proyecto
        """
        # Intentar cargar desde JSON primero
        datos_json = self._cargar_datos_desde_json(mes, año, "tickets_por_proyecto", None)
        if datos_json:
            return datos_json
        
        # Datos de ejemplo si no hay JSON
        return [
            {"proyecto": "CIUDADANA", "generados": 150, "cerrados": 145, "abiertos": 5},
            {"proyecto": "COLEGIOS", "generados": 25, "cerrados": 24, "abiertos": 1},
            {"proyecto": "TRANSMILENIO", "generados": 18, "cerrados": 18, "abiertos": 0},
        ]
    
    def _agrupar_tickets_por_proyecto(self, tickets: List[Dict]) -> List[Dict]:
        """Agrupa tickets por proyecto"""
        proyectos = {}
        for ticket in tickets:
            proyecto = ticket.get("project", {}).get("name", "SIN PROYECTO")
            if proyecto not in proyectos:
                proyectos[proyecto] = {"generados": 0, "cerrados": 0, "abiertos": 0}
            
            proyectos[proyecto]["generados"] += 1
            estado = ticket.get("status", 0)
            if estado == 6:  # Cerrado
                proyectos[proyecto]["cerrados"] += 1
            else:
                proyectos[proyecto]["abiertos"] += 1
        
        return [{"proyecto": k, **v} for k, v in proyectos.items()]
    
    async def get_tickets_por_estado(self, mes: int, año: int) -> List[Dict]:
        """
        Tickets agrupados por estado
        
        Args:
            mes: Mes (1-12)
            año: Año
            
        Returns:
            Lista de tickets agrupados por estado
        """
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
    
    def _agrupar_tickets_por_estado(self, tickets: List[Dict]) -> List[Dict]:
        """Agrupa tickets por estado"""
        estados_map = {
            1: "NUEVO",
            2: "ASIGNADO",
            3: "EN PROCESO",
            4: "PENDIENTE",
            5: "RESUELTO",
            6: "CERRADO"
        }
        
        estados = {}
        total = len(tickets)
        
        for ticket in tickets:
            estado_id = ticket.get("status", 0)
            estado_nombre = estados_map.get(estado_id, f"ESTADO_{estado_id}")
            estados[estado_nombre] = estados.get(estado_nombre, 0) + 1
        
        resultado = []
        for estado, cantidad in estados.items():
            porcentaje = (cantidad / total * 100) if total > 0 else 0
            resultado.append({
                "estado": estado,
                "cantidad": cantidad,
                "porcentaje": round(porcentaje, 1)
            })
        
        return resultado
    
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
    
    async def get_actividades_por_subsistema(self, mes: int, año: int) -> List[Dict]:
        """
        Obtiene actividades agrupadas por subsistema desde MySQL de GLPI
        
        Args:
            mes: Mes (1-12)
            año: Año (ej: 2025)
            
        Returns:
            Lista de actividades por subsistema
        """
        # Intentar cargar desde JSON primero
        datos_json = self._cargar_datos_desde_json(mes, año, "actividades_por_subsistema", None)
        if datos_json:
            return datos_json
        
        # Si hay servicio MySQL configurado, obtener datos reales
        if self._use_mysql and self.glpi_service:
            try:
                actividades = await self.glpi_service.get_actividades_por_subsistema(año, mes)
                logger.info(f"Obtenidas {len(actividades)} actividades desde MySQL GLPI")
                return actividades
            except Exception as e:
                logger.warning(f"Error al obtener actividades de MySQL GLPI: {e}. Usando datos de ejemplo.")
        
        # Datos de ejemplo si no hay MySQL ni JSON
        return [
            {
                "subsistema": "Domos Ciudadanos",
                "diagnostico": "15",
                "diagnostico_subsistema": "8",
                "limpieza_acrilico": "12",
                "mto_acometida": "5",
                "mto_correctivo": "20",
                "mto_correctivo_subsistema": "10",
                "plan_de_choque": "3",
                "total": "73"
            }
        ]


# Singleton
_glpi_extractor_instance: Optional[GLPIExtractor] = None


async def get_glpi_extractor() -> GLPIExtractor:
    """
    Retorna instancia singleton del extractor GLPI
    
    Returns:
        Instancia de GLPIExtractor
    """
    global _glpi_extractor_instance
    if _glpi_extractor_instance is None:
        glpi_service = await get_glpi_service() if os.getenv("GLPI_MYSQL_HOST") else None
        _glpi_extractor_instance = GLPIExtractor(glpi_service=glpi_service)
    return _glpi_extractor_instance
