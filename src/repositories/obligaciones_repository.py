"""
Repositorio para guardar y consultar obligaciones en MongoDB
"""
from datetime import datetime
from typing import Dict, Any, Optional, List
from src.services.database import get_database
import logging

logger = logging.getLogger(__name__)


class ObligacionesRepository:
    """Repositorio para operaciones de obligaciones en MongoDB"""
    
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
        """Obtiene la colección de obligaciones (lazy loading)"""
        if self._collection is None and self.db is not None:
            self._collection = self.db["obligaciones"]
        return self._collection
    
    async def guardar_obligaciones(
        self,
        anio: int,
        mes: int,
        seccion: int,
        subseccion: Optional[str],
        obligaciones_data: Dict[str, Any],
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Guarda o actualiza las obligaciones en MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            seccion: Número de sección (1)
            subseccion: Subsección (ej: "1.5.1", "1.5.2", etc.) o None para todas
            obligaciones_data: Datos de las obligaciones procesadas
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
                "seccion": seccion
            }
            
            # Si hay subsección, incluirla en el filtro
            if subseccion:
                filtro["subseccion"] = subseccion
            
            # Construir documento a guardar
            documento = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion,
                "updated_at": datetime.now()
            }
            
            # Agregar subsección si existe
            if subseccion:
                documento["subseccion"] = subseccion
            
            # Agregar obligaciones según el tipo
            for key, value in obligaciones_data.items():
                if key.startswith("obligaciones_"):
                    documento[key] = value
            
            # Agregar metadatos de usuario
            if user_id:
                documento["user_updated"] = user_id
                # Si es nuevo documento, también agregar user_created
                documento_existente = await self.collection.find_one(filtro)
                if not documento_existente:
                    documento["user_created"] = user_id
                    documento["created_at"] = datetime.now()
            
            # Actualizar o insertar
            resultado = await self.collection.update_one(
                filtro,
                {"$set": documento},
                upsert=True
            )
            
            if resultado.upserted_id:
                logger.info(f"Obligaciones guardadas (nuevo documento) para {anio}-{mes}, sección {seccion}, subsección {subseccion}")
            else:
                logger.info(f"Obligaciones actualizadas para {anio}-{mes}, sección {seccion}, subsección {subseccion}")
            
            # Retornar el documento guardado
            documento_guardado = await self.collection.find_one(filtro)
            return documento_guardado
            
        except Exception as e:
            logger.warning(f"Error al guardar obligaciones en MongoDB: {e}")
            # No lanzar excepción, solo registrar warning
            return None
    
    async def obtener_obligaciones(
        self,
        anio: int,
        mes: int,
        seccion: int,
        subseccion: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Obtiene las obligaciones desde MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            seccion: Número de sección (1)
            subseccion: Subsección opcional (ej: "1.5.1")
            
        Returns:
            Documento con las obligaciones o None si no existe o MongoDB no está disponible
        """
        # Verificar si MongoDB está disponible
        if not self._is_mongodb_available() or self.collection is None:
            logger.warning("MongoDB no está configurado o no está disponible.")
            return None
        
        try:
            filtro = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion
            }
            
            if subseccion:
                filtro["subseccion"] = subseccion
            
            documento = await self.collection.find_one(filtro)
            
            if documento:
                logger.info(f"Obligaciones encontradas para {anio}-{mes}, sección {seccion}, subsección {subseccion}")
            else:
                logger.info(f"No se encontraron obligaciones para {anio}-{mes}, sección {seccion}, subsección {subseccion}")
            
            return documento
            
        except Exception as e:
            logger.error(f"Error al obtener obligaciones desde MongoDB: {e}", exc_info=True)
            raise
    
    async def eliminar_obligaciones(
        self,
        anio: int,
        mes: int,
        seccion: int,
        subseccion: Optional[str] = None
    ) -> bool:
        """
        Elimina las obligaciones de MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            seccion: Número de sección (1)
            subseccion: Subsección opcional
            
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
                "seccion": seccion
            }
            
            if subseccion:
                filtro["subseccion"] = subseccion
            
            resultado = await self.collection.delete_one(filtro)
            
            if resultado.deleted_count > 0:
                logger.info(f"Obligaciones eliminadas para {anio}-{mes}, sección {seccion}, subsección {subseccion}")
                return True
            else:
                logger.info(f"No se encontraron obligaciones para eliminar: {anio}-{mes}, sección {seccion}, subsección {subseccion}")
                return False
                
        except Exception as e:
            logger.error(f"Error al eliminar obligaciones desde MongoDB: {e}", exc_info=True)
            raise

