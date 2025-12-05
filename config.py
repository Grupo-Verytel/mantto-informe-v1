"""
Configuración global unificada del sistema
Centraliza todas las configuraciones del sistema, incluyendo variables de entorno
"""

import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


# ============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "3000"))

# ============================================================================
# CONFIGURACIÓN CORS
# ============================================================================
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:5001,http://localhost:3000,http://localhost:5173"
).split(",")

# ============================================================================
# CONFIGURACIÓN DE BASE DE DATOS (MongoDB)
# ============================================================================
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", "27017")
MONGODB_USER = os.getenv("MONGODB_USER", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "mantto_informe")
MONGODB_AUTH_SOURCE = os.getenv(
    "MONGODB_AUTH_SOURCE", "admin"
)





# ============================================================================
# CONFIGURACIÓN JWT
# ============================================================================
JWT_SECRET = os.getenv("JWT_SECRET", "default-secret-key-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_IN_HOURS = int(os.getenv("JWT_EXPIRES_IN_HOURS", "24"))

# ============================================================================
# CONFIGURACIÓN API EXTERNA DE AUTENTICACIÓN
# ============================================================================
EXTERNAL_AUTH_API_URL = os.getenv("EXTERNAL_AUTH_API_URL", "http://localhost:4000")
EXTERNAL_AUTH_API_TIMEOUT = int(os.getenv("EXTERNAL_AUTH_API_TIMEOUT", "10"))

# ============================================================================
# CONFIGURACIÓN GLPI
# ============================================================================
GLPI_API_URL = os.getenv("GLPI_API_URL", "https://glpi.etb.com.co/apirest.php")
GLPI_API_TOKEN = os.getenv("GLPI_API_TOKEN", "TU_TOKEN_AQUI")

# ============================================================================
# INFORMACIÓN DEL CONTRATO (FIJO)
# Datos oficiales del contrato SCJ-1809-2024
# ============================================================================
CONTRATO = {
    "numero": "SCJ-1809-2024",
    "numero_proceso": "SECOP II SCJ-SIF-CD-480-2024",
    "entidad": "EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ S.A. E.S.P.",
    "entidad_corto": "ETB",
    "nit_entidad": "899.999.115-8",
    "razon_social": "EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ S.A E.S.P. - ETB S.A E.S.P.",
    "direccion": "NIZA, CALLE 126 60 32 | PISO 1",
    "ciudad": "BOGOTÁ – COLOMBIA",
    "telefono": "6012423499",
    "objeto": "PRESTACIÓN DE LOS SERVICIOS DE ADMINISTRACIÓN, SOPORTE, MANTENIMIENTO PREVENTIVO, CORRECTIVO Y/O DE ACTUALIZACIÓN AL SISTEMA DE VIDEO VIGILANCIA DE BOGOTÁ D.C., CON DISPONIBILIDAD DE BOLSA DE REPUESTOS",
    "objeto_corto": "MANTENIMIENTO PREVENTIVO, MANTENIMIENTO CORRECTIVO Y SOPORTE AL SISTEMA DE VIDEOVIGILANCIA DE BOGOTÁ D.C., CON DISPONIBILIDAD DE BOLSA DE REPUESTOS",
    "contratista": os.getenv("CONTRATO_CONTRATISTA", "NOMBRE DEL CONTRATISTA"),
    "nit_contratista": os.getenv("CONTRATO_NIT_CONTRATISTA", "XXX.XXX.XXX-X"),
    "supervisor": os.getenv("CONTRATO_SUPERVISOR", "NOMBRE DEL SUPERVISOR"),
    "interventor": os.getenv("CONTRATO_INTERVENTOR", "NOMBRE DEL INTERVENTOR"),
    "fecha_inicio": "2024-11-19",  # 19 de noviembre de 2024 (fecha acta de inicio)
    "fecha_fin": "2025-11-18",  # 18 de noviembre de 2025
    "fecha_suscripcion": "2024-10-31",  # 31 de octubre de 2024
    "plazo_ejecucion": "DOCE (12) MESES",
    "valor_inicial": 16450000000,  # $16.450.000.000
    "adicion_1": 2000000000,  # $2.000.000.000
    "valor_total": 18450000000,  # $18.450.000.000
    "valor_contrato": 18450000000,  # Total del contrato
    "vigencia_poliza_inicial_inicio": "2024-10-31",
    "vigencia_poliza_inicial_fin": "2028-10-31",
    "vigencia_poliza_acta_inicio": "2024-11-19",
    "vigencia_poliza_acta_fin": "2028-11-19",
    "umbral_ans": 98.9,  # Porcentaje mínimo de disponibilidad
}

# ============================================================================
# DATOS ESTÁTICOS
# ============================================================================

# Meses en español
MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

# Lista de meses en español (para compatibilidad)
MESES_LISTA = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

# Subsistemas del contrato
SUBSISTEMAS = [
    "Domos Ciudadanos",
    "TransMilenio",
    "Instituciones Educativas",
    "Centro de Traslado por Protección (CTP)",
    "Centro de Atención Inmediata (CAI)",
    "Estaciones de Policía",
    "Estadio Nemesio Camacho El Campín",
    "Centros de Monitoreo",
    "Data Center",
    "C4-CAD",
]

# Localidades de Bogotá
LOCALIDADES = [
    "Usaquén",
    "Chapinero",
    "Santa Fe",
    "San Cristóbal",
    "Usme",
    "Tunjuelito",
    "Bosa",
    "Kennedy",
    "Fontibón",
    "Engativá",
    "Suba",
    "Barrios Unidos",
    "Teusaquillo",
    "Los Mártires",
    "Antonio Nariño",
    "Puente Aranda",
    "La Candelaria",
    "Rafael Uribe Uribe",
    "Ciudad Bolívar",
    "Sumapaz",
]

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================


def get_nombre_informe(anio: int, mes: int, version: int = 1) -> str:
    """Genera el nombre del archivo de informe"""
    nombre_mes = MESES[mes].upper()
    return f"INFORME_MENSUAL_{nombre_mes}_{anio}_V{version}.docx"


def get_periodo_texto(anio: int, mes: int) -> str:
    """Retorna el periodo en formato texto: 'Septiembre de 2025'"""
    return f"{MESES[mes]} de {anio}"

# Configuración GLPI
GLPI_API_URL = "https://glpi.etb.com.co/apirest.php"
GLPI_API_TOKEN = os.getenv("GLPI_API_TOKEN", "TU_TOKEN_AQUI")

# Configuración OpenAI (LLM)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Configuración SharePoint (solo App Registration - username/password deprecado)
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL", "")
SHAREPOINT_CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID", "")
SHAREPOINT_CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
# Tenant ID de Azure AD (GUID) - Si no se proporciona, se extrae del dominio de SHAREPOINT_SITE_URL
SHAREPOINT_TENANT_ID = os.getenv("SHAREPOINT_TENANT_ID", "")
# Ruta base adicional en SharePoint (ej: "Documentos compartidos" o "Shared Documents" o carpeta base)
SHAREPOINT_BASE_PATH = os.getenv("SHAREPOINT_BASE_PATH", "")
# Configuración GLPI MySQL
GLPI_MYSQL_HOST = os.getenv("GLPI_MYSQL_HOST", "")
GLPI_MYSQL_PORT = int(os.getenv("GLPI_MYSQL_PORT", "3306"))
GLPI_MYSQL_USER = os.getenv("GLPI_MYSQL_USER", "")
GLPI_MYSQL_PASSWORD = os.getenv("GLPI_MYSQL_PASSWORD", "")
GLPI_MYSQL_DATABASE = os.getenv("GLPI_MYSQL_DATABASE", "glpi")

# Lista de meses en español (para compatibilidad)
MESES_LISTA = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Configuración MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "")

# ============================================================================
# CONFIGURACIÓN DE DIRECTORIOS
# ============================================================================
# Directorio base del proyecto
BASE_DIR = Path(__file__).parent

# Directorio de salida para documentos generados
OUTPUT_DIR = BASE_DIR / "output"

# Directorio de templates Word
TEMPLATES_DIR = BASE_DIR / "src" / "resources" / "templates"

# Directorio de datos fuente (JSON, CSV, Excel)
FUENTES_DIR = BASE_DIR / "src" / "resources" / "fuentes"

# Directorio de datos fijos
DATA_DIR = BASE_DIR / "src" / "resources"

