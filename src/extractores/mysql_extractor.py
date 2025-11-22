"""
Extractor de datos de disponibilidad desde MySQL
Base de datos de monitoreo de cámaras
"""
from typing import Dict, List, Optional
from datetime import datetime, date
from calendar import monthrange
import json
from pathlib import Path
import config


class MySQLExtractor:
    """Extrae datos de disponibilidad del sistema de monitoreo"""
    
    def __init__(self, config_db: dict = None):
        """
        Args:
            config_db: Diccionario con host, user, password, database
        """
        self.config_db = config_db or {}
        self.connection = None
    
    def conectar(self):
        """Establece conexión con MySQL"""
        # TODO: Implementar conexión real
        # try:
        #     self.connection = mysql.connector.connect(
        #         host=self.config_db.get('host'),
        #         user=self.config_db.get('user'),
        #         password=self.config_db.get('password'),
        #         database=self.config_db.get('database')
        #     )
        # except mysql.connector.Error as e:
        #     print(f"[ERROR] Error al conectar a MySQL: {e}")
        #     raise
        pass
    
    def desconectar(self):
        """Cierra la conexión con MySQL"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def calcular_horas_mes(self, anio: int, mes: int) -> int:
        """Calcula las horas totales del mes"""
        dias = monthrange(anio, mes)[1]
        return dias * 24
    
    def get_disponibilidad_mes(self, anio: int, mes: int) -> dict:
        """
        Calcula la disponibilidad del mes
        
        Returns:
            {
                "horas_totales_mes": 720,
                "horas_operativas": 712.8,
                "horas_no_operativas": 7.2,
                "disponibilidad_porcentaje": 99.12
            }
        """
        # TODO: Query real a la base de datos
        # if not self.connection:
        #     self.conectar()
        # 
        # cursor = self.connection.cursor(dictionary=True)
        # query = """
        #     SELECT 
        #         SUM(horas_operativas) as horas_op,
        #         SUM(horas_no_operativas) as horas_no_op
        #     FROM disponibilidad_diaria
        #     WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s
        # """
        # cursor.execute(query, (anio, mes))
        # result = cursor.fetchone()
        # cursor.close()
        # 
        # horas_op = result['horas_op'] or 0
        # horas_no_op = result['horas_no_op'] or 0
        # horas_totales = self.calcular_horas_mes(anio, mes)
        # disponibilidad = (horas_op / (horas_op + horas_no_op)) * 100 if (horas_op + horas_no_op) > 0 else 0
        # 
        # return {
        #     "horas_totales_mes": horas_totales,
        #     "horas_operativas": horas_op,
        #     "horas_no_operativas": horas_no_op,
        #     "disponibilidad_porcentaje": disponibilidad
        # }
        
        # Por ahora, cargar desde archivo JSON si existe
        return self._cargar_datos_desde_json(anio, mes, "disponibilidad_mes", {
            "horas_totales_mes": self.calcular_horas_mes(anio, mes),
            "horas_operativas": 0,
            "horas_no_operativas": 0,
            "disponibilidad_porcentaje": 0
        })
    
    def get_disponibilidad_por_localidad(self, anio: int, mes: int) -> List[dict]:
        """
        Obtiene disponibilidad desglosada por localidad
        
        Returns:
            [
                {
                    "localidad": "Kennedy",
                    "total_camaras": 192,
                    "horas_operativas": 137980,
                    "horas_no_operativas": 580,
                    "disponibilidad": 99.58
                },
                ...
            ]
        """
        # TODO: Query real
        # if not self.connection:
        #     self.conectar()
        # 
        # cursor = self.connection.cursor(dictionary=True)
        # query = """
        #     SELECT 
        #         localidad,
        #         COUNT(DISTINCT id_camara) as total_camaras,
        #         SUM(horas_operativas) as horas_op,
        #         SUM(horas_no_operativas) as horas_no_op,
        #         (SUM(horas_operativas) / (SUM(horas_operativas) + SUM(horas_no_operativas))) * 100 as disponibilidad
        #     FROM disponibilidad_diaria
        #     WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s
        #     GROUP BY localidad
        #     ORDER BY disponibilidad DESC
        # """
        # cursor.execute(query, (anio, mes))
        # results = cursor.fetchall()
        # cursor.close()
        # 
        # return results
        
        # Por ahora, cargar desde archivo JSON si existe
        return self._cargar_datos_desde_json(anio, mes, "disponibilidad_por_localidad", [])
    
    def get_historico_ans(self, meses_atras: int = 12) -> List[dict]:
        """
        Obtiene el histórico de ANS de los últimos N meses
        
        Returns:
            [
                {"mes": "Enero 2025", "disponibilidad": 99.05, "observaciones": "-"},
                ...
            ]
        """
        # TODO: Query real
        # if not self.connection:
        #     self.conectar()
        # 
        # cursor = self.connection.cursor(dictionary=True)
        # query = """
        #     SELECT 
        #         DATE_FORMAT(fecha, '%%M %%Y') as mes,
        #         (SUM(horas_operativas) / (SUM(horas_operativas) + SUM(horas_no_operativas))) * 100 as disponibilidad
        #     FROM disponibilidad_diaria
        #     WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
        #     GROUP BY YEAR(fecha), MONTH(fecha)
        #     ORDER BY YEAR(fecha), MONTH(fecha)
        # """
        # cursor.execute(query, (meses_atras,))
        # results = cursor.fetchall()
        # cursor.close()
        # 
        # return [{"mes": r['mes'], "disponibilidad": r['disponibilidad'], "observaciones": "-"} for r in results]
        
        # Por ahora, cargar desde archivo JSON si existe
        return self._cargar_datos_desde_json(None, None, "historico_ans", [])
    
    def _cargar_datos_desde_json(self, anio: Optional[int], mes: Optional[int], campo: str, default: any) -> any:
        """
        Carga datos desde archivo JSON de fuentes
        
        Args:
            anio: Año (puede ser None para histórico)
            mes: Mes (puede ser None para histórico)
            campo: Nombre del campo a extraer del JSON
            default: Valor por defecto si no se encuentra
        
        Returns:
            Valor del campo o default
        """
        if anio and mes:
            archivo = config.FUENTES_DIR / f"ans_{mes}_{anio}.json"
        else:
            # Para histórico, buscar el archivo más reciente
            archivo = config.FUENTES_DIR / "ans_septiembre_2025.json"  # Por defecto
        
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

def get_mysql_extractor(config_db: dict = None) -> MySQLExtractor:
    """Obtiene la instancia singleton del extractor MySQL"""
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = MySQLExtractor(config_db)
    return _extractor_instance
