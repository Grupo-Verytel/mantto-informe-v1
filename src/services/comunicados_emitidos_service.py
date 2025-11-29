"""
Service para procesar comunicados emitidos de la sección 1.6.1
"""
from typing import Dict, List, Any, Optional
import config
from src.extractores.sharepoint_extractor import get_sharepoint_extractor
from src.ia.extractor_observaciones import get_extractor_observaciones
from src.repositories.comunicados_repository import ComunicadosRepository
import logging
import re

logger = logging.getLogger(__name__)


class ComunicadosEmitidosService:
    """Service para procesar comunicados emitidos de la sección 1.6.1"""
    
    def __init__(self):
        self.sharepoint_extractor = None
        self.extractor_observaciones = None
        self.repository = ComunicadosRepository()
        self._inicializar_extractores()
    
    def _inicializar_extractores(self):
        """Inicializa los extractores necesarios"""
        try:
            sharepoint_site_url = getattr(config, 'SHAREPOINT_SITE_URL', None) or config.SHAREPOINT_SITE_URL
            sharepoint_client_id = getattr(config, 'SHAREPOINT_CLIENT_ID', None) or config.SHAREPOINT_CLIENT_ID
            sharepoint_client_secret = getattr(config, 'SHAREPOINT_CLIENT_SECRET', None) or config.SHAREPOINT_CLIENT_SECRET
            sharepoint_base_path = getattr(config, 'SHAREPOINT_BASE_PATH', None) or config.SHAREPOINT_BASE_PATH
            
            self.sharepoint_extractor = get_sharepoint_extractor(
                site_url=sharepoint_site_url,
                client_id=sharepoint_client_id,
                client_secret=sharepoint_client_secret,
                base_path=sharepoint_base_path
            )
            
            self.extractor_observaciones = get_extractor_observaciones(
                sharepoint_site_url=sharepoint_site_url,
                sharepoint_client_id=sharepoint_client_id,
                sharepoint_client_secret=sharepoint_client_secret,
                sharepoint_base_path=sharepoint_base_path
            )
        except Exception as e:
            logger.warning(f"No se pudieron inicializar extractores: {e}")
            self.sharepoint_extractor = None
            self.extractor_observaciones = None
    
    def obtener_ruta_carpeta_comunicados(self, anio: int, mes: int, tipo: str = "emitidos") -> str:
        """
        Construye la ruta de la carpeta de comunicados en SharePoint
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            tipo: Tipo de comunicados ("emitidos" o "recibidos")
            
        Returns:
            Ruta de la carpeta en formato SharePoint
        """
        mes_abrev = config.MESES[mes].upper()[:3]
        
        if tipo == "recibidos":
            ruta = f"11. 01{mes_abrev} - 30{mes_abrev} / 01 OBLIGACIONES GENERALES / OBLIGACIÓN 7 y 10 / COMUNICADOS RECIBIDOS"
        else:  # emitidos por defecto
            ruta = f"11. 01{mes_abrev} - 30{mes_abrev} / 01 OBLIGACIONES GENERALES / OBLIGACIÓN 7 y 10 / COMUNICADOS EMITIDOS"
        
        logger.info(f"[DEBUG] Ruta construida para comunicados {tipo}: '{ruta}'")
        logger.info(f"[DEBUG] Mes: {mes}, Mes abreviado: {mes_abrev}, Año: {anio}")
        print(f"[DEBUG] Ruta construida para comunicados {tipo}: '{ruta}'")
        return ruta
    
    def extraer_radicado_desde_nombre(self, nombre_archivo: str) -> Optional[str]:
        """
        Extrae el radicado del nombre del archivo
        
        Args:
            nombre_archivo: Nombre del archivo (ej: "GSC-7444-2025.pdf")
            
        Returns:
            Radicado extraído (ej: "GSC-7444-2025") o None
        """
        # Intentar extraer patrón común de radicado: LETRAS-NUMEROS-AÑO
        # Ejemplos: "GSC-7444-2025", "GSC-7444-2025.pdf", "COM-123-2024.docx"
        patrones = [
            r'([A-Z]{2,}-\d+-\d{4})',  # GSC-7444-2025
            r'([A-Z]{2,}\d+-\d{4})',   # GSC7444-2025
            r'([A-Z]{2,}-\d+)',        # GSC-7444 (sin año)
        ]
        
        for patron in patrones:
            match = re.search(patron, nombre_archivo.upper())
            if match:
                return match.group(1)
        
        # Si no se encuentra patrón, retornar el nombre sin extensión
        nombre_sin_ext = nombre_archivo.rsplit('.', 1)[0] if '.' in nombre_archivo else nombre_archivo
        return nombre_sin_ext if nombre_sin_ext else None
    
    def procesar_comunicados(
        self,
        anio: int,
        mes: int,
        tipo: str = "emitidos",
        regenerar_todas: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Procesa los comunicados (emitidos o recibidos) desde SharePoint
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            tipo: Tipo de comunicados ("emitidos" o "recibidos")
            regenerar_todas: Si True, regenera toda la información incluso si ya existe
            
        Returns:
            Lista de comunicados procesados
        """
        if not self.sharepoint_extractor:
            logger.warning("SharePoint extractor no disponible")
            return []
        
        if not self.extractor_observaciones:
            logger.warning("Extractor de observaciones no disponible")
            return []
        
        # Obtener ruta de la carpeta según el tipo
        ruta_carpeta = self.obtener_ruta_carpeta_comunicados(anio, mes, tipo=tipo)
        logger.info(f"Listando archivos en carpeta: {ruta_carpeta}")
        print(f"[INFO] Listando archivos en carpeta: {ruta_carpeta}")
        
        # Listar archivos en la carpeta
        archivos = self.sharepoint_extractor.listar_archivos_en_carpeta(ruta_carpeta)
        logger.info(f"[INFO] Archivos encontrados: {len(archivos)}")
        print(f"[INFO] Archivos encontrados: {len(archivos)}")
        
        if not archivos:
            logger.warning(f"No se encontraron archivos en la carpeta: {ruta_carpeta}")
            return []
        
        comunicados = []
        
        for idx, archivo_info in enumerate(archivos, start=1):
            nombre_archivo = archivo_info.get("nombre", "")
            ruta_completa = archivo_info.get("ruta_completa", "")
            
            # Extraer radicado del nombre del archivo
            radicado = self.extraer_radicado_desde_nombre(nombre_archivo)
            
            # Extraer fecha y asunto del contenido del archivo
            fecha = None
            asunto = None
            
            try:
                # Obtener la ruta de SharePoint si está disponible, sino construirla
                ruta_sharepoint = archivo_info.get("ruta_sharepoint")
                
                if not ruta_sharepoint:
                    # Construir la ruta completa de SharePoint para descargar el archivo
                    # La ruta_completa viene como: "PROYECTOS/Año 2024/.../archivo.pdf"
                    # Necesitamos construir la ruta relativa del servidor: "/sites/OPERACIONES/Shared Documents/..."
                    from urllib.parse import urlparse
                    parsed = urlparse(self.sharepoint_extractor.site_url)
                    site_path_parts = [p for p in parsed.path.split('/') if p]
                    site_path = '/' + '/'.join(site_path_parts)  # ej: /sites/OPERACIONES
                    
                    # Construir ruta relativa del servidor completa
                    # Formato: /sites/OPERACIONES/Shared Documents/PROYECTOS/...
                    ruta_sharepoint = f"{site_path}/Shared Documents/{ruta_completa}"
                
                logger.info(f"[DEBUG] Extrayendo texto del archivo: {nombre_archivo}")
                logger.info(f"[DEBUG] Ruta completa relativa: {ruta_completa}")
                logger.info(f"[DEBUG] Ruta SharePoint (server relative): {ruta_sharepoint}")
                
                # Usar el método que descarga desde SharePoint directamente
                texto_archivo = self.extractor_observaciones._extraer_texto_desde_sharepoint(ruta_sharepoint)
                
                if texto_archivo and len(texto_archivo.strip()) > 50:
                    logger.info(f"[DEBUG] Texto extraído exitosamente: {len(texto_archivo)} caracteres")
                    logger.info(f"[DEBUG] Primeros 300 caracteres: {texto_archivo[:300]}")
                    
                    # Usar LLM para extraer fecha y asunto
                    resultado_llm = self.extractor_observaciones.extraer_fecha_y_asunto_comunicado(texto_archivo)
                    fecha = resultado_llm.get("fecha")
                    asunto = resultado_llm.get("asunto")
                    
                    logger.info(f"[SUCCESS] Procesado archivo {nombre_archivo}: fecha={fecha}, asunto={asunto[:100] if asunto else None}...")
                else:
                    logger.warning(f"[WARNING] No se pudo extraer texto del archivo o texto muy corto: {nombre_archivo}")
                    logger.warning(f"[WARNING] Longitud del texto: {len(texto_archivo) if texto_archivo else 0} caracteres")
            
            except Exception as e:
                logger.error(f"Error al procesar archivo {nombre_archivo}: {e}")
                import traceback
                traceback.print_exc()
                # Continuar con el siguiente archivo
            
            comunicado = {
                "item": idx,
                "radicado": radicado or nombre_archivo.rsplit('.', 1)[0] if '.' in nombre_archivo else nombre_archivo,
                "fecha": fecha or "No disponible",
                "asunto": asunto or "No disponible",
                "nombre_archivo": nombre_archivo,
                "ruta_completa": ruta_completa
            }
            
            comunicados.append(comunicado)
        
        logger.info(f"Se procesaron {len(comunicados)} comunicados {tipo}")
        return comunicados
    
    def procesar_comunicados_emitidos(
        self,
        anio: int,
        mes: int,
        regenerar_todas: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Procesa los comunicados emitidos desde SharePoint
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            regenerar_todas: Si True, regenera toda la información incluso si ya existe
            
        Returns:
            Lista de comunicados procesados
        """
        return self.procesar_comunicados(anio, mes, tipo="emitidos", regenerar_todas=regenerar_todas)
    
    def procesar_comunicados_recibidos(
        self,
        anio: int,
        mes: int,
        regenerar_todas: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Procesa los comunicados recibidos desde SharePoint
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            regenerar_todas: Si True, regenera toda la información incluso si ya existe
            
        Returns:
            Lista de comunicados procesados
        """
        return self.procesar_comunicados(anio, mes, tipo="recibidos", regenerar_todas=regenerar_todas)
    
    async def guardar_comunicados_en_mongodb(
        self,
        comunicados: List[Dict[str, Any]],
        anio: int,
        mes: int,
        seccion: int = 1,
        subseccion: str = "1.6.1",
        tipo: str = "emitidos",
        user_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Guarda los comunicados emitidos en MongoDB
        
        Args:
            comunicados: Lista de comunicados procesados
            anio: Año del informe
            mes: Mes del informe
            seccion: Número de sección (por defecto 1)
            subseccion: Subsección (por defecto "1.6.1")
            user_id: ID del usuario que realiza la operación (opcional)
            
        Returns:
            Documento guardado en MongoDB o None si falla
        """
        try:
            documento = await self.repository.guardar_comunicados(
                comunicados=comunicados,
                anio=anio,
                mes=mes,
                seccion=seccion,
                subseccion=subseccion,
                tipo=tipo,
                user_id=user_id
            )
            return documento
        except Exception as e:
            logger.error(f"Error al guardar comunicados en MongoDB: {e}")
            return None

