"""
Repository para operaciones de MongoDB relacionadas con comunicados emitidos
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from src.services.database import get_database

logger = logging.getLogger(__name__)


class ComunicadosRepository:
    """Repository para operaciones de MongoDB relacionadas con comunicados"""
    
    def __init__(self):
        self._db = None
        self._collection = None
    
    def _is_mongodb_available(self) -> bool:
        """Verifica si MongoDB está disponible"""
        if self._db is None:
            try:
                self._db = get_database()
                return True
            except (ValueError, Exception) as e:
                logger.debug(f"MongoDB no está disponible: {e}")
                self._db = None
                return False
        return True
    
    @property
    def db(self):
        """Obtiene la base de datos de MongoDB (lazy loading)"""
        if not self._is_mongodb_available():
            return None
        return self._db
    
    @property
    def collection(self):
        """Obtiene la colección de comunicados (lazy loading)"""
        if self._collection is None and self.db is not None:
            self._collection = self.db["comunicados"]
        return self._collection
    
    async def guardar_comunicados(
        self,
        comunicados: List[Dict[str, Any]],
        anio: int,
        mes: int,
        seccion: int = 1,
        subseccion: str = "1.6.1",
        tipo: str = "emitidos",
        user_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Guarda o actualiza comunicados emitidos en MongoDB
        
        Args:
            comunicados: Lista de comunicados procesados
            anio: Año del informe
            mes: Mes del informe
            seccion: Número de sección
            subseccion: Subsección (ej: "1.6.1")
            user_id: ID del usuario que realiza la operación (opcional)
            
        Returns:
            Documento guardado en MongoDB o None si falla
        """
        if not self._is_mongodb_available() or self.collection is None:
            logger.warning("MongoDB no está configurado o no está disponible. No se guardará en MongoDB.")
            return None
        
        try:
            # Crear documento para MongoDB
            campo_comunicados = f"comunicados_{tipo}"
            documento = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion,
                "subseccion": subseccion,
                campo_comunicados: comunicados,
                "fecha_actualizacion": datetime.utcnow(),
                "user_id": user_id
            }
            
            # Buscar si ya existe un documento para este año, mes, sección y subsección
            filtro = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion,
                "subseccion": subseccion
            }
            
            # Actualizar o insertar
            resultado = await self.collection.update_one(
                filtro,
                {"$set": documento},
                upsert=True
            )
            
            if resultado.upserted_id:
                documento["_id"] = resultado.upserted_id
                logger.info(f"Comunicados guardados en MongoDB (nuevo documento): {resultado.upserted_id}")
            else:
                logger.info(f"Comunicados actualizados en MongoDB para {anio}-{mes}, sección {seccion}, subsección {subseccion}")
                # Obtener el documento actualizado
                documento_actualizado = await self.collection.find_one(filtro)
                if documento_actualizado:
                    documento["_id"] = documento_actualizado["_id"]
            
            return documento
            
        except Exception as e:
            logger.error(f"Error al guardar comunicados en MongoDB: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def obtener_comunicados(
        self,
        anio: int,
        mes: int,
        seccion: int = 1,
        subseccion: str = "1.6.1"
    ) -> Optional[Dict[str, Any]]:
        """
        Obtiene comunicados desde MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe
            seccion: Número de sección
            subseccion: Subsección (ej: "1.6.1")
            
        Returns:
            Documento de MongoDB o None si no existe
        """
        if not self._is_mongodb_available() or self.collection is None:
            logger.warning("MongoDB no está configurado o no está disponible.")
            return None
        
        try:
            filtro = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion,
                "subseccion": subseccion
            }
            
            documento = await self.collection.find_one(filtro)
            return documento
            
        except Exception as e:
            logger.error(f"Error al obtener comunicados desde MongoDB: {e}")
            return None
    
    async def eliminar_comunicados(
        self,
        anio: int,
        mes: int,
        seccion: int = 1,
        subseccion: str = "1.6.1"
    ) -> bool:
        """
        Elimina comunicados de MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe
            seccion: Número de sección
            subseccion: Subsección (ej: "1.6.1")
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        if not self._is_mongodb_available() or self.collection is None:
            logger.warning("MongoDB no está configurado o no está disponible.")
            return False
        
        try:
            filtro = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion,
                "subseccion": subseccion
            }
            
            resultado = await self.collection.delete_one(filtro)
            return resultado.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error al eliminar comunicados de MongoDB: {e}")
            return False

