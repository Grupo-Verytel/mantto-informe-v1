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
    
    async def construir_documento_desde_mongodb(
        self,
        anio: int,
        mes: int,
        db
    ) -> Dict[str, Any]:
        """
        Construye el documento en formato esperado por el nuevo generador desde MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe
            db: Instancia de la base de datos MongoDB
            
        Returns:
            Diccionario con la estructura esperada por el generador:
            {
                "anio": 2025,
                "mes": 11,
                "index": [
                    {"id": "4", "level": 1, "title": "...", "content": {...}},
                    {"id": "4.1", "level": 2, "title": "...", "content": {...}},
                    ...
                ]
            }
        """
        try:
            logger.info(f"Construyendo documento desde MongoDB para {anio}-{mes}, sección 4...")
            
            repository = self._get_repository(db)
            inventario = await repository.get_inventario(anio, mes, "4")
            
            # Log para depuración
            if inventario:
                logger.info(f"Datos de inventario obtenidos: claves={list(inventario.keys())}")
                logger.info(f"Subsecciones directas: {list(inventario.get('subsecciones', {}).keys())}")
                # Verificar si hay estructura anidada con "data"
                if "data" in inventario:
                    data = inventario.get("data", {})
                    logger.info(f"Estructura con 'data' encontrada: subsecciones={list(data.get('subsecciones', {}).keys())}")
                    # Usar la estructura con "data" si existe
                    inventario = data
            
            if not inventario:
                logger.warning(f"No se encontró inventario para {anio}-{mes}")
                # Retornar estructura vacía
                return {
                    "anio": anio,
                    "mes": mes,
                    "index": [
                        {"id": "4", "level": 1, "title": "4. INFORME DE BIENES Y SERVICIOS", "content": {}},
                        {"id": "4.1", "level": 2, "title": "4.1 GESTIÓN DE INVENTARIO", "content": {}},
                        {"id": "4.2", "level": 2, "title": "4.2 ENTRADAS ALMACÉN SDSCJ", "content": {}},
                        {"id": "4.3", "level": 2, "title": "4.3 ENTREGA EQUIPOS NO OPERATIVOS ALMACÉN SDSCJ", "content": {}},
                        {"id": "4.4", "level": 2, "title": "4.4 GESTIONES DE INCLUSIÓN A LA BOLSA", "content": {}},
                    ]
                }
            
            # Obtener subsecciones
            subsecciones = inventario.get("subsecciones", {})
            logger.info(f"Subsecciones disponibles: {list(subsecciones.keys())}")
            subseccion_4 = subsecciones.get("4", {})
            logger.info(f"Subsección 4 disponible: {bool(subseccion_4)}, claves: {list(subseccion_4.keys()) if subseccion_4 else []}")
            
            # Construir estructura index
            index = []
            
            # Sección 4 (principal)
            index.append({
                "id": "4",
                "level": 1,
                "title": "4. INFORME DE BIENES Y SERVICIOS",
                "content": {
                    "image": ""  # Si hay imagen en MongoDB, agregarla aquí
                }
            })
            
            # 4.1 Gestión de Inventario
            sub_4_1 = subseccion_4.get("1", {})
            logger.info(f"Sección 4.1 - Datos obtenidos: texto={bool(sub_4_1.get('texto'))}, ruta={bool(sub_4_1.get('ruta'))}, tabla={len(sub_4_1.get('tabla', []))} registros")
            
            # Combinar texto y ruta como se hace en inventario_routes
            texto_41 = sub_4_1.get("texto", "")
            ruta_41 = sub_4_1.get("ruta", "")
            texto_combinado = ""
            if texto_41 and ruta_41:
                texto_combinado = f"{texto_41}\n{ruta_41}"
            elif texto_41:
                texto_combinado = texto_41
            elif ruta_41:
                texto_combinado = ruta_41
            
            # Obtener tabla - puede estar en diferentes campos
            tabla_41 = sub_4_1.get("tabla", [])
            if not tabla_41:
                # Intentar otros nombres posibles
                tabla_41 = sub_4_1.get("tablaInventario", [])
            if not tabla_41:
                tabla_41 = sub_4_1.get("tablaGestion", [])
            
            logger.info(f"Sección 4.1 - Texto combinado: {len(texto_combinado)} caracteres, Tabla: {len(tabla_41)} registros")
            
            content_41 = {
                "texto": texto_combinado,
                "tabla": tabla_41
            }
            index.append({
                "id": "4.1",
                "level": 2,
                "title": "4.1 GESTIÓN DE INVENTARIO",
                "content": content_41
            })
            
            # 4.2 Entradas Almacén SDSCJ
            sub_4_2 = subseccion_4.get("2", {})
            if sub_4_2 and sub_4_2.get("hayEntradas", False):
                tabla_entradas = sub_4_2.get("tablaEntradas", [])
                # Transformar tablaEntradas al formato esperado
                elementos = []
                for item in tabla_entradas:
                    elementos.append({
                        "descripcion": item.get("itemBolsa", item.get("descripcion", "")),
                        "cantidad": item.get("cantidad", 0),
                        "unidad": item.get("unidad", "UN"),
                        "valor_unitario": item.get("valor_unitario", item.get("valorUnitario", 0)),
                        "valor_total": item.get("valor_total", item.get("valorTotal", 0))
                    })
                
                content_42 = {
                    "texto": sub_4_2.get("texto", ""),
                    "comunicado": {
                        "numero": sub_4_2.get("comunicado", ""),
                        "fecha": sub_4_2.get("fechaIngreso", "")
                    },
                    "elementos": elementos,
                    "anexos": sub_4_2.get("anexos", [])
                }
                logger.info(f"Sección 4.2 - hayEntradas=True, {len(elementos)} elementos, texto: {len(sub_4_2.get('texto', ''))} caracteres")
            else:
                content_42 = {
                    "texto": sub_4_2.get("texto", "") if sub_4_2 else "",
                    "comunicado": {},
                    "elementos": [],
                    "anexos": []
                }
                logger.info(f"Sección 4.2 - hayEntradas={sub_4_2.get('hayEntradas', False) if sub_4_2 else False}")
            
            index.append({
                "id": "4.2",
                "level": 2,
                "title": "4.2 ENTRADAS ALMACÉN SDSCJ",
                "content": content_42
            })
            
            # 4.3 Entrega Equipos No Operativos
            sub_4_3 = subseccion_4.get("3", {})
            
            # Obtener tablaEquiposNoOperativos (puede ser dict o list)
            tabla_equipos_no_operativos = sub_4_3.get("tablaEquiposNoOperativos", {})
            if isinstance(tabla_equipos_no_operativos, list) and len(tabla_equipos_no_operativos) > 0:
                tabla_equipos_no_operativos = tabla_equipos_no_operativos[0]
            elif not isinstance(tabla_equipos_no_operativos, dict):
                tabla_equipos_no_operativos = {}
            
            # Obtener tablaSiniestros (puede ser dict o list)
            tabla_siniestros = sub_4_3.get("tablaSiniestros", {})
            if isinstance(tabla_siniestros, list) and len(tabla_siniestros) > 0:
                tabla_siniestros = tabla_siniestros[0]
            elif not isinstance(tabla_siniestros, dict):
                tabla_siniestros = {}
            
            # Construir content_43 con la nueva estructura que espera _seccion_4_3
            content_43 = {
                "haySalidas": sub_4_3.get("haySalidas", False),
                "texto": sub_4_3.get("texto", ""),
                "tablaEquiposNoOperativos": tabla_equipos_no_operativos,
                "textoBajasNoOperativas": sub_4_3.get("textoBajasNoOperativas", ""),
                "tablaDetalleEquipos": sub_4_3.get("tablaDetalleEquipos", []),
                "haySiniestros": sub_4_3.get("haySiniestros", False),
                "textoSiniestros": sub_4_3.get("textoSiniestros", ""),
                "tablaSiniestros": tabla_siniestros,
                "textoReintegro": sub_4_3.get("textoReintegro", ""),
                "tablaDetalleSiniestros": sub_4_3.get("tablaDetalleSiniestros", [])
            }
            
            logger.info(f"Sección 4.3 - haySalidas={content_43.get('haySalidas')}, haySiniestros={content_43.get('haySiniestros')}")
            logger.info(f"Sección 4.3 - tablaDetalleEquipos: {len(content_43.get('tablaDetalleEquipos', []))} items")
            logger.info(f"Sección 4.3 - tablaDetalleSiniestros: {len(content_43.get('tablaDetalleSiniestros', []))} items")
            logger.info(f"Sección 4.3 - tablaEquiposNoOperativos: {bool(tabla_equipos_no_operativos)}")
            logger.info(f"Sección 4.3 - tablaSiniestros: {bool(tabla_siniestros)}")
            
            index.append({
                "id": "4.3",
                "level": 2,
                "title": "4.3 ENTREGA EQUIPOS NO OPERATIVOS ALMACÉN SDSCJ",
                "content": content_43
            })
            
            # 4.4 Gestiones de Inclusión a la Bolsa
            sub_4_4 = subseccion_4.get("4", {})
            texto_44 = sub_4_4.get("texto", "") if sub_4_4 else ""
            tabla_gestion_inclusion = sub_4_4.get("tablaGestionInclusion") if sub_4_4 else None
            
            logger.info(f"Sección 4.4 - texto: {len(texto_44) if texto_44 else 0} caracteres")
            logger.info(f"Sección 4.4 - tablaGestionInclusion: tipo={type(tabla_gestion_inclusion)}, valor={bool(tabla_gestion_inclusion)}")
            
            content_44 = {
                "texto": texto_44,
                "tablaGestionInclusion": tabla_gestion_inclusion
            }
            
            index.append({
                "id": "4.4",
                "level": 2,
                "title": "4.4 GESTIONES DE INCLUSIÓN A LA BOLSA",
                "content": content_44
            })
            
            documento = {
                "anio": anio,
                "mes": mes,
                "index": index
            }
            
            logger.info(f"Documento construido exitosamente para {anio}-{mes}")
            return documento
        
        except Exception as e:
            logger.error(f"Error al construir documento desde MongoDB: {e}", exc_info=True)
            raise
    
    async def generar_seccion4(
        self,
        anio: int,
        mes: int,
        output_path: Optional[Path] = None,
        db = None
    ) -> Path:
        """
        Genera el documento de la sección 4 desde MongoDB usando el nuevo generador
        
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
        
        # Construir documento desde MongoDB
        document = await self.construir_documento_desde_mongodb(anio, mes, db)
        
        # Determinar ruta de salida
        if output_path is None:
            output_path = config.OUTPUT_DIR / f"seccion_4_{anio}_{mes:02d}.docx"
        
        # Asegurar que el directorio existe
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Crear generador y generar documento
        generador = GeneradorSeccion4()
        await generador.generar(document, output_path)
        
        logger.info(f"Sección 4 generada exitosamente en: {output_path}")
        return output_path

