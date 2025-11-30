"""
Utilidades para trabajar con informes aprobados
"""
from pathlib import Path
from typing import List, Optional
import config
import re

try:
    import PyPDF2
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False

try:
    from docx import Document as DocxDocument
    DOCX_DISPONIBLE = True
except ImportError:
    DOCX_DISPONIBLE = False


def obtener_ultimos_informes_aprobados(cantidad: int = 3) -> List[Path]:
    """
    Obtiene los últimos N informes aprobados ordenados por fecha de modificación
    
    Args:
        cantidad: Número de informes a obtener (default: 3)
        
    Returns:
        Lista de Paths a los archivos de informes aprobados
    """
    if not config.INFORMES_APROBADOS_DIR.exists():
        print(f"[WARNING] Directorio de informes aprobados no existe: {config.INFORMES_APROBADOS_DIR}")
        return []
    
    # Obtener todos los archivos PDF y DOCX
    archivos = []
    for ext in ['*.pdf', '*.docx']:
        archivos.extend(config.INFORMES_APROBADOS_DIR.glob(ext))
    
    if not archivos:
        print(f"[WARNING] No se encontraron informes aprobados en {config.INFORMES_APROBADOS_DIR}")
        return []
    
    # Ordenar por fecha de modificación (más reciente primero)
    archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    # Retornar los últimos N
    return archivos[:cantidad]


def extraer_seccion_obligaciones_generales(ruta_informe: Path) -> Optional[str]:
    """
    Extrae la sección 1.5.1 OBLIGACIONES GENERALES de un informe aprobado
    
    Args:
        ruta_informe: Path al archivo del informe (PDF o DOCX)
        
    Returns:
        Texto de la sección 1.5.1 o None si no se encuentra
    """
    if not ruta_informe.exists():
        return None
    
    extension = ruta_informe.suffix.lower()
    texto_completo = ""
    
    try:
        if extension == '.pdf' and PDF_DISPONIBLE:
            with open(ruta_informe, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    texto_completo += page.extract_text() + "\n"
        elif extension in ['.docx', '.doc'] and DOCX_DISPONIBLE:
            doc = DocxDocument(ruta_informe)
            for para in doc.paragraphs:
                texto_completo += para.text + "\n"
        else:
            print(f"[WARNING] Formato no soportado para extracción: {extension}")
            return None
        
        # Buscar la sección 1.5.1 OBLIGACIONES GENERALES
        # Patrones posibles:
        # - "1.5.1" seguido de "OBLIGACIONES GENERALES"
        # - "1.5.1." seguido de "OBLIGACIONES GENERALES"
        # - Variaciones con espacios
        
        patrones = [
            r'1\.5\.1[\.\s]+OBLIGACIONES\s+GENERALES',
            r'1\.5\.1[\.\s]+Obligaciones\s+Generales',
            r'1\.5\.1[\.\s]+Obligaciones\s+generales',
        ]
        
        inicio_seccion = None
        for patron in patrones:
            match = re.search(patron, texto_completo, re.IGNORECASE)
            if match:
                inicio_seccion = match.start()
                break
        
        if inicio_seccion is None:
            print(f"[WARNING] No se encontró la sección 1.5.1 en {ruta_informe.name}")
            return None
        
        # Extraer desde el inicio de la sección hasta la siguiente sección (1.5.2 o 1.6)
        texto_desde_seccion = texto_completo[inicio_seccion:]
        
        # Buscar el final de la sección (siguiente sección principal)
        fin_patrones = [
            r'1\.5\.2[\.\s]',
            r'1\.6[\.\s]',
            r'2\.\s',
        ]
        
        fin_seccion = len(texto_desde_seccion)
        for patron in fin_patrones:
            match = re.search(patron, texto_desde_seccion, re.IGNORECASE)
            if match:
                fin_seccion = match.start()
                break
        
        seccion_texto = texto_desde_seccion[:fin_seccion].strip()
        
        if len(seccion_texto) < 100:
            print(f"[WARNING] Sección 1.5.1 extraída es muy corta ({len(seccion_texto)} caracteres) en {ruta_informe.name}")
            return None
        
        print(f"[INFO] Sección 1.5.1 extraída de {ruta_informe.name}: {len(seccion_texto)} caracteres")
        return seccion_texto
        
    except Exception as e:
        print(f"[WARNING] Error al extraer sección de {ruta_informe.name}: {e}")
        return None


def obtener_contexto_informes_aprobados(cantidad: int = 3) -> List[str]:
    """
    Obtiene el texto de la sección 1.5.1 de los últimos N informes aprobados
    
    Args:
        cantidad: Número de informes a procesar (default: 3)
        
    Returns:
        Lista de textos de la sección 1.5.1 de cada informe
    """
    informes = obtener_ultimos_informes_aprobados(cantidad)
    contextos = []
    
    for informe in informes:
        texto_seccion = extraer_seccion_obligaciones_generales(informe)
        if texto_seccion:
            contextos.append(texto_seccion)
    
    print(f"[INFO] Se obtuvieron {len(contextos)} contextos de informes aprobados")
    return contextos

