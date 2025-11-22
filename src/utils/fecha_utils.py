"""
Utilidades para manejo de fechas en español
"""
from datetime import datetime, date
from typing import Union
import config

def fecha_texto_largo(fecha: Union[datetime, date, str]) -> str:
    """
    Convierte fecha a texto largo en español
    Ejemplo: "23 de septiembre de 2025"
    """
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
    
    dia = fecha.day
    mes = config.MESES[fecha.month].lower()
    anio = fecha.year
    
    return f"{dia} de {mes} de {anio}"

def fecha_texto_corto(fecha: Union[datetime, date, str]) -> str:
    """
    Convierte fecha a texto corto
    Ejemplo: "23/09/2025"
    """
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
    
    return fecha.strftime("%d/%m/%Y")

def periodo_texto(anio: int, mes: int) -> str:
    """
    Retorna el periodo en formato texto
    Ejemplo: "Septiembre de 2025"
    """
    return f"{config.MESES[mes]} de {anio}"

def rango_mes(anio: int, mes: int) -> tuple:
    """
    Retorna el primer y último día del mes
    """
    from calendar import monthrange
    
    primer_dia = date(anio, mes, 1)
    ultimo_dia = date(anio, mes, monthrange(anio, mes)[1])
    
    return primer_dia, ultimo_dia


