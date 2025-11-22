"""
Utilidades para manipulación de documentos Word
"""
from pathlib import Path
from typing import List
from docx import Document

def combinar_documentos(archivos: List[Path], archivo_salida: Path) -> None:
    """
    Combina múltiples documentos Word en uno solo
    
    Args:
        archivos: Lista de rutas a los documentos a combinar
        archivo_salida: Ruta del archivo de salida
    """
    if not archivos:
        raise ValueError("No hay documentos para combinar")
    
    documento_final = Document(archivos[0])
    
    # Agregar cada documento subsecuente
    for archivo in archivos[1:]:
        doc_temp = Document(archivo)
        
        # Agregar salto de página antes de cada nuevo documento (excepto el primero)
        documento_final.add_page_break()
        
        # Copiar elementos de cada sección
        for elemento in doc_temp.element.body:
            documento_final.element.body.append(elemento)
    
    documento_final.save(str(archivo_salida))

def agregar_pagina_nueva(doc: Document) -> None:
    """
    Agrega un salto de página al documento
    
    Args:
        doc: Documento Word
    """
    doc.add_page_break()

def aplicar_estilo_titulo(parrafo, nivel: int = 1) -> None:
    """
    Aplica estilo de título a un párrafo
    
    Args:
        parrafo: Párrafo del documento
        nivel: Nivel del título (1-9)
    """
    estilo = f"Heading {min(nivel, 9)}"
    parrafo.style = estilo


