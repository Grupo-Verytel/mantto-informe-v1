"""
Extractor de observaciones desde archivos de anexos usando LLM
"""
from typing import Dict, Optional, List
from pathlib import Path
import os
import tempfile
import config
from src.extractores.sharepoint_extractor import get_sharepoint_extractor

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Intentar importar OpenAI
try:
    from openai import OpenAI
    OPENAI_DISPONIBLE = True
except ImportError:
    OPENAI_DISPONIBLE = False
    print("[WARNING] openai no está disponible. Las observaciones se generarán de forma estática.")

# Intentar importar otras librerías para lectura de PDFs
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


class ExtractorObservaciones:
    """Extrae observaciones de cumplimiento desde archivos de anexos usando LLM"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini",
                 sharepoint_site_url: Optional[str] = None, sharepoint_client_id: Optional[str] = None,
                 sharepoint_client_secret: Optional[str] = None, sharepoint_base_path: Optional[str] = None):
        """
        Inicializa el extractor de observaciones
        
        Args:
            api_key: API key de OpenAI (o usar variable de entorno OPENAI_API_KEY)
            model: Modelo de OpenAI a usar (default: gpt-4o-mini)
            sharepoint_site_url: URL del sitio de SharePoint
            sharepoint_client_id: Client ID para autenticación de aplicación
            sharepoint_client_secret: Client Secret para autenticación de aplicación
            sharepoint_base_path: Ruta base adicional en SharePoint (ej: "Documentos compartidos")
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or getattr(config, 'OPENAI_API_KEY', None)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini") or getattr(config, 'OPENAI_MODEL', "gpt-4o-mini")
        self.client = None
        
        if OPENAI_DISPONIBLE and self.api_key:
            try:
                # Inicializar cliente OpenAI - usar variable de entorno si está disponible
                # o pasar api_key explícitamente
                if os.getenv("OPENAI_API_KEY"):
                    # Si está en variable de entorno, OpenAI() la detecta automáticamente
                    self.client = OpenAI()
                else:
                    # Si no está en variable de entorno, pasarla explícitamente
                    self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"[WARNING] Error al inicializar cliente OpenAI: {e}")
                print(f"[INFO] Intentando con configuración alternativa...")
                try:
                    # Intentar solo con variable de entorno
                    self.client = OpenAI()
                except Exception as e2:
                    print(f"[WARNING] Error al inicializar cliente OpenAI (fallback): {e2}")
                    self.client = None
        
        # Inicializar extractor de SharePoint
        self.sharepoint_extractor = get_sharepoint_extractor(
            site_url=sharepoint_site_url,
            client_id=sharepoint_client_id,
            client_secret=sharepoint_client_secret,
            base_path=sharepoint_base_path
        )
        self.archivos_temporales = []  # Para limpiar archivos descargados
    
    def extraer_texto_archivo(self, ruta_archivo: str) -> str:
        """
        Extrae texto de un archivo (PDF, DOCX, TXT)
        Soporta archivos locales y desde SharePoint
        
        Args:
            ruta_archivo: Ruta al archivo (local, Path, o URL de SharePoint)
            
        Returns:
            Texto extraído del archivo
        """
        # Si es Path, convertir a string
        if isinstance(ruta_archivo, Path):
            ruta_archivo = str(ruta_archivo)
        
        # Verificar si es URL de SharePoint (solo URLs completas, no rutas relativas del servidor)
        if isinstance(ruta_archivo, str) and self.sharepoint_extractor.es_url_sharepoint(ruta_archivo):
            print(f"[DEBUG] Detectada URL de SharePoint, descargando...")
            return self._extraer_texto_desde_sharepoint(ruta_archivo)
        
        # Verificar si es ruta relativa del servidor (comienza con /sites/, /teams/, etc.)
        if isinstance(ruta_archivo, str) and (ruta_archivo.startswith('/sites/') or ruta_archivo.startswith('/teams/') or ruta_archivo.startswith('/personal/')):
            print(f"[DEBUG] Detectada ruta relativa del servidor, descargando desde SharePoint...")
            return self._extraer_texto_desde_sharepoint(ruta_archivo)
        
        # Convertir a Path si es string
        if isinstance(ruta_archivo, str):
            ruta_archivo = Path(ruta_archivo)
        
        if not ruta_archivo.exists():
            print(f"[WARNING] Archivo no existe: {ruta_archivo}")
            return ""
        
        extension = ruta_archivo.suffix.lower()
        print(f"[DEBUG] Extrayendo texto de archivo local: {ruta_archivo} (extensión: {extension})")
        
        try:
            if extension == '.pdf' and PDF_DISPONIBLE:
                texto = self._leer_pdf(ruta_archivo)
                print(f"[DEBUG] Texto extraído de PDF: {len(texto)} caracteres")
                return texto
            elif extension in ['.docx', '.doc'] and DOCX_DISPONIBLE:
                texto = self._leer_docx(ruta_archivo)
                print(f"[DEBUG] Texto extraído de DOCX: {len(texto)} caracteres")
                return texto
            elif extension == '.txt':
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    texto = f.read()
                print(f"[DEBUG] Texto extraído de TXT: {len(texto)} caracteres")
                return texto
            else:
                print(f"[WARNING] Formato no soportado: {extension}")
                return ""
        except Exception as e:
            print(f"[WARNING] Error al leer archivo {ruta_archivo}: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _extraer_texto_desde_sharepoint(self, url_sharepoint: str) -> str:
        """
        Extrae texto de un archivo desde SharePoint
        
        Args:
            url_sharepoint: URL del archivo en SharePoint o ruta relativa del servidor
            
        Returns:
            Texto extraído del archivo
        """
        print(f"[INFO] Descargando archivo desde SharePoint: {url_sharepoint}")
        print(f"[DEBUG] Tipo de ruta: {'URL completa' if url_sharepoint.startswith('http') else 'Ruta relativa del servidor'}")
        
        # Descargar archivo temporalmente
        try:
            archivo_temp = self.sharepoint_extractor.descargar_archivo(url_sharepoint)
        except Exception as e:
            print(f"[ERROR] Error al descargar archivo desde SharePoint: {e}")
            import traceback
            traceback.print_exc()
            return ""
        
        if not archivo_temp:
            print(f"[WARNING] No se pudo descargar archivo desde SharePoint (retornó None): {url_sharepoint}")
            return ""
        
        if not archivo_temp.exists():
            print(f"[WARNING] Archivo descargado no existe: {archivo_temp}")
            return ""
        
        tamaño = archivo_temp.stat().st_size
        print(f"[INFO] Archivo descargado exitosamente: {archivo_temp} (tamaño: {tamaño} bytes)")
        
        if tamaño == 0:
            print(f"[WARNING] El archivo descargado está vacío (0 bytes)")
            return ""
        
        # Guardar referencia para limpiar después
        self.archivos_temporales.append(archivo_temp)
        
        # Extraer texto del archivo descargado
        try:
            # Pasar como Path, no como string, para que se lea como archivo local
            texto = self.extraer_texto_archivo(str(archivo_temp))
            print(f"[INFO] Texto extraído del archivo: {len(texto)} caracteres")
            if len(texto) > 0:
                print(f"[DEBUG] Primeros 200 caracteres del texto: {texto[:200]}...")
            else:
                print(f"[WARNING] No se pudo extraer texto del archivo (archivo puede estar corrupto o ser imagen)")
            return texto
        except Exception as e:
            print(f"[ERROR] Error al extraer texto del archivo: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _leer_pdf(self, ruta: Path) -> str:
        """Lee texto de un archivo PDF"""
        texto = ""
        try:
            with open(ruta, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    texto += page.extract_text() + "\n"
        except Exception as e:
            print(f"[WARNING] Error al leer PDF {ruta}: {e}")
        return texto
    
    def _leer_docx(self, ruta: Path) -> str:
        """Lee texto de un archivo DOCX"""
        texto = ""
        try:
            doc = DocxDocument(ruta)
            for para in doc.paragraphs:
                texto += para.text + "\n"
        except Exception as e:
            print(f"[WARNING] Error al leer DOCX {ruta}: {e}")
        return texto
    
    def generar_observacion_llm(self, texto_anexo: str, obligacion: str, 
                                periodicidad: str, cumplio: str) -> str:
        """
        Genera observación de cumplimiento usando LLM basándose en el contenido del anexo
        
        Args:
            texto_anexo: Texto extraído del archivo de anexo
            obligacion: Texto de la obligación
            periodicidad: Periodicidad de la obligación
            cumplio: Estado de cumplimiento ("Cumplió" o "No Cumplió")
            
        Returns:
            Observación generada
        """
        if not self.client or not OPENAI_DISPONIBLE:
            # Fallback: retornar observación genérica
            return self._generar_observacion_fallback(obligacion, cumplio)
        
        if not texto_anexo or len(texto_anexo.strip()) < 50:
            # Si el texto es muy corto, usar fallback
            return self._generar_observacion_fallback(obligacion, cumplio)
        
        try:
            prompt = f"""Eres un asistente que genera observaciones de cumplimiento contractual para informes técnicos.

CONTEXTO:
- Obligación: {obligacion}
- Periodicidad: {periodicidad}
- Estado: {cumplio}

CONTENIDO DEL ANEXO:
{texto_anexo[:4000]}  # Limitar a 4000 caracteres para evitar tokens excesivos

INSTRUCCIONES:
Genera una observación profesional y concisa (máximo 200 palabras) que:
1. Confirme el cumplimiento de la obligación
2. Haga referencia específica al contenido del anexo
3. Sea apropiada para un informe técnico formal
4. Use lenguaje profesional y técnico
5. Mencione detalles relevantes del anexo si son importantes

Formato: Texto corrido, sin viñetas ni listas.

OBSERVACIÓN:"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en redacción de informes técnicos y contractuales."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3  # Baja temperatura para respuestas más determinísticas
            )
            
            observacion = response.choices[0].message.content.strip()
            return observacion
            
        except Exception as e:
            print(f"[WARNING] Error al generar observación con LLM: {e}")
            return self._generar_observacion_fallback(obligacion, cumplio)
    
    def _generar_observacion_fallback(self, obligacion: str, cumplio: str) -> str:
        """
        Genera observación genérica cuando no hay LLM disponible
        
        Args:
            obligacion: Texto de la obligación
            cumplio: Estado de cumplimiento
            
        Returns:
            Observación genérica
        """
        if cumplio == "Cumplió":
            # Extraer palabras clave de la obligación
            if "Constitución" in obligacion or "Ley" in obligacion:
                return "La EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ S.A. E.S.P acata la Constitución, la Ley, las normas legales y procedimientos establecidos por el Gobierno Nacional y Distrital, y demás disposiciones pertinentes."
            elif "especificaciones" in obligacion.lower() or "propuesta" in obligacion.lower():
                return "Se da cumplimiento con el presente informe y sus anexos."
            elif "Seguridad Social" in obligacion or "salud" in obligacion.lower():
                return "Se acredita el cumplimiento del Sistema de Seguridad Social, incluyendo salud, pensión, aportes parafiscales y riesgos laborales, mediante la presentación de las planillas de pago correspondientes y los certificados respectivos."
            else:
                return f"Se da cumplimiento a la obligación: {obligacion[:100]}..."
        else:
            return f"No se cumplió la obligación: {obligacion[:100]}..."
    
    def procesar_obligacion(self, obligacion: Dict) -> Dict:
        """
        Procesa una obligación y genera observación dinámica desde el anexo
        
        Args:
            obligacion: Diccionario con obligación (debe tener 'anexo', 'obligacion', 'periodicidad', 'cumplio')
            
        Returns:
            Obligación con observación actualizada
        """
        ruta_anexo = obligacion.get("anexo", "")
        
        # Si ya tiene observación y no queremos regenerarla, retornar tal cual
        if obligacion.get("observaciones") and not obligacion.get("regenerar_observacion", False):
            return obligacion
        
        # Intentar extraer texto del anexo
        texto_anexo = ""
        if ruta_anexo and ruta_anexo != "-":
            # Convertir ruta relativa a Path absoluto
            # Las rutas vienen como: "01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 1,7,8,9,10,11,13,14 y 15/ Oficio Obli SEPTIEMBRE 2025.pdf"
            print(f"[INFO] Procesando anexo para obligación {obligacion.get('item', 'N/A')}: {ruta_anexo}")
            ruta_completa = self._resolver_ruta_anexo(ruta_anexo)
            if ruta_completa:
                print(f"[INFO] Ruta resuelta: {ruta_completa}")
                print(f"[INFO] Extrayendo texto del anexo...")
                texto_anexo = self.extraer_texto_archivo(ruta_completa)
                print(f"[INFO] Texto extraído: {len(texto_anexo)} caracteres")
                if len(texto_anexo) == 0:
                    print(f"[WARNING] No se pudo extraer texto del anexo (archivo puede estar vacío o corrupto)")
            else:
                print(f"[WARNING] No se pudo resolver ruta del anexo: {ruta_anexo}")
        else:
            print(f"[INFO] No hay anexo para la obligación {obligacion.get('item', 'N/A')}")
        
        # Generar observación
        print(f"[INFO] Generando observación con LLM (cliente disponible: {bool(self.client)}, texto disponible: {len(texto_anexo) > 50})")
        observacion = self.generar_observacion_llm(
            texto_anexo=texto_anexo,
            obligacion=obligacion.get("obligacion", ""),
            periodicidad=obligacion.get("periodicidad", ""),
            cumplio=obligacion.get("cumplio", "Cumplió")
        )
        
        # Actualizar obligación con observación generada
        obligacion_actualizada = obligacion.copy()
        obligacion_actualizada["observaciones"] = observacion
        # Marcar si se generó con LLM (si hay texto del anexo, cliente disponible, y no es fallback)
        # Verificar si la observación es diferente del fallback para saber si se usó LLM
        observacion_fallback = self._generar_observacion_fallback(
            obligacion.get("obligacion", ""),
            obligacion.get("cumplio", "Cumplió")
        )
        generada_con_llm = bool(
            texto_anexo and 
            len(texto_anexo.strip()) > 50 and  # Al menos 50 caracteres de texto
            self.client and 
            observacion != observacion_fallback  # La observación es diferente del fallback
        )
        obligacion_actualizada["observacion_generada_llm"] = generada_con_llm
        
        return obligacion_actualizada
    
    def _resolver_ruta_anexo(self, ruta_relativa: str) -> Optional[str]:
        """
        Resuelve una ruta relativa de anexo a Path absoluto o URL de SharePoint
        
        Args:
            ruta_relativa: Ruta como aparece en el JSON (ej: "01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ ...")
                          o URL de SharePoint
            
        Returns:
            Path absoluto al archivo, URL de SharePoint, o None si no se encuentra
        """
        # Verificar si es URL de SharePoint
        if self.sharepoint_extractor.es_url_sharepoint(ruta_relativa):
            return ruta_relativa
        
        # Normalizar ruta (reemplazar espacios y caracteres especiales)
        ruta_normalizada = ruta_relativa.replace(" / ", "/").replace(" /", "/").replace("/ ", "/")
        
        # Buscar en diferentes ubicaciones posibles
        ubicaciones_posibles = [
            config.OUTPUT_DIR / ruta_normalizada,
            config.DATA_DIR / "anexos" / ruta_normalizada,
            config.DATA_DIR / "fuentes" / ruta_normalizada,
            Path(ruta_normalizada),  # Ruta absoluta
        ]
        
        for ubicacion in ubicaciones_posibles:
            if ubicacion.exists():
                return str(ubicacion)
        
        # Intentar buscar solo el nombre del archivo
        nombre_archivo = Path(ruta_relativa).name
        for ubicacion_base in [config.OUTPUT_DIR, config.DATA_DIR / "anexos", config.DATA_DIR / "fuentes"]:
            for archivo in ubicacion_base.rglob(nombre_archivo):
                return str(archivo)
        
        # Intentar buscar en SharePoint si está configurado
        if self.sharepoint_extractor.site_url:
            # Si la ruta no es una URL completa, construir ruta relativa del servidor
            # Las rutas vienen como: "01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ archivo.pdf"
            # Necesitamos convertir a: "/sites/OPERACIONES/[base_path]/01SEP - 30SEP/01 OBLIGACIONES GENERALES/archivo.pdf"
            
            # Extraer la ruta base del sitio (ej: /sites/OPERACIONES)
            from urllib.parse import urlparse
            sitio_parsed = urlparse(self.sharepoint_extractor.site_url)
            sitio_path_parts = [p for p in sitio_parsed.path.split('/') if p]
            
            print(f"[DEBUG] Resolviendo ruta de SharePoint:")
            print(f"  - Ruta original: {ruta_relativa}")
            print(f"  - Ruta normalizada: {ruta_normalizada}")
            print(f"  - Site URL: {self.sharepoint_extractor.site_url}")
            print(f"  - Site path parts: {sitio_path_parts}")
            print(f"  - Base path: {self.sharepoint_extractor.base_path}")
            
            # Construir ruta relativa del servidor
            if sitio_path_parts:
                # Ejemplo: sitio_path_parts = ['sites', 'OPERACIONES']
                # base_path = "Documentos/PROYECTOS/Año 2024/..."
                # ruta_normalizada = "01SEP - 30SEP/01 OBLIGACIONES GENERALES/archivo.pdf"
                
                path_parts = sitio_path_parts.copy()
                
                # Agregar base_path si está configurado
                if self.sharepoint_extractor.base_path:
                    base_path_clean = self.sharepoint_extractor.base_path.strip('/').strip()
                    if base_path_clean:
                        # Dividir base_path en partes y agregar cada una
                        base_path_parts = [p for p in base_path_clean.split('/') if p]
                        print(f"  - Base path parts: {base_path_parts}")
                        path_parts.extend(base_path_parts)
                
                # Agregar la ruta del archivo
                ruta_archivo_clean = ruta_normalizada.lstrip('/')
                server_relative_url = '/' + '/'.join(path_parts) + '/' + ruta_archivo_clean
                print(f"[INFO] Intentando buscar en SharePoint con ruta relativa: {server_relative_url}")
                # Retornar la ruta relativa para que SharePoint la use directamente
                return server_relative_url
            else:
                # Fallback: construir URL completa
                ruta_sharepoint = ruta_normalizada.lstrip("/")
                url_sharepoint = f"{self.sharepoint_extractor.site_url.rstrip('/')}/{ruta_sharepoint}"
                print(f"[INFO] Intentando buscar en SharePoint: {url_sharepoint}")
                return url_sharepoint
        
        print(f"[WARNING] No se encontró archivo de anexo: {ruta_relativa}")
        return None
    
    def limpiar_archivos_temporales(self):
        """Limpia archivos temporales descargados de SharePoint"""
        for archivo in self.archivos_temporales:
            try:
                if archivo.exists():
                    archivo.unlink()
            except Exception as e:
                print(f"[WARNING] Error al eliminar archivo temporal {archivo}: {e}")
        self.archivos_temporales.clear()


# Singleton
_extractor_observaciones = None

def get_extractor_observaciones(api_key: Optional[str] = None, model: str = "gpt-4o-mini",
                                sharepoint_site_url: Optional[str] = None,
                                sharepoint_client_id: Optional[str] = None,
                                sharepoint_client_secret: Optional[str] = None,
                                sharepoint_base_path: Optional[str] = None) -> ExtractorObservaciones:
    """Obtiene instancia singleton del extractor de observaciones"""
    global _extractor_observaciones
    if _extractor_observaciones is None:
        _extractor_observaciones = ExtractorObservaciones(
            api_key=api_key,
            model=model,
            sharepoint_site_url=sharepoint_site_url,
            sharepoint_client_id=sharepoint_client_id,
            sharepoint_client_secret=sharepoint_client_secret,
            sharepoint_base_path=sharepoint_base_path
        )
    return _extractor_observaciones

