"""
Configuración global del generador de informes ETB
"""
from pathlib import Path
from datetime import datetime

# Rutas base
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
FIJOS_DIR = DATA_DIR / "fijos"
FUENTES_DIR = DATA_DIR / "fuentes"

# Crear directorios si no existen
for dir_path in [TEMPLATES_DIR, DATA_DIR, OUTPUT_DIR, FIJOS_DIR, FUENTES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Información del contrato (FIJO)
CONTRATO = {
    "numero": "SCJ-1809-2024",
    "entidad": "EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ S.A. E.S.P.",
    "entidad_corto": "ETB",
    "objeto": "MANTENIMIENTO PREVENTIVO, MANTENIMIENTO CORRECTIVO Y SOPORTE AL SISTEMA DE VIDEOVIGILANCIA DE BOGOTÁ D.C., CON DISPONIBILIDAD DE BOLSA DE REPUESTOS",
    "contratista": "NOMBRE DEL CONTRATISTA",  # Ajustar
    "nit_contratista": "XXX.XXX.XXX-X",
    "supervisor": "NOMBRE DEL SUPERVISOR",
    "interventor": "NOMBRE DEL INTERVENTOR",
    "fecha_inicio": "2024-11-01",
    "fecha_fin": "2025-10-31",
    "valor_contrato": 0,  # Ajustar
    "umbral_ans": 98.9,  # Porcentaje mínimo de disponibilidad
}

# Meses en español
MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

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
    "C4-CAD"
]

# Localidades de Bogotá
LOCALIDADES = [
    "Usaquén", "Chapinero", "Santa Fe", "San Cristóbal", "Usme",
    "Tunjuelito", "Bosa", "Kennedy", "Fontibón", "Engativá",
    "Suba", "Barrios Unidos", "Teusaquillo", "Los Mártires",
    "Antonio Nariño", "Puente Aranda", "La Candelaria", "Rafael Uribe Uribe",
    "Ciudad Bolívar", "Sumapaz"
]

def get_nombre_informe(anio: int, mes: int, version: int = 1) -> str:
    """Genera el nombre del archivo de informe"""
    nombre_mes = MESES[mes].upper()
    return f"INFORME_MENSUAL_{nombre_mes}_{anio}_V{version}.docx"

def get_periodo_texto(anio: int, mes: int) -> str:
    """Retorna el periodo en formato texto: 'Septiembre de 2025'"""
    return f"{MESES[mes]} de {anio}"


