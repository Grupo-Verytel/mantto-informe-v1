"""
Aplicación principal FastAPI para el sistema de generación de informes
"""
import os
# """
# Aplicación principal FastAPI para el sistema de autenticación y roles
# """
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

# Cargar variables de entorno
load_dotenv()

# Configurar logging


import config



# # Configurar logging
logging.basicConfig(
    level=logging.INFO if config.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación"""
    # Startup
    logger.info("=" * 80)
    logger.info("Iniciando aplicación FastAPI...")
    logger.info("=" * 80)
    
    # Aquí puedes agregar inicializaciones si es necesario
    # Por ejemplo, conexión a MongoDB si la necesitas
    
    yield
    
    # Shutdown
    logger.info("=" * 80)
    logger.info("Cerrando aplicación...")
    logger.info("=" * 80)


# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Generación de Informes Mensuales ETB",
    description="API para generar informes mensuales de mantenimiento con extracción dinámica de datos",
    version="1.0.0",
    lifespan=lifespan
)

# # Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.routes import auth_routes,comunicados_routes,obligaciones_routes,seccion1_routes,seccion3_routes,seccion5_routes,section2_routes
routes = [
    auth_routes.router,
    obligaciones_routes.router,
    comunicados_routes.router,
    seccion1_routes.router,
    section2_routes.router,
    seccion3_routes.router,
    seccion5_routes.router
]
try: 
    for route in routes:
        app.include_router(route, prefix="/api")
        logger.info(f"✓ Rutas de {route.tags[0]} incluidas")
except Exception as e:
    logger.warning(f"No se pudieron incluir rutas de {route.tags[0]}: {e}")





