# """
# Aplicación principal FastAPI para el sistema de autenticación y roles
# """
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
    
from src.routes import auth_routes
from src.services.database import connect_to_mongo, close_mongo_connection

# # Cargar variables de entorno
load_dotenv()

# # Configurar logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG", "False").lower() == "true" else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación"""
    # Startup
    logger.info("Iniciando aplicación...")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("Cerrando aplicación...")
    await close_mongo_connection()


# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Autenticación y Roles - Mantto Informe",
    description="API para autenticación y control de acceso basado en roles",
    version="1.0.0",
    lifespan=lifespan
)

# # Configurar CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5001,http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Incluir rutas
app.include_router(auth_routes.router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "Sistema de Autenticación y Roles - Mantto Informe API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "service": "authentication-api"
    }


if __name__ == "__main__":
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "3000"))

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
