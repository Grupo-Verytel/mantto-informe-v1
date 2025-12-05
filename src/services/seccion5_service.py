"""
Service para procesar datos de laboratorio desde Excel en SharePoint y guardarlos en MongoDB
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
import pandas as pd
from urllib.parse import urlparse
from src.repositories.laboratorio_repository import LaboratorioRepository
from src.extractores.sharepoint_extractor import SharePointExtractor
import config

logger = logging.getLogger(__name__)


class Seccion5Service:
    """Service para procesar datos de laboratorio desde SharePoint"""
    
    def __init__(self):
        self.laboratorio_repo = LaboratorioRepository()
        self.sharepoint_extractor = SharePointExtractor()
    
    def _obtener_nombre_archivo_excel(self, mes: int) -> str:
        """
        Obtiene el nombre del archivo Excel según el mes
        
        Args:
            mes: Mes del informe (1-12)
            
        Returns:
            Nombre del archivo (ej: "ANEXO_SEPTIEMBRE.xlsx")
        """
        nombre_mes = config.MESES[mes].upper()
        return f"ANEXO_{nombre_mes}.xlsx"
    
    def _construir_ruta_sharepoint(self, ruta_personalizada: Optional[str] = None) -> str:
        """
        Construye la ruta en SharePoint donde se encuentra el archivo Excel
        
        Args:
            ruta_personalizada: Ruta personalizada (opcional). Si no se proporciona, usa la ruta por defecto
            
        Returns:
            Ruta relativa en SharePoint
        """
        if ruta_personalizada:
            return ruta_personalizada
        
        # Ruta por defecto según el usuario
        # /11.%2001SEP%20-%2030SEP/01%20OBLIGACIONES%20GENERALES/OBLIGACI%C3%93N%202,5,6,9,13/ANEXO%20LABORATORIO/
        return "11. 01SEP - 30SEP/01 OBLIGACIONES GENERALES/OBLIGACIÓN 2,5,6,9,13/ANEXO LABORATORIO"
    
    async def procesar_excel_desde_sharepoint(
        self,
        anio: int,
        mes: int,
        ruta_sharepoint: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Procesa el archivo Excel de laboratorio desde SharePoint y lo guarda en MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            ruta_sharepoint: Ruta personalizada en SharePoint (opcional)
            user_id: ID del usuario que realiza la operación
            
        Returns:
            Diccionario con el resultado del procesamiento:
            {
                "success": True/False,
                "message": "Mensaje descriptivo",
                "total_registros": 0,
                "datos": [...],
                "mongodb_id": "..." (opcional)
            }
        """
        try:
            # Obtener nombre del archivo
            nombre_archivo = self._obtener_nombre_archivo_excel(mes)
            logger.info(f"[DEBUG] Procesando archivo de laboratorio: {nombre_archivo}")
            
            # Construir ruta completa en SharePoint
            ruta_carpeta = self._construir_ruta_sharepoint(ruta_sharepoint)
            
            # Mostrar información de configuración de SharePoint
            logger.info("=" * 80)
            logger.info("[DEBUG] CONFIGURACIÓN SHAREPOINT PARA LABORATORIO")
            logger.info("=" * 80)
            logger.info(f"[DEBUG] Site URL: {self.sharepoint_extractor.site_url}")
            logger.info(f"[DEBUG] Base Path configurado: '{self.sharepoint_extractor.base_path}'")
            logger.info(f"[DEBUG] Ruta carpeta construida: '{ruta_carpeta}'")
            logger.info(f"[DEBUG] Ruta SharePoint recibida como parámetro: '{ruta_sharepoint}'")
            logger.info(f"[DEBUG] Nombre archivo: '{nombre_archivo}'")
            
            # Si la ruta personalizada ya incluye el nombre del archivo, usarla directamente
            if ruta_sharepoint and nombre_archivo.lower() in ruta_sharepoint.lower():
                ruta_completa = ruta_sharepoint
                logger.info(f"[DEBUG] Ruta personalizada ya incluye el archivo, usando directamente: {ruta_completa}")
            else:
                # Construir ruta completa: carpeta + nombre archivo
                ruta_completa = f"{ruta_carpeta}/{nombre_archivo}"
                logger.info(f"[DEBUG] Ruta completa construida: '{ruta_completa}'")
            
            # Mostrar cómo se construirá la ruta relativa del servidor
            if self.sharepoint_extractor.base_path:
                # La ruta relativa del servidor será: /sites/OPERACIONES/[base_path]/[ruta_completa]
                sitio_parsed = urlparse(self.sharepoint_extractor.site_url)
                sitio_path_parts = [p for p in sitio_parsed.path.split('/') if p]
                base_path_parts = [p for p in self.sharepoint_extractor.base_path.strip('/').split('/') if p]
                ruta_completa_parts = [p for p in ruta_completa.split('/') if p]
                
                server_relative_url_parts = sitio_path_parts + base_path_parts + ruta_completa_parts
                server_relative_url = '/' + '/'.join(server_relative_url_parts)
                
                logger.info(f"[DEBUG] Ruta relativa del servidor que se construirá:")
                logger.info(f"[DEBUG]   /sites/OPERACIONES + [base_path] + [ruta_completa]")
                logger.info(f"[DEBUG]   = {server_relative_url}")
            else:
                logger.info(f"[DEBUG] No hay base_path configurado, ruta será relativa al sitio")
            
            logger.info("=" * 80)
            
            # Intentar descargar directamente (más confiable que verificar primero)
            logger.info(f"Intentando descargar archivo desde SharePoint...")
            archivo_temp = None
            archivo_encontrado = False
            nombre_archivo_final = nombre_archivo  # Mantener el nombre original
            
            # Primero intentar con el nombre esperado
            try:
                archivo_temp = self.sharepoint_extractor.descargar_archivo(ruta_completa)
                if archivo_temp and archivo_temp.exists():
                    archivo_encontrado = True
                    logger.info(f"Archivo encontrado y descargado: {nombre_archivo}")
            except Exception as e:
                logger.warning(f"No se pudo descargar con el nombre esperado: {e}")
            
            # Si no se encontró, intentar con variaciones del nombre
            if not archivo_encontrado:
                logger.warning(f"Archivo {nombre_archivo} no encontrado. Intentando variaciones...")
                nombre_mes_alternativo = config.MESES[mes].upper()
                variaciones = [
                    f"ANEXO_{nombre_mes_alternativo}.xlsx",
                    f"anexo_{nombre_mes_alternativo.lower()}.xlsx",
                    f"Anexo_{nombre_mes_alternativo.capitalize()}.xlsx",
                    f"ANEXO_{mes:02d}.xlsx",
                    f"ANEXO_{mes}.xlsx"
                ]
                
                for variacion in variaciones:
                    ruta_variacion = f"{ruta_carpeta}/{variacion}"
                    logger.info(f"Intentando con variación: {variacion}")
                    try:
                        archivo_temp = self.sharepoint_extractor.descargar_archivo(ruta_variacion)
                        if archivo_temp and archivo_temp.exists():
                            logger.info(f"Archivo encontrado con variación: {variacion}")
                            nombre_archivo_final = variacion
                            ruta_completa = ruta_variacion
                            archivo_encontrado = True
                            break
                    except Exception as e:
                        logger.debug(f"Variación {variacion} no funcionó: {e}")
                        continue
            
            # Si aún no se encontró, listar archivos en la carpeta para diagnóstico
            if not archivo_encontrado:
                logger.warning(f"Archivo no encontrado. Listando archivos en la carpeta para diagnóstico...")
                try:
                    archivos_en_carpeta = self.sharepoint_extractor.listar_archivos_en_carpeta(ruta_carpeta)
                    if archivos_en_carpeta:
                        logger.info(f"Archivos encontrados en la carpeta '{ruta_carpeta}':")
                        nombres_archivos = [archivo.get('nombre', 'N/A') for archivo in archivos_en_carpeta]
                        for i, nombre in enumerate(nombres_archivos[:10], 1):  # Mostrar primeros 10
                            logger.info(f"  {i}. {nombre}")
                        
                        # Buscar archivos que contengan "ANEXO" o el nombre del mes
                        archivos_similares = [a for a in nombres_archivos if 'ANEXO' in a.upper() or nombre_mes_alternativo.upper() in a.upper()]
                        if archivos_similares:
                            logger.info(f"Archivos similares encontrados: {archivos_similares}")
                except Exception as e:
                    logger.warning(f"No se pudieron listar archivos en la carpeta: {e}")
                
                # Log detallado de las rutas intentadas
                logger.error(f"[ERROR] No se encontró el archivo después de intentar todas las variaciones")
                logger.error(f"[ERROR] Ruta carpeta base: '{ruta_carpeta}'")
                logger.error(f"[ERROR] Nombre archivo esperado: '{nombre_archivo}'")
                logger.error(f"[ERROR] Ruta completa final intentada: '{ruta_completa}'")
                logger.error(f"[ERROR] Ruta SharePoint recibida como parámetro: '{ruta_sharepoint}'")
                
                mensaje_error = (
                    f"No se encontró el archivo '{nombre_archivo}' en SharePoint.\n"
                    f"Ruta carpeta usada: '{ruta_carpeta}'\n"
                    f"Ruta completa intentada: '{ruta_completa}'\n"
                )
                if ruta_sharepoint:
                    mensaje_error += f"Ruta personalizada recibida: '{ruta_sharepoint}'\n"
                else:
                    mensaje_error += "Se usó la ruta por defecto.\n"
                
                return {
                    "success": False,
                    "message": mensaje_error,
                    "detalle": {
                        "ruta_carpeta": ruta_carpeta,
                        "nombre_archivo": nombre_archivo,
                        "ruta_completa_intentada": ruta_completa,
                        "ruta_sharepoint_parametro": ruta_sharepoint,
                        "ruta_por_defecto": "11. 01SEP - 30SEP/01 OBLIGACIONES GENERALES/OBLIGACIÓN 2,5,6,9,13/ANEXO LABORATORIO"
                    },
                    "total_registros": 0,
                    "datos": []
                }
            
            # Actualizar nombre_archivo si se encontró con una variación
            nombre_archivo = nombre_archivo_final
            
            logger.info(f"Archivo descargado exitosamente: {archivo_temp}")
            
            try:
                # Leer la hoja 2 del Excel
                # Nota: pandas usa índice 0 para la primera hoja, así que hoja 2 = índice 1
                logger.info(f"Leyendo hoja 2 del archivo Excel...")
                try:
                    # Intentar leer por índice (1 = segunda hoja)
                    df = pd.read_excel(archivo_temp, sheet_name=1)
                except Exception as e:
                    logger.warning(f"No se pudo leer la hoja 2 por índice, intentando por nombre...")
                    # Intentar leer por nombre común
                    nombres_hojas = ["Hoja2", "Sheet2", "Datos", "Laboratorio"]
                    df = None
                    for nombre in nombres_hojas:
                        try:
                            df = pd.read_excel(archivo_temp, sheet_name=nombre)
                            logger.info(f"Hoja encontrada con nombre: {nombre}")
                            break
                        except:
                            continue
                    
                    if df is None:
                        # Si no se encuentra, leer la primera hoja disponible
                        logger.warning("No se encontró hoja 2, leyendo primera hoja disponible...")
                        df = pd.read_excel(archivo_temp, sheet_name=0)
                
                if df.empty:
                    logger.warning("La hoja 2 está vacía")
                    return {
                        "success": False,
                        "message": "La hoja 2 del archivo Excel está vacía",
                        "total_registros": 0,
                        "datos": []
                    }
                
                logger.info(f"DataFrame leído: {len(df)} filas, {len(df.columns)} columnas")
                logger.info(f"Columnas encontradas: {list(df.columns)}")
                
                # Normalizar nombres de columnas (eliminar espacios, convertir a mayúsculas)
                df.columns = df.columns.str.strip().str.upper()
                
                # Mapear columnas esperadas (pueden variar en el Excel)
                columnas_esperadas = {
                    "ID": ["ID", "ÍTEM", "ITEM", "NÚMERO", "NUMERO"],
                    "FECHA": ["FECHA", "FECHA DE REGISTRO", "FECHA_REGISTRO"],
                    "PUNTO": ["PUNTO", "PUNTO DE INSTALACIÓN", "PUNTO_INSTALACION", "UBICACIÓN", "UBICACION"],
                    "EQUIPO": ["EQUIPO", "EQUIPO INSTALADO", "EQUIPO_INSTALADO", "TIPO EQUIPO"],
                    "SERIAL": ["SERIAL", "NÚMERO DE SERIE", "NUMERO_SERIE", "SERIAL NUMBER"],
                    "ESTADO": ["ESTADO", "ESTADO DEL EQUIPO", "ESTADO_EQUIPO", "CONDICIÓN", "CONDICION"],
                    "RADICADO": ["RADICADO", "NÚMERO RADICADO", "NUMERO_RADICADO", "RADICADO ETB"],
                    "APROBACION": ["APROBACIÓN", "APROBACION", "ESTADO APROBACIÓN", "ESTADO_APROBACION", "APROBADO"]
                }
                
                # Encontrar las columnas reales en el DataFrame
                columnas_encontradas = {}
                for columna_esperada, variaciones in columnas_esperadas.items():
                    for variacion in variaciones:
                        if variacion in df.columns:
                            columnas_encontradas[columna_esperada] = variacion
                            break
                
                logger.info(f"Columnas mapeadas: {columnas_encontradas}")
                
                # Verificar que se encontraron las columnas mínimas
                columnas_minimas = ["ID", "FECHA", "PUNTO", "EQUIPO", "SERIAL", "ESTADO", "RADICADO", "APROBACION"]
                columnas_faltantes = [col for col in columnas_minimas if col not in columnas_encontradas]
                
                if columnas_faltantes:
                    logger.warning(f"Columnas faltantes: {columnas_faltantes}")
                    logger.info(f"Columnas disponibles en el Excel: {list(df.columns)}")
                
                # Extraer datos de la tabla
                datos_laboratorio = []
                for idx, row in df.iterrows():
                    # Saltar filas vacías
                    if row.isna().all():
                        continue
                    
                    registro = {}
                    for columna_esperada, columna_real in columnas_encontradas.items():
                        valor = row.get(columna_real, "")
                        # Convertir a string y limpiar
                        if pd.notna(valor):
                            registro[columna_esperada.lower()] = str(valor).strip()
                        else:
                            registro[columna_esperada.lower()] = ""
                    
                    # Agregar índice si no hay ID
                    if "id" not in registro or not registro["id"]:
                        registro["id"] = str(idx + 1)
                    
                    # Solo agregar si tiene al menos algunos datos
                    if any(registro.values()):
                        datos_laboratorio.append(registro)
                
                logger.info(f"Registros extraídos: {len(datos_laboratorio)}")
                
                if not datos_laboratorio:
                    return {
                        "success": False,
                        "message": "No se encontraron datos válidos en la hoja 2 del archivo Excel",
                        "total_registros": 0,
                        "datos": []
                    }
                
                # Guardar en MongoDB
                logger.info(f"Guardando {len(datos_laboratorio)} registros en MongoDB...")
                documento_guardado = await self.laboratorio_repo.guardar_datos_laboratorio(
                    anio=anio,
                    mes=mes,
                    datos_laboratorio=datos_laboratorio,
                    user_id=user_id
                )
                
                mongodb_id = None
                if documento_guardado:
                    mongodb_id = str(documento_guardado.get("_id", ""))
                    logger.info(f"Datos guardados en MongoDB con ID: {mongodb_id}")
                
                return {
                    "success": True,
                    "message": f"Archivo procesado exitosamente. {len(datos_laboratorio)} registros guardados en MongoDB",
                    "total_registros": len(datos_laboratorio),
                    "datos": datos_laboratorio,
                    "mongodb_id": mongodb_id,
                    "archivo": nombre_archivo,
                    "ruta_sharepoint": ruta_completa
                }
                
            finally:
                # Limpiar archivo temporal
                try:
                    if archivo_temp.exists():
                        archivo_temp.unlink()
                        logger.info(f"Archivo temporal eliminado: {archivo_temp}")
                except Exception as e:
                    logger.warning(f"Error al eliminar archivo temporal: {e}")
                    
        except Exception as e:
            logger.error(f"Error al procesar Excel desde SharePoint: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error al procesar el archivo Excel: {str(e)}",
                "total_registros": 0,
                "datos": []
            }
    
    async def obtener_datos_laboratorio(
        self,
        anio: int,
        mes: int
    ) -> Optional[Dict[str, Any]]:
        """
        Obtiene los datos de laboratorio desde MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            
        Returns:
            Documento con los datos de laboratorio o None si no existe
        """
        return await self.laboratorio_repo.obtener_datos_laboratorio(anio, mes)
    
    async def cargar_datos_desde_mongodb(
        self,
        anio: int,
        mes: int,
        generador
    ) -> None:
        """
        Carga datos desde MongoDB y los asigna al generador
        
        Args:
            anio: Año del informe
            mes: Mes del informe
            generador: Instancia del generador de sección 5
        """
        try:
            logger.info(f"Cargando datos de laboratorio desde MongoDB para {anio}-{mes}...")
            
            documento = await self.laboratorio_repo.obtener_datos_laboratorio(anio, mes)
            
            if documento:
                datos_laboratorio = documento.get("datos_laboratorio", [])
                generador.datos_laboratorio_raw = datos_laboratorio
                logger.info(f"Datos de laboratorio cargados: {len(datos_laboratorio)} registros")
            else:
                logger.warning(f"No se encontraron datos de laboratorio para {anio}-{mes}")
                generador.datos_laboratorio_raw = []
                
        except Exception as e:
            logger.error(f"Error al cargar datos desde MongoDB: {e}")
            import traceback
            traceback.print_exc()
            generador.datos_laboratorio_raw = []
    
    async def generar_seccion5(
        self,
        anio: int,
        mes: int,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Genera el documento de la sección 5 desde MongoDB
        
        Args:
            anio: Año del informe
            mes: Mes del informe (1-12)
            output_path: Ruta donde guardar el documento. Si None, usa directorio de salida por defecto
            
        Returns:
            Path al archivo generado
        """
        from src.generadores.seccion_5_laboratorio import GeneradorSeccion5
        import config
        
        # Crear generador
        generador = GeneradorSeccion5(
            anio=anio,
            mes=mes,
            cargar_desde_mongodb=True
        )
        
        # Cargar datos desde MongoDB
        await self.cargar_datos_desde_mongodb(anio, mes, generador)
        
        # Determinar ruta de salida
        if output_path is None:
            output_path = config.OUTPUT_DIR / f"seccion_5_{anio}_{mes:02d}.docx"
        
        # Asegurar que el directorio existe
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generar y guardar el documento
        generador.guardar(output_path)
        
        logger.info(f"Sección 5 generada exitosamente en: {output_path}")
        return output_path

