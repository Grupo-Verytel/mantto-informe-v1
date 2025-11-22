"""
Configuración específica para cálculos de ANS
Valores contractuales del contrato SCJ-1809-2024
"""

# Umbral mínimo de disponibilidad (%)
UMBRAL_ANS = 98.9

# Configuración de penalidades
PENALIDAD_CONFIG = {
    # Por cada 0.1% de déficit se aplica este % del valor mensual
    "porcentaje_por_decima": 0.5,
    
    # Límites de penalidad
    "penalidad_maxima_porcentaje": 10.0,  # Máximo 10% del valor mensual
    
    # Valor mensual del contrato (actualizar según contrato)
    "valor_mensual_contrato": 150000000,
}

# Fórmula de disponibilidad
# Disponibilidad (%) = (Horas Operativas / Horas Totales) × 100

# Estados de cámaras para el cálculo
ESTADOS_OPERATIVOS = ["Operativa", "En línea", "OK"]
ESTADOS_NO_OPERATIVOS = ["No operativa", "Fuera de línea", "Falla"]
ESTADOS_MANTENIMIENTO = ["En mantenimiento", "Preventivo", "Correctivo"]

# Localidades de Bogotá para el reporte
LOCALIDADES = [
    "Usaquén", "Chapinero", "Santa Fe", "San Cristóbal", "Usme",
    "Tunjuelito", "Bosa", "Kennedy", "Fontibón", "Engativá",
    "Suba", "Barrios Unidos", "Teusaquillo", "Los Mártires",
    "Antonio Nariño", "Puente Aranda", "La Candelaria", 
    "Rafael Uribe Uribe", "Ciudad Bolívar", "Sumapaz"
]

def calcular_penalidad(disponibilidad: float, umbral: float, valor_mensual: float) -> dict:
    """
    Calcula la penalidad por incumplimiento de ANS
    
    Fórmula típica:
    - Por cada 0.1% debajo del umbral = 0.5% del valor mensual
    - Máximo 10% del valor mensual
    
    Args:
        disponibilidad: Porcentaje de disponibilidad obtenido
        umbral: Umbral mínimo requerido (98.9%)
        valor_mensual: Valor mensual del contrato
    
    Returns:
        Diccionario con información de la penalidad
    """
    if disponibilidad >= umbral:
        return {
            "aplica": False,
            "deficit": 0,
            "porcentaje_penalidad": 0,
            "valor_penalidad": 0,
            "descripcion": "No aplica penalidad - ANS cumplido"
        }
    
    deficit = umbral - disponibilidad
    decimas_deficit = deficit / 0.1
    porcentaje_penalidad = min(decimas_deficit * PENALIDAD_CONFIG["porcentaje_por_decima"], 
                              PENALIDAD_CONFIG["penalidad_maxima_porcentaje"])
    valor_penalidad = valor_mensual * (porcentaje_penalidad / 100)
    
    return {
        "aplica": True,
        "deficit": deficit,
        "porcentaje_penalidad": porcentaje_penalidad,
        "valor_penalidad": valor_penalidad,
        "descripcion": f"Penalidad por déficit de {deficit:.2f}% en disponibilidad"
    }

