"""
Repositorio para guardar y consultar datos de laboratorio en MongoDB
"""
from datetime import datetime
from typing import Dict, Any, Optional, List
from src.services.database import get_database
import logging

logger = logging.getLogger(__name__)


class LaboratorioRepository:
    """Repositorio para operaciones de laboratorio en MongoDB"""
    
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
        """Obtiene la base de datos MongoDB (lazy loading)"""
        if not self._is_mongodb_available():
            return None
        return self._db
    
    @property
    def collection(self):
        """Obtiene la colección de laboratorio (lazy loading)"""
        if self._collection is None and self.db is not None:
            self._collection = self.db["laboratorio"]
        return self._collection
    
    async def guardar_datos_laboratorio(
        self,
        anio: int,
        mes: int,
        datos_laboratorio: List[Dict[str, Any]],
        user_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Guarda o actualiza los datos de laboratorio en MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            datos_laboratorio: Lista de registros de laboratorio
            user_id: ID del usuario que realiza la operación
            
        Returns:
            Documento guardado o actualizado, o None si MongoDB no está disponible
        """
        # Verificar si MongoDB está disponible
        if not self._is_mongodb_available() or self.collection is None:
            logger.warning("MongoDB no está configurado o no está disponible. No se guardará en MongoDB.")
            return None
        
        try:
            # Construir filtro para buscar documento existente
            filtro = {
                "anio": anio,
                "mes": mes,
                "seccion": 5
            }
            
            # Construir documento a guardar
            documento = {
                "anio": anio,
                "mes": mes,
                "seccion": 5,
                "datos_laboratorio": datos_laboratorio,
                "updated_at": datetime.utcnow(),
                "total_registros": len(datos_laboratorio)
            }
            
            # Agregar metadatos de usuario
            if user_id:
                documento["user_updated"] = user_id
                # Si es nuevo documento, también agregar user_created
                documento_existente = await self.collection.find_one(filtro)
                if not documento_existente:
                    documento["user_created"] = user_id
                    documento["created_at"] = datetime.utcnow()
            
            # Actualizar o insertar
            resultado = await self.collection.update_one(
                filtro,
                {"$set": documento},
                upsert=True
            )
            
            if resultado.upserted_id:
                logger.info(f"Datos de laboratorio guardados (nuevo documento) para {anio}-{mes}")
            else:
                logger.info(f"Datos de laboratorio actualizados para {anio}-{mes}")
            
            # Retornar el documento guardado
            documento_guardado = await self.collection.find_one(filtro)
            return documento_guardado
            
        except Exception as e:
            logger.error(f"Error al guardar datos de laboratorio en MongoDB: {e}", exc_info=True)
            return None
    
    async def obtener_datos_laboratorio(
        self,
        anio: int,
        mes: int
    ) -> Optional[Dict[str, Any]]:
        """
        Obtiene los datos de laboratorio desde MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            
        Returns:
            Documento con los datos de laboratorio o None si no existe o MongoDB no está disponible
        """
        # Verificar si MongoDB está disponible
        if not self._is_mongodb_available() or self.collection is None:
            logger.warning("MongoDB no está configurado o no está disponible.")
            return None
        
        try:
            filtro = {
                "anio": anio,
                "mes": mes,
                "seccion": 5
            }
            
            documento = await self.collection.find_one(filtro)
            
            if documento:
                logger.info(f"Datos de laboratorio encontrados para {anio}-{mes}")
            else:
                logger.info(f"No se encontraron datos de laboratorio para {anio}-{mes}")
            
            return documento
            
        except Exception as e:
            logger.error(f"Error al obtener datos de laboratorio desde MongoDB: {e}", exc_info=True)
            raise
    
    async def eliminar_datos_laboratorio(
        self,
        anio: int,
        mes: int
    ) -> bool:
        """
        Elimina los datos de laboratorio de MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            
        Returns:
            True si se eliminó, False si no existía o MongoDB no está disponible
        """
        # Verificar si MongoDB está disponible
        if not self._is_mongodb_available() or self.collection is None:
            logger.warning("MongoDB no está configurado o no está disponible.")
            return False
        
        try:
            filtro = {
                "anio": anio,
                "mes": mes,
                "seccion": 5
            }
            
            resultado = await self.collection.delete_one(filtro)
            
            if resultado.deleted_count > 0:
                logger.info(f"Datos de laboratorio eliminados para {anio}-{mes}")
                return True
            else:
                logger.info(f"No se encontraron datos de laboratorio para eliminar: {anio}-{mes}")
                return False
                
        except Exception as e:
            logger.error(f"Error al eliminar datos de laboratorio desde MongoDB: {e}", exc_info=True)
            raise

