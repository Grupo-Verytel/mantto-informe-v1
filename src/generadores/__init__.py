"""
Generadores de secciones del informe
"""
from .seccion_1_info_general import GeneradorSeccion1
from .seccion_2_mesa_servicio import GeneradorSeccion2
from .seccion_3_ans import GeneradorSeccion3
from .seccion_4_bienes import GeneradorSeccion4
from .seccion_5_laboratorio import GeneradorSeccion5

__all__ = ['GeneradorSeccion1', 'GeneradorSeccion2', 'GeneradorSeccion3', 'GeneradorSeccion4', 'GeneradorSeccion5']

