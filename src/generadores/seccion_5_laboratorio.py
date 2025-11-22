"""
Generador Sección 5: Informe de Laboratorio
Tipo: 🟩 EXTRACCIÓN DATOS (laboratorio, inventario)

Subsecciones:
- 5.1 Actividades generales
  - 5.1.1 Reintegrados al inventario
  - 5.1.2 No operatividad
  - 5.1.3 RMA
- 5.2 Pendiente por parte
"""
from pathlib import Path
from typing import Dict, Any, List
import json
from .base import GeneradorSeccion
import config


class GeneradorSeccion5(GeneradorSeccion):
    """Genera la sección 5: Informe de Laboratorio"""
    
    @property
    def nombre_seccion(self) -> str:
        return "5. INFORME DE LABORATORIO"
    
    @property
    def template_file(self) -> str:
        return "seccion_5_laboratorio.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.actividades_generales: List[Dict] = []
        self.reintegrados: List[Dict] = []
        self.no_operativos: List[Dict] = []
        self.rma: List[Dict] = []
        self.pendiente_por_parte: List[Dict] = []
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 5 desde JSON"""
        # Cargar datos desde archivo JSON
        # Intentar primero con formato numérico, luego con nombre de mes
        archivo = config.FUENTES_DIR / f"laboratorio_{self.mes}_{self.anio}.json"
        if not archivo.exists():
            archivo = config.FUENTES_DIR / f"laboratorio_{config.MESES[self.mes].lower()}_{self.anio}.json"
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.actividades_generales = data.get("actividades_generales", [])
                    self.reintegrados = data.get("reintegrados", [])
                    self.no_operativos = data.get("no_operativos", [])
                    self.rma = data.get("rma", [])
                    self.pendiente_por_parte = data.get("pendiente_por_parte", [])
            except Exception as e:
                print(f"[WARNING] Error al cargar datos desde {archivo}: {e}")
                self._inicializar_datos_vacios()
        else:
            print(f"[WARNING] Archivo de datos no encontrado: {archivo}")
            self._inicializar_datos_vacios()
    
    def _inicializar_datos_vacios(self) -> None:
        """Inicializa estructuras vacías para consumo futuro"""
        self.actividades_generales = []
        self.reintegrados = []
        self.no_operativos = []
        self.rma = []
        self.pendiente_por_parte = []
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        return {
            # Texto narrativo fijo
            "texto_intro": "Durante el presente periodo se adelantaron las actividades de análisis, diagnóstico y verificación técnica de equipos, siguiendo los lineamientos del contrato SCJ-1809-2024.",
            
            # 5.1 Actividades generales
            "actividades_generales": self.actividades_generales,
            "total_actividades": len(self.actividades_generales),
            
            # 5.1.1 Reintegrados al inventario
            "reintegrados": self.reintegrados,
            "total_reintegrados": len(self.reintegrados),
            
            # 5.1.2 No operatividad
            "no_operativos": self.no_operativos,
            "total_no_operativos": len(self.no_operativos),
            
            # 5.1.3 RMA
            "rma": self.rma,
            "total_rma": len(self.rma),
            
            # 5.2 Pendiente por parte
            "pendiente_por_parte": self.pendiente_por_parte,
            "total_pendiente": len(self.pendiente_por_parte),
        }

