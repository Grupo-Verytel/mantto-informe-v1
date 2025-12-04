"""
Service para generar la sección 4 del informe desde MongoDB
"""
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from src.generadores.seccion_4_bienes import GeneradorSeccion4
from src.repositories.inventario_repository import InventarioRepository
import config

logger = logging.getLogger(__name__)


class Seccion4Service:
    """Service para generar la sección 4 del informe"""
    
    def __init__(self):
        self.inventario_repo = None
    
    def _get_repository(self, db):
        """Obtiene o crea el repositorio con la base de datos"""
        if self.inventario_repo is None or self.inventario_repo.db is None:
            self.inventario_repo = InventarioRepository(db)
        return self.inventario_repo
    
    async def cargar_datos_desde_mongodb(
        self,
        anio: int,
        mes: int,
        generador: GeneradorSeccion4,
        db
    ) -> None:
        """
        Carga datos desde MongoDB y los asigna al generador
        
        Args:
            anio: Año del informe
            mes: Mes del informe
            generador: Instancia del generador de sección 4
            db: Instancia de la base de datos MongoDB
        """
        try:
            logger.info(f"Cargando datos de inventario desde MongoDB para {anio}-{mes}, sección 4...")
            
            repository = self._get_repository(db)
            inventario = await repository.get_inventario(anio, mes, "4")
            
            if not inventario:
                logger.warning(f"No se encontró inventario para {anio}-{mes}")
                generador.datos = {}
                return
            
            # Obtener subsecciones
            subsecciones = inventario.get("subsecciones", {})
            subseccion_4 = subsecciones.get("4", {})
            
            # Transformar datos de MongoDB al formato que espera el generador
            datos_transformados = {}
            
            # 4.1 Gestión de Inventario
            sub_4_1 = subseccion_4.get("1", {})
            if sub_4_1:
                datos_transformados["gestion_inventario"] = {
                    "texto": sub_4_1.get("texto", ""),
                    "ruta": sub_4_1.get("ruta", "")
                }
            
            # 4.2 Entradas Almacén SDSCJ
            sub_4_2 = subseccion_4.get("2", {})
            if sub_4_2 and sub_4_2.get("hayEntradas", False):
                tabla_entradas = sub_4_2.get("tablaEntradas", [])
                # Transformar tablaEntradas al formato esperado
                items = []
                for item in tabla_entradas:
                    items.append({
                        "descripcion": item.get("itemBolsa", ""),
                        "cantidad": item.get("cantidad", 0),
                        "unidad": "UN",  # Por defecto
                        "valor_unitario": 0,  # No está en el JSON
                        "valor_total": 0  # No está en el JSON
                    })
                
                datos_transformados["entradas_almacen"] = {
                    "comunicado": {
                        "numero": sub_4_2.get("comunicado", ""),
                        "titulo": "",
                        "fecha": sub_4_2.get("fechaIngreso", "")
                    },
                    "texto": sub_4_2.get("texto", ""),
                    "items": items,
                    "anexos": []
                }
            else:
                datos_transformados["entradas_almacen"] = {
                    "comunicado": {},
                    "texto": "",
                    "items": [],
                    "anexos": []
                }
            
            # 4.3 Entrega Equipos No Operativos
            sub_4_3 = subseccion_4.get("3", {})
            if sub_4_3:
                equipos_data = {
                    "comunicado": {
                        "numero": sub_4_3.get("tablaEquiposNoOperativos", {}).get("comunicado", ""),
                        "titulo": "",
                        "fecha": sub_4_3.get("tablaEquiposNoOperativos", {}).get("fecha", "")
                    },
                    "texto": sub_4_3.get("texto", ""),
                    "equipos": [],
                    "anexos": []
                }
                
                # Equipos no operativos
                if sub_4_3.get("haySalidas", False):
                    tabla_detalle = sub_4_3.get("tablaDetalleEquipos", [])
                    equipos = []
                    for eq in tabla_detalle:
                        equipos.append({
                            "descripcion": eq.get("equipo", ""),
                            "serial": "",
                            "cantidad": eq.get("cantidad", 0),
                            "motivo": sub_4_3.get("textoBajasNoOperativas", ""),
                            "valor": 0
                        })
                    equipos_data["equipos"] = equipos
                    equipos_data["texto"] = sub_4_3.get("textoBajasNoOperativas", "")
                
                # Siniestros
                if sub_4_3.get("haySiniestros", False):
                    tabla_siniestros = sub_4_3.get("tablaSiniestros", {})
                    tabla_detalle_siniestros = sub_4_3.get("tablaDetalleSiniestros", [])
                    
                    # Agregar equipos de siniestros
                    for sin in tabla_detalle_siniestros:
                        equipos_data["equipos"].append({
                            "descripcion": sin.get("equipo", ""),
                            "serial": "",
                            "cantidad": sin.get("cantidad", 0),
                            "motivo": sub_4_3.get("textoSiniestros", ""),
                            "valor": 0
                        })
                    
                    equipos_data["texto"] += f"\n\n{sub_4_3.get('textoSiniestros', '')}"
                    equipos_data["texto"] += f"\n{sub_4_3.get('textoReintegro', '')}"
                
                datos_transformados["equipos_no_operativos"] = equipos_data
            else:
                datos_transformados["equipos_no_operativos"] = {
                    "comunicado": {},
                    "texto": "",
                    "equipos": [],
                    "anexos": []
                }
            
            # 4.4 Gestiones de Inclusión a la Bolsa
            sub_4_4 = subseccion_4.get("4", {})
            if sub_4_4:
                tabla_gestion = sub_4_4.get("tablaGestionInclusion", {})
                datos_transformados["inclusiones_bolsa"] = {
                    "comunicado": {
                        "numero": tabla_gestion.get("consecutivoETB", ""),
                        "titulo": "",
                        "fecha": tabla_gestion.get("fecha", "")
                    },
                    "texto": sub_4_4.get("texto", ""),
                    "estado": "En proceso",
                    "items": [{
                        "descripcion": tabla_gestion.get("descripcion", ""),
                        "cantidad": 1,
                        "unidad": "UN",
                        "valor_unitario": 0,
                        "valor_total": 0,
                        "justificacion": ""
                    }],
                    "anexos": []
                }
            else:
                datos_transformados["inclusiones_bolsa"] = {
                    "comunicado": {},
                    "texto": "",
                    "estado": "Sin solicitudes",
                    "items": [],
                    "anexos": []
                }
            
            # Asignar datos transformados al generador
            generador.datos = datos_transformados
            generador.datos["mes"] = config.MESES[mes]
            generador.datos["anio"] = anio
            
            logger.info(f"Datos de inventario cargados exitosamente para {anio}-{mes}")
        
        except Exception as e:
            logger.error(f"Error al cargar datos desde MongoDB: {e}", exc_info=True)
            generador.datos = {}
            raise
    
    async def generar_seccion4(
        self,
        anio: int,
        mes: int,
        output_path: Optional[Path] = None,
        db = None
    ) -> Path:
        """
        Genera el documento de la sección 4 desde MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            output_path: Ruta donde guardar el documento. Si None, usa directorio de salida por defecto
            db: Instancia de la base de datos MongoDB
            
        Returns:
            Path al archivo generado
        """
        if db is None:
            raise ValueError("db es requerido para generar la sección 4")
        
        # Crear generador
        generador = GeneradorSeccion4(
            anio=anio,
            mes=mes
        )
        
        # Cargar datos desde MongoDB
        await self.cargar_datos_desde_mongodb(anio, mes, generador, db)
        
        # Determinar ruta de salida
        if output_path is None:
            output_path = config.OUTPUT_DIR / f"seccion_4_{anio}_{mes:02d}.docx"
        
        # Asegurar que el directorio existe
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generar y guardar el documento
        generador.guardar(output_path)
        
        logger.info(f"Sección 4 generada exitosamente en: {output_path}")
        return output_path

