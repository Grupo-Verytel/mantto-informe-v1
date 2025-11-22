"""
Clase base para todos los generadores de secciones
"""
from abc import ABC, abstractmethod
from pathlib import Path
from docxtpl import DocxTemplate
from typing import Dict, Any
import config

class GeneradorSeccion(ABC):
    """Clase base abstracta para generadores de secciones"""
    
    def __init__(self, anio: int, mes: int):
        self.anio = anio
        self.mes = mes
        self.periodo = config.get_periodo_texto(anio, mes)
        self.contrato = config.CONTRATO
        self.contexto: Dict[str, Any] = {}
    
    @property
    @abstractmethod
    def nombre_seccion(self) -> str:
        """Nombre de la sección (ej: '1. INFORMACIÓN GENERAL')"""
        pass
    
    @property
    @abstractmethod
    def template_file(self) -> str:
        """Nombre del archivo template"""
        pass
    
    @property
    def template_path(self) -> Path:
        """Ruta completa al template"""
        return config.TEMPLATES_DIR / self.template_file
    
    def cargar_contexto_base(self) -> Dict[str, Any]:
        """Carga el contexto base común a todas las secciones"""
        return {
            "contrato_numero": self.contrato["numero"],
            "entidad": self.contrato["entidad"],
            "entidad_corto": self.contrato["entidad_corto"],
            "periodo": self.periodo,
            "mes": config.MESES[self.mes],
            "anio": self.anio,
            "mes_numero": self.mes,
        }
    
    @abstractmethod
    def cargar_datos(self) -> None:
        """Carga los datos específicos de la sección"""
        pass
    
    @abstractmethod
    def procesar(self) -> Dict[str, Any]:
        """Procesa los datos y retorna el contexto para el template"""
        pass
    
    def generar(self) -> DocxTemplate:
        """Genera la sección completa"""
        # Cargar contexto base
        self.contexto = self.cargar_contexto_base()
        
        # Cargar datos específicos
        self.cargar_datos()
        
        # Procesar y agregar al contexto
        datos_seccion = self.procesar()
        self.contexto.update(datos_seccion)
        
        # Renderizar template
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template no encontrado: {self.template_path}")
        
        doc = DocxTemplate(self.template_path)
        doc.render(self.contexto)
        
        return doc
    
    def guardar(self, output_path: Path) -> None:
        """Genera y guarda la sección"""
        doc = self.generar()
        doc.save(str(output_path))
        print(f"[OK] {self.nombre_seccion} guardada en: {output_path}")


