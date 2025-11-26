"""
Extractor de datos y archivos de SharePoint
"""
from typing import List, Dict, Any, Optional, BinaryIO
from pathlib import Path
import os
import tempfile
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse, quote

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Intentar importar Office365-REST-Python-Client
try:
    from office365.sharepoint.client_context import ClientContext
    from office365.runtime.auth.authentication_context import AuthenticationContext
    OFFICE365_DISPONIBLE = True
except ImportError:
    OFFICE365_DISPONIBLE = False
    print("[WARNING] Office365-REST-Python-Client no está disponible. Usando método alternativo con requests.")


class SharePointExtractor:
    """Extrae archivos y datos desde SharePoint"""
    
    def __init__(self, site_url: Optional[str] = None, client_id: Optional[str] = None,
                 client_secret: Optional[str] = None, base_path: Optional[str] = None):
        """
        Inicializa el extractor de SharePoint
        
        Args:
            site_url: URL del sitio de SharePoint (ej: https://empresa.sharepoint.com/sites/Sitio)
            client_id: Client ID para autenticación de aplicación (requerido)
            client_secret: Client Secret para autenticación de aplicación (requerido)
            base_path: Ruta base adicional en SharePoint (ej: "Documentos compartidos" o carpeta base)
        """
        # Intentar obtener desde parámetros, luego .env, luego config
        try:
            import config as cfg
            self.site_url = site_url or os.getenv("SHAREPOINT_SITE_URL") or getattr(cfg, 'SHAREPOINT_SITE_URL', "")
            self.client_id = client_id or os.getenv("SHAREPOINT_CLIENT_ID") or getattr(cfg, 'SHAREPOINT_CLIENT_ID', "")
            self.client_secret = client_secret or os.getenv("SHAREPOINT_CLIENT_SECRET") or getattr(cfg, 'SHAREPOINT_CLIENT_SECRET', "")
            self.base_path = base_path or os.getenv("SHAREPOINT_BASE_PATH") or getattr(cfg, 'SHAREPOINT_BASE_PATH', "")
        except:
            self.site_url = site_url or os.getenv("SHAREPOINT_SITE_URL", "")
            self.client_id = client_id or os.getenv("SHAREPOINT_CLIENT_ID", "")
            self.client_secret = client_secret or os.getenv("SHAREPOINT_CLIENT_SECRET", "")
            self.base_path = base_path or os.getenv("SHAREPOINT_BASE_PATH", "")
        
        # Deprecated: username y password ya no se usan
        self.username = None
        self.password = None
        self.ctx = None
        
        # Intentar inicializar contexto si hay credenciales
        if self.site_url and OFFICE365_DISPONIBLE:
            try:
                if self.client_id and self.client_secret:
                    # Autenticación con App Registration (único método soportado)
                    self.ctx = ClientContext(self.site_url).with_client_credentials(
                        self.client_id, self.client_secret
                    )
                else:
                    print("[WARNING] SHAREPOINT_CLIENT_ID y SHAREPOINT_CLIENT_SECRET son requeridos")
                    self.ctx = None
            except Exception as e:
                print(f"[WARNING] Error al inicializar SharePoint: {e}")
                self.ctx = None
    
    def descargar_archivo(self, ruta_sharepoint: str, archivo_destino: Optional[Path] = None) -> Optional[Path]:
        """
        Descarga un archivo desde SharePoint
        
        Args:
            ruta_sharepoint: Puede ser:
                            - URL completa (https://...)
                            - Ruta relativa del servidor (/sites/.../archivo.pdf)
                            - Ruta relativa simple (01SEP - 30SEP/...)
            archivo_destino: Ruta donde guardar el archivo (si None, usa archivo temporal)
        
        Returns:
            Path al archivo descargado o None si falla
        """
        """
        Descarga un archivo desde SharePoint
        
        Args:
            ruta_sharepoint: Ruta relativa en SharePoint (ej: "/sites/Sitio/Documentos/archivo.pdf")
                            o URL completa del archivo
            archivo_destino: Ruta donde guardar el archivo (si None, usa archivo temporal)
        
        Returns:
            Path al archivo descargado o None si falla
        """
        # Normalizar ruta y extraer server_relative_url
        server_relative_url = None
        url_archivo = None
        
        if ruta_sharepoint.startswith("http"):
            # Es una URL completa - extraer ruta relativa del servidor
            url_parsed = urlparse(ruta_sharepoint)
            # Construir ruta relativa del servidor (ej: /sites/Sitio/Documentos/archivo.pdf)
            # La URL completa tiene formato: https://dominio.sharepoint.com/sites/Sitio/Documentos/...
            path_parts = [p for p in url_parsed.path.split('/') if p]  # Eliminar vacíos
            
            # Encontrar el índice de 'sites', 'teams' o 'personal'
            try:
                idx = next(i for i, part in enumerate(path_parts) if part in ['sites', 'teams', 'personal'])
                # Construir ruta relativa: /sites/... o /teams/... o /personal/...
                server_relative_url = '/' + '/'.join(path_parts[idx:])
            except StopIteration:
                # Si no encuentra, usar toda la ruta después del dominio
                server_relative_url = url_parsed.path if url_parsed.path.startswith('/') else '/' + url_parsed.path
            
            url_archivo = ruta_sharepoint
        elif ruta_sharepoint.startswith("/"):
            # Es una ruta relativa del servidor (ya tiene /sites/...)
            server_relative_url = ruta_sharepoint
            url_archivo = f"{self.site_url.rstrip('/')}{ruta_sharepoint}"
        else:
            # Es una ruta relativa simple - construir ruta relativa del servidor
            # Extraer la ruta base del sitio (ej: /sites/OPERACIONES)
            sitio_parsed = urlparse(self.site_url)
            sitio_path_parts = [p for p in sitio_parsed.path.split('/') if p]
            
            # Construir ruta relativa del servidor
            if sitio_path_parts:
                # Ejemplo: sitio_path_parts = ['sites', 'OPERACIONES']
                # base_path = "Documentos compartidos" (opcional)
                # ruta_sharepoint = "01SEP - 30SEP/01 OBLIGACIONES GENERALES/archivo.pdf"
                
                # Construir: /sites/OPERACIONES/[base_path]/01SEP - 30SEP/...
                path_parts = sitio_path_parts.copy()
                
                # Agregar base_path si está configurado
                if self.base_path:
                    # Normalizar base_path (eliminar barras iniciales/finales)
                    base_path_clean = self.base_path.strip('/').strip()
                    if base_path_clean:
                        path_parts.append(base_path_clean)
                
                # Agregar la ruta del archivo
                ruta_archivo_clean = ruta_sharepoint.lstrip('/')
                server_relative_url = '/' + '/'.join(path_parts) + '/' + ruta_archivo_clean
            else:
                # Fallback
                server_relative_url = '/' + ruta_sharepoint.lstrip('/')
            
            url_archivo = f"{self.site_url.rstrip('/')}/{ruta_sharepoint.lstrip('/')}"
        
        # Crear archivo temporal si no se especifica destino
        if archivo_destino is None:
            extension = Path(ruta_sharepoint).suffix or ".tmp"
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
            archivo_destino = Path(temp_file.name)
            temp_file.close()
        
        try:
            # Método 1: Usar Office365-REST-Python-Client (si está disponible)
            if self.ctx and OFFICE365_DISPONIBLE:
                return self._descargar_con_office365(server_relative_url, archivo_destino)
            
            # Método 2: Usar requests con autenticación básica
            return self._descargar_con_requests(url_archivo, archivo_destino)
            
        except Exception as e:
            print(f"[WARNING] Error al descargar archivo desde SharePoint: {e}")
            return None
    
    def _descargar_con_office365(self, server_relative_url: str, archivo_destino: Path) -> Optional[Path]:
        """Descarga usando Office365-REST-Python-Client"""
        try:
            # Obtener archivo usando ruta relativa del servidor
            file = self.ctx.web.get_file_by_server_relative_url(server_relative_url)
            self.ctx.load(file)
            self.ctx.execute_query()
            
            # Descargar contenido
            with open(archivo_destino, "wb") as f:
                file.download(f)
                self.ctx.execute_query()
            
            return archivo_destino
        except Exception as e:
            print(f"[WARNING] Error con Office365: {e}")
            return None
    
    def _descargar_con_requests(self, url_archivo: str, archivo_destino: Path) -> Optional[Path]:
        """Descarga usando requests (método alternativo)"""
        try:
            # Headers
            headers = {
                "Accept": "application/json",
            }
            
            # Obtener token OAuth con App Registration
            if self.client_id and self.client_secret:
                token = self._obtener_token_oauth()
                if token:
                    headers["Authorization"] = f"Bearer {token}"
                else:
                    print("[WARNING] No se pudo obtener token OAuth")
                    return None
            else:
                print("[WARNING] SHAREPOINT_CLIENT_ID y SHAREPOINT_CLIENT_SECRET son requeridos")
                return None
            
            # Descargar archivo
            response = requests.get(url_archivo, headers=headers, stream=True)
            response.raise_for_status()
            
            # Guardar archivo
            with open(archivo_destino, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return archivo_destino
            
        except Exception as e:
            print(f"[WARNING] Error con requests: {e}")
            return None
    
    def _obtener_token_oauth(self) -> Optional[str]:
        """
        Obtiene token OAuth para SharePoint usando Client ID y Client Secret
        
        Returns:
            Token de acceso OAuth o None si falla
        """
        if not self.client_id or not self.client_secret:
            return None
        
        try:
            # Extraer tenant ID del site_url
            # Formato: https://{tenant}.sharepoint.com/sites/...
            parsed = urlparse(self.site_url)
            domain = parsed.netloc  # ej: verytelcsp.sharepoint.com
            tenant = domain.split('.')[0]  # ej: verytelcsp
            
            # Usar endpoint de Microsoft Graph para obtener token
            # Para SharePoint, necesitamos usar el endpoint correcto
            # Intentar primero con el tenant extraído, si falla usar "common"
            token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
            
            # Datos para la solicitud
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": f"{self.site_url}/.default",
                "grant_type": "client_credentials"
            }
            
            # Realizar solicitud
            response = requests.post(token_url, data=data)
            
            # Si falla con el tenant específico, intentar con "common"
            if response.status_code != 200:
                print(f"[INFO] Intentando con tenant 'common' (error {response.status_code})")
                token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
                response = requests.post(token_url, data=data)
            
            response.raise_for_status()
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            if access_token:
                print(f"[INFO] Token OAuth obtenido exitosamente")
            return access_token
            
        except Exception as e:
            print(f"[WARNING] Error al obtener token OAuth: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def es_url_sharepoint(self, ruta: str) -> bool:
        """
        Verifica si una ruta es una URL de SharePoint
        
        Args:
            ruta: Ruta a verificar
        
        Returns:
            True si es una URL de SharePoint
        """
        if not ruta:
            return False
        
        # Verificar si es URL
        if not (ruta.startswith("http://") or ruta.startswith("https://")):
            return False
        
        # Verificar dominios comunes de SharePoint
        dominios_sharepoint = [
            "sharepoint.com",
            "sharepointonline.com",
            "microsoftonline.com",
            "office365.com"
        ]
        
        parsed = urlparse(ruta)
        dominio = parsed.netloc.lower()
        
        return any(dom in dominio for dom in dominios_sharepoint)
    
    def buscar_archivo_por_nombre(self, nombre_archivo: str, carpeta_base: str = "/") -> Optional[str]:
        """
        Busca un archivo en SharePoint por nombre
        
        Args:
            nombre_archivo: Nombre del archivo a buscar
            carpeta_base: Carpeta base donde buscar (ruta relativa)
        
        Returns:
            Ruta relativa al archivo encontrado o None
        """
        # TODO: Implementar búsqueda en SharePoint
        # Por ahora retorna None
        return None


# Singleton
_sharepoint_extractor = None

def get_sharepoint_extractor(site_url: Optional[str] = None, client_id: Optional[str] = None,
                            client_secret: Optional[str] = None, base_path: Optional[str] = None) -> SharePointExtractor:
    """Obtiene instancia singleton del extractor de SharePoint"""
    global _sharepoint_extractor
    if _sharepoint_extractor is None:
        _sharepoint_extractor = SharePointExtractor(
            site_url=site_url,
            client_id=client_id,
            client_secret=client_secret,
            base_path=base_path
        )
    return _sharepoint_extractor

def obtener_comunicados_sharepoint(fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
    """
    Obtiene comunicados de SharePoint para un rango de fechas
    
    Args:
        fecha_inicio: Fecha de inicio (formato YYYY-MM-DD)
        fecha_fin: Fecha de fin (formato YYYY-MM-DD)
    
    Returns:
        Lista de diccionarios con los comunicados
    """
    # TODO: Implementar obtención de comunicados desde SharePoint
    return []


