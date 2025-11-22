"""
Convertir números a texto en español (para valores monetarios)
"""
from num2words import num2words

def numero_a_letras(numero: float, moneda: bool = True) -> str:
    """
    Convierte un número a su representación en letras
    
    Args:
        numero: Número a convertir
        moneda: Si True, agrega "PESOS M/CTE"
    
    Returns:
        Texto en mayúsculas
    
    Ejemplo:
        245678910 -> "DOSCIENTOS CUARENTA Y CINCO MILLONES SEISCIENTOS 
                      SETENTA Y OCHO MIL NOVECIENTOS DIEZ PESOS M/CTE"
    """
    # Separar parte entera y decimal
    parte_entera = int(numero)
    parte_decimal = int(round((numero - parte_entera) * 100))
    
    # Convertir a letras
    texto = num2words(parte_entera, lang='es')
    texto = texto.upper()
    
    if moneda:
        if parte_decimal > 0:
            texto += f" PESOS CON {parte_decimal}/100 M/CTE"
        else:
            texto += " PESOS M/CTE"
    
    return texto

def formato_moneda(numero: float) -> str:
    """
    Formatea número como moneda colombiana
    
    Ejemplo:
        245678910 -> "$245.678.910"
    """
    return f"${numero:,.0f}".replace(",", ".")


