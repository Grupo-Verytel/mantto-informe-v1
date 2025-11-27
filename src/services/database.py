"""
Servicio de conexión a MongoDB
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Database:
    """Clase para manejar la conexión a MongoDB"""
    
    client: Optional[AsyncIOMotorClient] = None
    database = None


db = Database()


async def connect_to_mongo():
    """Conecta a MongoDB"""
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "mantto_informe")
    
    try:
        db.client = AsyncIOMotorClient(mongodb_uri)
        db.database = db.client[db_name]
        logger.info(f"Conectado a MongoDB: {db_name}")
        
        # Verificar conexión
        await db.client.admin.command('ping')
        logger.info("Conexión a MongoDB verificada exitosamente")
        
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB: {str(e)}")
        raise


async def close_mongo_connection():
    """Cierra la conexión a MongoDB"""
    if db.client:
        db.client.close()
        logger.info("Conexión a MongoDB cerrada")


def get_database():
    """Obtiene la instancia de la base de datos"""
    return db.database



