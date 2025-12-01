"""
Servicio de conexión a MongoDB
"""
import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging
import config

import config

logger = logging.getLogger(__name__)

# Cliente global
_client: Optional[AsyncIOMotorClient] = None
_database = None


def get_database():
    """
    Obtiene la instancia de la base de datos MongoDB
    
    Returns:
        Base de datos MongoDB
    """
    global _database, _client
    
    if _database is None:
        # Usar las variables específicas del .env
        mongo_uri = os.getenv("MONGODB_URI") or getattr(config, 'MONGODB_URI', None)
        mongo_db = os.getenv("MONGODB_DB_NAME") or getattr(config, 'MONGODB_DB_NAME', None)
        
        if not mongo_uri:
            raise ValueError("MONGODB_URI no está configurado en .env o config.py")
        
        if not mongo_db:
            raise ValueError("MONGODB_DB_NAME no está configurado en .env o config.py")
        
        try:
            _client = AsyncIOMotorClient(mongo_uri)
            _database = _client[mongo_db]
            logger.info(f"Conectado a MongoDB: {mongo_db}")
        except Exception as e:
            logger.error(f"Error al conectar a MongoDB: {e}")
            raise
    
    return _database


async def connect_to_mongo():
    """Conecta a MongoDB con autenticación si está configurada"""
    mongodb_uri = config.MONGODB_URI
    db_name = config.MONGODB_DB_NAME
    
    try:
        # Construir URI con autenticación si hay usuario y contraseña
        if config.MONGODB_USER and config.MONGODB_PASSWORD:
            # Si ya viene una URI completa en MONGODB_URI, usarla
            if not mongodb_uri.startswith("mongodb://") or "@" in mongodb_uri:
                # Ya tiene autenticación o es una URI completa
                pass
            else:
                # Construir URI con autenticación
                mongodb_uri = f"mongodb://{config.MONGODB_USER}:{config.MONGODB_PASSWORD}@{config.MONGODB_HOST}:{config.MONGODB_PORT}/{db_name}?authSource={config.MONGODB_AUTH_SOURCE}"
        
        db.client = AsyncIOMotorClient(mongodb_uri)
        db.database = db.client[db_name]
        
        # Ocultar contraseña en logs
        uri_log = mongodb_uri
        if config.MONGODB_PASSWORD:
            uri_log = mongodb_uri.replace(config.MONGODB_PASSWORD, "***")
        
        logger.info(f"Conectado a MongoDB: {db_name}")
        logger.debug(f"MongoDB URI: {uri_log}")
        
        # Verificar conexión
        await db.client.admin.command('ping')
        logger.info("Conexión a MongoDB verificada exitosamente")
        
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Cierra la conexión a MongoDB"""
    global _client, _database
    
    if _client:
        _client.close()
        _client = None
        _database = None
        logger.info("Conexión a MongoDB cerrada")

