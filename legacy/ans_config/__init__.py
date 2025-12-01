"""
Módulo de configuración del generador de informes ETB
"""
from .ans_config import (
    UMBRAL_ANS,
    PENALIDAD_CONFIG,
    ESTADOS_OPERATIVOS,
    ESTADOS_NO_OPERATIVOS,
    ESTADOS_MANTENIMIENTO,
    LOCALIDADES,
    calcular_penalidad
)

__all__ = [
    'UMBRAL_ANS',
    'PENALIDAD_CONFIG',
    'ESTADOS_OPERATIVOS',
    'ESTADOS_NO_OPERATIVOS',
    'ESTADOS_MANTENIMIENTO',
    'LOCALIDADES',
    'calcular_penalidad'
]

