"""
Aplicación principal FastAPI para el sistema de generación de informes
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG", "False").lower() == "true" else logging.WARNING,
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

# Configurar CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5001,http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",  # Permitir todos los orígenes (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
try:
    from src.routes import obligaciones_routes
    app.include_router(obligaciones_routes.router, prefix="/api")
    logger.info("✓ Rutas de obligaciones incluidas")
except Exception as e:
    logger.warning(f"No se pudieron incluir rutas de obligaciones: {e}")

try:
    from src.routes import comunicados_routes
    app.include_router(comunicados_routes.router)
    logger.info("✓ Rutas de comunicados incluidas")
except Exception as e:
    logger.warning(f"No se pudieron incluir rutas de comunicados: {e}")

try:
    from src.routes import seccion1_routes
    app.include_router(seccion1_routes.router)
    logger.info("✓ Rutas de sección 1 incluidas")
except Exception as e:
    logger.warning(f"No se pudieron incluir rutas de sección 1: {e}")

# Intentar incluir otras rutas si existen
try:
    from src.routes import section1_routes
    app.include_router(section1_routes.router, prefix="/api")
    logger.info("✓ Rutas de sección 1 (legacy) incluidas")
except ImportError:
    logger.info("Rutas de sección 1 (legacy) no disponibles")

try:
    from src.routes import section2_routes
    app.include_router(section2_routes.router, prefix="/api")
    logger.info("✓ Rutas de sección 2 incluidas")
except ImportError:
    logger.info("Rutas de sección 2 no disponibles")

try:
    from src.routes import auth_routes
    app.include_router(auth_routes.router, prefix="/api")
    logger.info("✓ Rutas de autenticación incluidas")
except ImportError:
    logger.info("Rutas de autenticación no disponibles")

try:
    from src.routes import seccion5_routes
    app.include_router(seccion5_routes.router)
    logger.info("✓ Rutas de sección 5 (laboratorio) incluidas")
except Exception as e:
    logger.warning(f"No se pudieron incluir rutas de sección 5: {e}")


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "Sistema de Generación de Informes Mensuales ETB API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "obligaciones": "/api/obligaciones/procesar",
            "comunicados_emitidos": "/api/comunicados/emitidos",
            "comunicados_recibidos": "/api/comunicados/recibidos",
            "seccion1_generar": "/api/seccion1/generar",
            "seccion1_descargar": "/api/seccion1/descargar",
            "seccion5_procesar_excel": "/api/seccion5/procesar-excel",
            "seccion5_obtener_datos": "/api/seccion5/obtener-datos",
            "seccion5_generar": "/api/seccion5/generar",
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "service": "informes-api"
    }


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Iniciando servidor en http://{host}:{port}")
    logger.info(f"Documentación disponible en http://{host}:{port}/docs")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )

