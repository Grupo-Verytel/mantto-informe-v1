"""
Módulo de inteligencia artificial para generación de contenido
"""
from .generador_parrafos import generar_narrativa
from .analizador_datos import analizar_tendencias
from .extractor_observaciones import ExtractorObservaciones, get_extractor_observaciones

__all__ = [
    'generar_narrativa',
    'analizar_tendencias',
    'ExtractorObservaciones',
    'get_extractor_observaciones',
]
