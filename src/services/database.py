"""
Servicio de conexión a MongoDB
"""
import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging
import config

logger = logging.getLogger(__name__)

# Cliente global
_client: Optional[AsyncIOMotorClient] = None
_database = None


def get_database():
    """
    Obtiene la instancia de la base de datos MongoDB
    Usa las variables de config que ya están cargadas desde .env
    
    Returns:
        Base de datos MongoDB
    """
    global _database, _client
    
    if _database is None:
        # Obtener variables de config (ya cargadas desde .env)
        mongo_uri = config.MONGODB_URI
        mongo_db_name = config.MONGODB_DB_NAME
        mongo_user = config.MONGODB_USER
        mongo_password = config.MONGODB_PASSWORD
        mongo_host = config.MONGODB_HOST
        mongo_port = config.MONGODB_PORT
        mongo_auth_source = config.MONGODB_AUTH_SOURCE
        
        # Validar que tenemos al menos host y nombre de base de datos
        if not mongo_host:
            raise ValueError("MONGODB_HOST no está configurado en .env o config.py")
        
        if not mongo_db_name:
            raise ValueError("MONGODB_DB_NAME no está configurado en .env o config.py")
        
        # Si MONGODB_URI está definida y es válida, usarla directamente
        if mongo_uri and mongo_uri.strip() and (mongo_uri.startswith("mongodb://") or mongo_uri.startswith("mongodb+srv://")):
            # Usar la URI completa del .env
            final_uri = mongo_uri
        else:
        
            # Construir URI desde las variables individuales
            if mongo_user and mongo_password:
                # Construir URI con autenticación
                final_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource={mongo_db_name}"
            else:
                # URI sin autenticación (solo para desarrollo local)
                final_uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db_name}"
      
        try:
            _client = AsyncIOMotorClient(final_uri)
            _database = _client[mongo_db_name]
            
            # Ocultar contraseña en logs
            uri_log = final_uri
            if "@" in final_uri:
                # Ocultar contraseña en el log
                parts = final_uri.split("@")
                if len(parts) == 2:
                    auth_part = parts[0]
                    if ":" in auth_part:
                        user_part = auth_part.split(":")[0]
                        uri_log = f"mongodb://{user_part}:***@{parts[1]}"
            
            logger.info(f"Conectado a MongoDB: {mongo_db_name}")
            logger.info(f"MongoDB Host: {mongo_host}:{mongo_port}")
            logger.debug(f"MongoDB URI: {uri_log}")
        except Exception as e:
            logger.error(f"Error al conectar a MongoDB: {e}")
            logger.error(f"Intentando conectar a: {mongo_host}:{mongo_port}")
            logger.error(f"Base de datos: {mongo_db_name}")
            raise
    
    return _database


async def connect_to_mongo():
    """Conecta a MongoDB con autenticación si está configurada"""
    global _client, _database
    
    # Usar la misma lógica que get_database()
    if _database is None:
        get_database()
    
    try:
        # Verificar conexión
        await _client.admin.command('ping')
        logger.info("Conexión a MongoDB verificada exitosamente")
    except Exception as e:
        logger.error(f"Error al verificar conexión a MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Cierra la conexión a MongoDB"""
    global _client, _database
    
    if _client:
        _client.close()
        _client = None
        _database = None
        logger.info("Conexión a MongoDB cerrada")

