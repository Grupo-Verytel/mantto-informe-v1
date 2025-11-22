"""
Extractor de datos de archivos Excel y CSV
Para comunicados, inventario, facturas
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import config


def leer_excel(ruta: Path, hoja: str = None) -> pd.DataFrame:
    """
    Lee un archivo Excel
    
    Args:
        ruta: Ruta al archivo Excel
        hoja: Nombre de la hoja (opcional)
    
    Returns:
        DataFrame con los datos
    """
    if hoja:
        return pd.read_excel(ruta, sheet_name=hoja)
    return pd.read_excel(ruta)


def leer_csv(ruta: Path, separador: str = ',') -> pd.DataFrame:
    """
    Lee un archivo CSV
    
    Args:
        ruta: Ruta al archivo CSV
        separador: Separador del CSV (default: ',')
    
    Returns:
        DataFrame con los datos
    """
    return pd.read_csv(ruta, sep=separador, encoding='utf-8')


def dataframe_a_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convierte un DataFrame a lista de diccionarios
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        Lista de diccionarios
    """
    return df.to_dict('records')


class ExcelExtractor:
    """Extrae datos de archivos Excel para la Sección 4"""
    
    def __init__(self, ruta_base: Path = None):
        self.ruta_base = ruta_base or config.FUENTES_DIR
    
    def get_entradas_almacen(self, anio: int, mes: int) -> dict:
        """
        Extrae datos de entradas al almacén desde Excel
        
        Archivo esperado: entradas_almacen_{mes}_{anio}.xlsx
        Columnas: descripcion, cantidad, unidad, valor_unitario, valor_total
        
        Returns:
            {
                "comunicado": {...},
                "items": [...],
                "anexos": [...]
            }
        """
        # Intentar primero con formato numérico, luego con nombre de mes
        archivo = self.ruta_base / f"entradas_almacen_{mes}_{anio}.xlsx"
        if not archivo.exists():
            archivo = self.ruta_base / f"entradas_almacen_{config.MESES[mes].lower()}_{anio}.xlsx"
        
        if not archivo.exists():
            return {"comunicado": {}, "items": [], "anexos": []}
        
        try:
            # Leer datos
            df = pd.read_excel(archivo, sheet_name="Items")
            
            items = []
            for _, row in df.iterrows():
                items.append({
                    "descripcion": str(row.get("descripcion", "")),
                    "cantidad": int(row.get("cantidad", 0)),
                    "unidad": str(row.get("unidad", "UN")),
                    "valor_unitario": float(row.get("valor_unitario", 0)),
                    "valor_total": float(row.get("valor_total", 0))
                })
            
            # Leer metadatos del comunicado (otra hoja)
            comunicado = {}
            try:
                df_meta = pd.read_excel(archivo, sheet_name="Comunicado")
                if not df_meta.empty:
                    comunicado = {
                        "numero": str(df_meta.iloc[0].get("numero", "")),
                        "titulo": str(df_meta.iloc[0].get("titulo", "")),
                        "fecha": str(df_meta.iloc[0].get("fecha", ""))
                    }
            except:
                pass
            
            return {
                "comunicado": comunicado,
                "items": items,
                "anexos": []  # Configurar según estructura
            }
        except Exception as e:
            print(f"[WARNING] Error al leer {archivo}: {e}")
            return {"comunicado": {}, "items": [], "anexos": []}
    
    def get_equipos_no_operativos(self, anio: int, mes: int) -> dict:
        """
        Extrae datos de equipos no operativos desde Excel
        
        Archivo esperado: equipos_no_operativos_{mes}_{anio}.xlsx
        """
        # Intentar primero con formato numérico, luego con nombre de mes
        archivo = self.ruta_base / f"equipos_no_operativos_{mes}_{anio}.xlsx"
        if not archivo.exists():
            archivo = self.ruta_base / f"equipos_no_operativos_{config.MESES[mes].lower()}_{anio}.xlsx"
        
        if not archivo.exists():
            return {"comunicado": {}, "equipos": [], "anexos": []}
        
        try:
            df = pd.read_excel(archivo, sheet_name="Equipos")
            
            equipos = []
            for _, row in df.iterrows():
                equipos.append({
                    "descripcion": str(row.get("descripcion", "")),
                    "serial": str(row.get("serial", "N/A")),
                    "cantidad": int(row.get("cantidad", 1)),
                    "motivo": str(row.get("motivo", "")),
                    "valor": float(row.get("valor", 0))
                })
            
            # Leer metadatos del comunicado
            comunicado = {}
            try:
                df_meta = pd.read_excel(archivo, sheet_name="Comunicado")
                if not df_meta.empty:
                    comunicado = {
                        "numero": str(df_meta.iloc[0].get("numero", "")),
                        "titulo": str(df_meta.iloc[0].get("titulo", "")),
                        "fecha": str(df_meta.iloc[0].get("fecha", ""))
                    }
            except:
                pass
            
            return {
                "comunicado": comunicado,
                "equipos": equipos,
                "anexos": []
            }
        except Exception as e:
            print(f"[WARNING] Error al leer {archivo}: {e}")
            return {"comunicado": {}, "equipos": [], "anexos": []}
    
    def get_inclusiones_bolsa(self, anio: int, mes: int) -> dict:
        """
        Extrae datos de solicitudes de inclusión a la bolsa
        
        Archivo esperado: inclusiones_bolsa_{mes}_{anio}.xlsx
        """
        # Intentar primero con formato numérico, luego con nombre de mes
        archivo = self.ruta_base / f"inclusiones_bolsa_{mes}_{anio}.xlsx"
        if not archivo.exists():
            archivo = self.ruta_base / f"inclusiones_bolsa_{config.MESES[mes].lower()}_{anio}.xlsx"
        
        if not archivo.exists():
            return {"comunicado": {}, "items": [], "estado": "Sin solicitudes", "anexos": []}
        
        try:
            df = pd.read_excel(archivo, sheet_name="Items")
            
            items = []
            for _, row in df.iterrows():
                items.append({
                    "descripcion": str(row.get("descripcion", "")),
                    "cantidad": int(row.get("cantidad", 0)),
                    "unidad": str(row.get("unidad", "UN")),
                    "valor_unitario": float(row.get("valor_unitario", 0)),
                    "valor_total": float(row.get("valor_total", 0)),
                    "justificacion": str(row.get("justificacion", ""))
                })
            
            # Leer metadatos del comunicado
            comunicado = {}
            estado = "En trámite"
            try:
                df_meta = pd.read_excel(archivo, sheet_name="Comunicado")
                if not df_meta.empty:
                    comunicado = {
                        "numero": str(df_meta.iloc[0].get("numero", "")),
                        "titulo": str(df_meta.iloc[0].get("titulo", "")),
                        "fecha": str(df_meta.iloc[0].get("fecha", ""))
                    }
                    estado = str(df_meta.iloc[0].get("estado", "En trámite"))
            except:
                pass
            
            return {
                "comunicado": comunicado,
                "items": items,
                "estado": estado,
                "anexos": []
            }
        except Exception as e:
            print(f"[WARNING] Error al leer {archivo}: {e}")
            return {"comunicado": {}, "items": [], "estado": "Sin solicitudes", "anexos": []}


# Instancia global del extractor
_extractor_instance = None

def get_excel_extractor(ruta_base: Path = None) -> ExcelExtractor:
    """Obtiene la instancia singleton del extractor Excel"""
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = ExcelExtractor(ruta_base)
    return _extractor_instance



