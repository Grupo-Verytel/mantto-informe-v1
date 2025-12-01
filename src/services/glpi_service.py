import os
import aiomysql
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class GLPIService:
    
    def __init__(self):
        self.host = os.getenv("GLPI_MYSQL_HOST", "")
        self.port = int(os.getenv("GLPI_MYSQL_PORT", "3306"))
        self.user = os.getenv("GLPI_MYSQL_USER", "")
        self.password = os.getenv("GLPI_MYSQL_PASSWORD", "")
        self.database = os.getenv("GLPI_MYSQL_DATABASE", "glpi")
        self.pool: Optional[aiomysql.Pool] = None
        
    async def connect(self) -> bool:
        try:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.database,
                minsize=1,
                maxsize=10,
                autocommit=True
            )
            logger.info(f"Conectado a MySQL GLPI: {self.database}@{self.host}")
            return True
            
        except Exception as e:
            logger.error(f"Error al conectar a MySQL GLPI: {str(e)}")
            raise
    
    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None
    
    async def get_actividades_por_subsistema(self, anio: int, mes: int) -> List[Dict[str, Any]]:
        if not self.pool:
            await self.connect()
        
        query = """
        SELECT 
            l.building AS subsistema,
            SUM(CASE WHEN t.itilcategories_id = 72 THEN 1 ELSE 0 END) AS diagnostico,
            SUM(CASE WHEN t.itilcategories_id = 75 THEN 1 ELSE 0 END) AS diagnostico_subsistema,
            SUM(CASE WHEN t.itilcategories_id = 70 THEN 1 ELSE 0 END) AS limpieza_acrilico,
            SUM(CASE WHEN t.itilcategories_id = 76 THEN 1 ELSE 0 END) AS mto_acometida,
            SUM(CASE WHEN t.itilcategories_id = 69 THEN 1 ELSE 0 END) AS mto_correctivo,
            SUM(CASE WHEN t.itilcategories_id = 77 THEN 1 ELSE 0 END) AS mto_correctivo_subsistema,
            SUM(CASE WHEN t.itilcategories_id = 74 THEN 1 ELSE 0 END) AS plan_de_choque,
            SUM(
                CASE WHEN t.itilcategories_id IN (72,75,70,76,69,77,74) 
                     THEN 1 ELSE 0 END
            ) AS total
        FROM glpi_tickets t
        INNER JOIN glpi_locations l ON l.id = t.locations_id
        INNER JOIN glpi_itilcategories c ON c.id = t.itilcategories_id
        WHERE t.is_deleted = 0
          AND l.building IS NOT NULL
          AND l.building != ''
          AND YEAR(t.date) = %s 
          AND MONTH(t.date) = %s
        GROUP BY l.building
        ORDER BY l.building ASC        
        """
        
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, (anio, mes))
                    results = await cursor.fetchall()
                    
                    formatted_results = []
                    for row in results:
                        formatted_results.append({
                            "subsistema": str(row.get("subsistema", "")),
                            "diagnostico": str(row.get("diagnostico", 0)),
                            "diagnostico_subsistema": str(row.get("diagnostico_subsistema", 0)),
                            "limpieza_acrilico": str(row.get("limpieza_acrilico", 0)),
                            "mto_acometida": str(row.get("mto_acometida", 0)),
                            "mto_correctivo": str(row.get("mto_correctivo", 0)),
                            "mto_correctivo_subsistema": str(row.get("mto_correctivo_subsistema", 0)),
                            "plan_de_choque": str(row.get("plan_de_choque", 0)),
                            "total": str(row.get("total", 0))
                        })
                    
                    return formatted_results
                    
        except Exception as e:
            logger.error(f"Error al ejecutar query MySQL GLPI: {str(e)}")
            raise
    
    async def get_visitas_diagnostico_subsistemas(self, anio: int, mes: int) -> List[Dict[str, Any]]:
        """
        Obtiene las visitas de diagnóstico a subsistemas desde MySQL de GLPI.
        
        Args:
            anio: Año (ej: 2025)
            mes: Mes (1-12)
            
        Returns:
            Lista de visitas de diagnóstico por subsistema
        """
        if not self.pool:
            await self.connect()
        
        # TODO: Reemplazar con el query real que el usuario proporcionará
        query = """
        SELECT 
            l.building AS subsistema,
            COUNT(*) AS ejecutadas
        FROM glpi_tickets t
        INNER JOIN glpi_locations l ON l.id = t.locations_id
        INNER JOIN glpi_itilcategories c on c.id = t.itilcategories_id
        WHERE t.is_deleted = 0
          AND c.id = 75
          AND l.building IS NOT NULL
          AND l.building != ''
          AND YEAR(t.date) = %s 
          AND MONTH(t.date) = %s
        GROUP BY l.building
        ORDER BY l.building ASC
        """
        
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, (anio, mes))
                    results = await cursor.fetchall()
                    
                    formatted_results = []
                    for row in results:
                        formatted_results.append({
                            "subsistema": str(row.get("subsistema", "")),
                            "ejecutadas": str(row.get("ejecutadas", 0))
                        })
                    
                    return formatted_results
                    
        except Exception as e:
            logger.error(f"Error al ejecutar query MySQL GLPI para visitas de diagnóstico: {str(e)}")
            raise
    
    async def get_estado_tickets_por_subsistema(self, anio: int, mes: int) -> List[Dict[str, Any]]:
        """
        Obtiene el estado de los tickets por subsistema agrupados por estado.
        
        Args:
            anio: Año (ej: 2025)
            mes: Mes (1-12)
            
        Returns:
            Lista de tickets por subsistema con sus estados
        """
        if not self.pool:
            await self.connect()
        
        query = """
        SELECT 
            l.building AS subsistema,
            SUM(CASE WHEN t.status = 1 THEN 1 ELSE 0 END) AS nuevo,
            SUM(CASE WHEN t.status = 2 THEN 1 ELSE 0 END) AS en_curso_asignada,
            SUM(CASE WHEN t.status = 3 THEN 1 ELSE 0 END) AS en_curso_planificada,
            SUM(CASE WHEN t.status = 4 THEN 1 ELSE 0 END) AS en_espera,
            SUM(CASE WHEN t.status = 5 THEN 1 ELSE 0 END) AS resueltas,
            SUM(CASE WHEN t.status = 6 THEN 1 ELSE 0 END) AS cerrado,
            COUNT(*) AS total
        FROM glpi_tickets t
        INNER JOIN glpi_locations l ON l.id = t.locations_id
        WHERE t.is_deleted = 0
          AND l.building IS NOT NULL
          AND l.building != ''
          AND YEAR(t.date) = %s
          AND MONTH(t.date) = %s
        GROUP BY l.building
        ORDER BY l.building ASC
        """
        
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, (anio, mes))
                    results = await cursor.fetchall()
                    
                    formatted_results = []
                    for row in results:
                        formatted_results.append({
                            "subsistema": str(row.get("subsistema", "")),
                            "cerrado": str(row.get("cerrado", 0)),
                            "en_curso_asignada": str(row.get("en_curso_asignada", 0)),
                            "en_curso_planificada": str(row.get("en_curso_planificada", 0)),
                            "en_espera": str(row.get("en_espera", 0)),
                            "resueltas": str(row.get("resueltas", 0)),
                            "total": str(row.get("total", 0))
                        })
                    
                    return formatted_results
                    
        except Exception as e:
            logger.error(f"Error al ejecutar query MySQL GLPI para estado de tickets: {str(e)}")
            raise


_glpi_service_instance: Optional[GLPIService] = None


async def get_glpi_service() -> GLPIService:
    global _glpi_service_instance
    if _glpi_service_instance is None:
        _glpi_service_instance = GLPIService()
    return _glpi_service_instance


async def close_glpi_service():
    global _glpi_service_instance
    if _glpi_service_instance:
        await _glpi_service_instance.close()
        _glpi_service_instance = None
