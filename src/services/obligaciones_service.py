"""
Service para procesar obligaciones y generar observaciones dinámicamente
"""
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import config
from src.ia.extractor_observaciones import get_extractor_observaciones
from src.repositories.obligaciones_repository import ObligacionesRepository
import logging

logger = logging.getLogger(__name__)


class ObligacionesService:
    """Service para procesar obligaciones de la sección 1.5"""
    
    def __init__(self):
        self.extractor_observaciones = None
        self.repository = ObligacionesRepository()
        self._inicializar_extractor()
    
    def _inicializar_extractor(self):
        """Inicializa el extractor de observaciones"""
        try:
            sharepoint_site_url = getattr(config, 'SHAREPOINT_SITE_URL', None) or config.SHAREPOINT_SITE_URL
            sharepoint_client_id = getattr(config, 'SHAREPOINT_CLIENT_ID', None) or config.SHAREPOINT_CLIENT_ID
            sharepoint_client_secret = getattr(config, 'SHAREPOINT_CLIENT_SECRET', None) or config.SHAREPOINT_CLIENT_SECRET
            sharepoint_base_path = getattr(config, 'SHAREPOINT_BASE_PATH', None) or config.SHAREPOINT_BASE_PATH
            
            self.extractor_observaciones = get_extractor_observaciones(
                sharepoint_site_url=sharepoint_site_url,
                sharepoint_client_id=sharepoint_client_id,
                sharepoint_client_secret=sharepoint_client_secret,
                sharepoint_base_path=sharepoint_base_path
            )
        except Exception as e:
            logger.warning(f"No se pudo inicializar extractor de observaciones: {e}")
            self.extractor_observaciones = None
    
    def cargar_obligaciones_desde_json(self, anio: int, mes: int) -> Dict[str, List[Dict]]:
        """
        Carga obligaciones desde archivo JSON
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            
        Returns:
            Diccionario con obligaciones_generales, obligaciones_especificas, etc.
        """
        # Intentar primero con formato numérico, luego con nombre de mes
        archivo = config.FUENTES_DIR / f"obligaciones_{mes}_{anio}.json"
        if not archivo.exists():
            archivo = config.FUENTES_DIR / f"obligaciones_{config.MESES[mes].lower()}_{anio}.json"
        
        if not archivo.exists():
            logger.warning(f"Archivo de obligaciones no encontrado: {archivo}")
            return {
                "obligaciones_generales": [],
                "obligaciones_especificas": [],
                "obligaciones_ambientales": [],
                "obligaciones_anexos": []
            }
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Obligaciones cargadas desde {archivo}")
            return data
        except Exception as e:
            logger.error(f"Error al cargar obligaciones desde {archivo}: {e}")
            return {
                "obligaciones_generales": [],
                "obligaciones_especificas": [],
                "obligaciones_ambientales": [],
                "obligaciones_anexos": []
            }
    
    def procesar_obligaciones(
        self,
        obligaciones: List[Dict],
        tipo: str = "generales",
        regenerar_todas: bool = False
    ) -> List[Dict]:
        """
        Procesa una lista de obligaciones y genera observaciones dinámicamente
        
        Args:
            obligaciones: Lista de obligaciones a procesar
            tipo: Tipo de obligación ("generales", "especificas", "ambientales", "anexos")
            regenerar_todas: Si True, regenera todas las observaciones incluso si ya existen
            
        Returns:
            Lista de obligaciones con observaciones actualizadas
        """
        if not self.extractor_observaciones:
            logger.warning("Extractor de observaciones no disponible. Retornando obligaciones sin procesar.")
            return obligaciones
        
        obligaciones_procesadas = []
        total = len(obligaciones)
        
        for idx, obligacion in enumerate(obligaciones, 1):
            item = obligacion.get("item", idx)
            logger.info(f"[{idx}/{total}] Procesando obligación {tipo} - Item {item}")
            
            # Si regenerar_todas es True, forzar regeneración
            if regenerar_todas:
                obligacion["regenerar_observacion"] = True
            
            try:
                obligacion_procesada = self.extractor_observaciones.procesar_obligacion(obligacion)
                obligaciones_procesadas.append(obligacion_procesada)
                
                # Log del resultado
                if obligacion_procesada.get("observaciones"):
                    logger.info(f"  ✓ Observación generada ({len(obligacion_procesada['observaciones'])} caracteres)")
                else:
                    logger.warning(f"  ⚠ No se generó observación para item {item}")
            
            except Exception as e:
                logger.error(f"  ✗ Error al procesar obligación {item}: {e}")
                # Agregar obligación sin procesar en caso de error
                obligaciones_procesadas.append(obligacion)
        
        return obligaciones_procesadas
    
    def procesar_todas_las_obligaciones(
        self,
        anio: int,
        mes: int,
        regenerar_todas: bool = False
    ) -> Dict[str, List[Dict]]:
        """
        Procesa todas las obligaciones (generales, específicas, ambientales, anexos)
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            regenerar_todas: Si True, regenera todas las observaciones
            
        Returns:
            Diccionario con todas las obligaciones procesadas
        """
        # Cargar obligaciones desde JSON
        obligaciones = self.cargar_obligaciones_desde_json(anio, mes)
        
        resultado = {}
        
        # Procesar obligaciones generales
        if obligaciones.get("obligaciones_generales"):
            logger.info("=" * 60)
            logger.info("PROCESANDO OBLIGACIONES GENERALES")
            logger.info("=" * 60)
            resultado["obligaciones_generales"] = self.procesar_obligaciones(
                obligaciones["obligaciones_generales"],
                tipo="generales",
                regenerar_todas=regenerar_todas
            )
        
        # Procesar obligaciones específicas
        if obligaciones.get("obligaciones_especificas"):
            logger.info("=" * 60)
            logger.info("PROCESANDO OBLIGACIONES ESPECÍFICAS")
            logger.info("=" * 60)
            resultado["obligaciones_especificas"] = self.procesar_obligaciones(
                obligaciones["obligaciones_especificas"],
                tipo="especificas",
                regenerar_todas=regenerar_todas
            )
        
        # Procesar obligaciones ambientales
        if obligaciones.get("obligaciones_ambientales"):
            logger.info("=" * 60)
            logger.info("PROCESANDO OBLIGACIONES AMBIENTALES")
            logger.info("=" * 60)
            resultado["obligaciones_ambientales"] = self.procesar_obligaciones(
                obligaciones["obligaciones_ambientales"],
                tipo="ambientales",
                regenerar_todas=regenerar_todas
            )
        
        # Procesar obligaciones de anexos
        if obligaciones.get("obligaciones_anexos"):
            logger.info("=" * 60)
            logger.info("PROCESANDO OBLIGACIONES DE ANEXOS")
            logger.info("=" * 60)
            resultado["obligaciones_anexos"] = self.procesar_obligaciones(
                obligaciones["obligaciones_anexos"],
                tipo="anexos",
                regenerar_todas=regenerar_todas
            )
        
        return resultado
    
    def obtener_tipo_obligacion_por_subseccion(self, subseccion: str) -> Optional[str]:
        """
        Mapea una subsección a un tipo de obligación
        
        Args:
            subseccion: Subsección (ej: "1.5.1", "1.5.2", etc.)
            
        Returns:
            Tipo de obligación o None si no existe
        """
        mapeo = {
            "1.5.1": "obligaciones_generales",
            "1.5.2": "obligaciones_especificas",
            "1.5.3": "obligaciones_ambientales",
            "1.5.4": "obligaciones_anexos"
        }
        return mapeo.get(subseccion)
    
    def procesar_subseccion(
        self,
        anio: int,
        mes: int,
        subseccion: str,
        regenerar_todas: bool = False
    ) -> Dict[str, Any]:
        """
        Procesa una subsección específica de obligaciones
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            subseccion: Subsección a procesar (ej: "1.5.1", "1.5.2", etc.)
            regenerar_todas: Si True, regenera todas las observaciones
            
        Returns:
            Diccionario con las obligaciones de la subsección procesadas
        """
        tipo_obligacion = self.obtener_tipo_obligacion_por_subseccion(subseccion)
        
        if not tipo_obligacion:
            raise ValueError(f"Subsección {subseccion} no válida. Subsecciones válidas: 1.5.1, 1.5.2, 1.5.3, 1.5.4")
        
        # Cargar obligaciones desde JSON
        obligaciones = self.cargar_obligaciones_desde_json(anio, mes)
        
        # Obtener obligaciones de la subsección
        obligaciones_subseccion = obligaciones.get(tipo_obligacion, [])
        
        # Si es 1.5.4 (obligaciones_anexos), verificar existencia de archivos
        if subseccion == "1.5.4":
            return self._procesar_obligaciones_anexos(obligaciones_subseccion)
        
        # Procesar obligaciones normales
        tipo_corto = tipo_obligacion.replace("obligaciones_", "")
        obligaciones_procesadas = self.procesar_obligaciones(
            obligaciones_subseccion,
            tipo=tipo_corto,
            regenerar_todas=regenerar_todas
        )
        
        return {
            tipo_obligacion: obligaciones_procesadas
        }
    
    def _procesar_obligaciones_anexos(self, obligaciones: List[Dict]) -> Dict[str, Any]:
        """
        Procesa obligaciones de anexos verificando existencia de archivos en SharePoint
        
        Solo verifica si el archivo existe y retorna formato simplificado.
        No genera observaciones con LLM.
        
        Args:
            obligaciones: Lista de obligaciones de anexos
            
        Returns:
            Diccionario con formato simplificado: solo archivo_existe y anexo
        """
        from src.extractores.sharepoint_extractor import get_sharepoint_extractor
        import config
        
        sharepoint_extractor = get_sharepoint_extractor()
        
        resultado = []
        
        for obligacion in obligaciones:
            ruta_anexo = obligacion.get("anexo", "")
            
            # Verificar existencia del archivo
            archivo_existe = False
            mensaje_anexo = ""
            
            if ruta_anexo and ruta_anexo != "-" and ruta_anexo.lower() != "no aplica":
                try:
                    logger.info(f"Verificando existencia del archivo: {ruta_anexo}")
                    # Intentar verificar existencia en SharePoint
                    archivo_existe = sharepoint_extractor.verificar_archivo_existe(ruta_anexo)
                    
                    if archivo_existe:
                        mensaje_anexo = ruta_anexo  # Si existe, poner la ruta completa
                        logger.info(f"✓ Archivo encontrado: {ruta_anexo}")
                    else:
                        mensaje_anexo = "Archivo no existe"  # Si no existe, mensaje fijo
                        logger.warning(f"✗ Archivo no encontrado: {ruta_anexo}")
                        
                except Exception as e:
                    logger.error(f"Error al verificar archivo {ruta_anexo}: {e}")
                    archivo_existe = False
                    mensaje_anexo = "Archivo no existe"  # En caso de error, considerar como no existe
            else:
                mensaje_anexo = "Archivo no existe"
                logger.info(f"⚠ No se especificó ruta de anexo")
            
            # Formato simplificado: solo archivo_existe y anexo
            resultado.append({
                "archivo_existe": archivo_existe,
                "anexo": mensaje_anexo
            })
        
        logger.info(f"Procesadas {len(resultado)} obligaciones de anexos. Archivos encontrados: {sum(1 for r in resultado if r.get('archivo_existe', False))}")
        
        return {
            "obligaciones_anexos": resultado
        }
    
    def guardar_obligaciones_procesadas(
        self,
        obligaciones: Dict[str, List[Dict]],
        anio: int,
        mes: int,
        crear_backup: bool = True
    ) -> Path:
        """
        Guarda las obligaciones procesadas en un archivo JSON
        
        Args:
            obligaciones: Diccionario con obligaciones procesadas
            anio: Año del informe
            mes: Mes del informe (1-12)
            crear_backup: Si True, crea un backup del archivo original
            
        Returns:
            Ruta del archivo guardado
        """
        # Determinar nombre del archivo
        archivo = config.FUENTES_DIR / f"obligaciones_{mes}_{anio}.json"
        if not archivo.exists():
            archivo = config.FUENTES_DIR / f"obligaciones_{config.MESES[mes].lower()}_{anio}.json"
        
        # Crear backup si existe el archivo original
        if crear_backup and archivo.exists():
            backup_path = archivo.with_suffix(f".backup_{mes}_{anio}.json")
            import shutil
            shutil.copy2(archivo, backup_path)
            logger.info(f"Backup creado: {backup_path}")
        
        # Guardar obligaciones procesadas
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(obligaciones, f, ensure_ascii=False, indent=2)
            logger.info(f"Obligaciones procesadas guardadas en: {archivo}")
            return archivo
        except Exception as e:
            logger.error(f"Error al guardar obligaciones procesadas: {e}")
            raise
    
    async def guardar_obligaciones_en_mongodb(
        self,
        obligaciones: Dict[str, List[Dict]],
        anio: int,
        mes: int,
        seccion: int,
        subseccion: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Guarda las obligaciones procesadas en MongoDB
        
        Args:
            obligaciones: Diccionario con obligaciones procesadas
            anio: Año del informe
            mes: Mes del informe (1-12)
            seccion: Número de sección (1)
            subseccion: Subsección opcional (ej: "1.5.1")
            user_id: ID del usuario que realiza la operación
            
        Returns:
            Documento guardado en MongoDB
        """
        try:
            documento_guardado = await self.repository.guardar_obligaciones(
                anio=anio,
                mes=mes,
                seccion=seccion,
                subseccion=subseccion,
                obligaciones_data=obligaciones,
                user_id=user_id
            )
            if documento_guardado:
                logger.info(f"Obligaciones guardadas en MongoDB para {anio}-{mes}, sección {seccion}, subsección {subseccion}")
            else:
                logger.info(f"MongoDB no está disponible. Obligaciones procesadas correctamente pero no guardadas en MongoDB.")
            return documento_guardado
        except Exception as e:
            logger.warning(f"Error al guardar obligaciones en MongoDB: {e}")
            # No lanzar excepción, solo registrar warning
            return None

