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
                 client_secret: Optional[str] = None, tenant_id: Optional[str] = None,
                 base_path: Optional[str] = None):
        """
        Inicializa el extractor de SharePoint
        
        Args:
            site_url: URL del sitio de SharePoint (ej: https://empresa.sharepoint.com/sites/Sitio)
            client_id: Client ID para autenticación de aplicación (requerido)
            client_secret: Client Secret para autenticación de aplicación (requerido)
            tenant_id: Tenant ID de Azure AD (GUID) - Si no se proporciona, se extrae del dominio
            base_path: Ruta base adicional en SharePoint (ej: "Documentos compartidos" o carpeta base)
        """
        # Intentar obtener desde parámetros, luego .env, luego config
        try:
            import config as cfg
            self.site_url = site_url or os.getenv("SHAREPOINT_SITE_URL") or getattr(cfg, 'SHAREPOINT_SITE_URL', "")
            self.client_id = client_id or os.getenv("SHAREPOINT_CLIENT_ID") or getattr(cfg, 'SHAREPOINT_CLIENT_ID', "")
            self.client_secret = client_secret or os.getenv("SHAREPOINT_CLIENT_SECRET") or getattr(cfg, 'SHAREPOINT_CLIENT_SECRET', "")
            self.tenant_id = tenant_id or os.getenv("SHAREPOINT_TENANT_ID") or getattr(cfg, 'SHAREPOINT_TENANT_ID', "")
            self.base_path = base_path or os.getenv("SHAREPOINT_BASE_PATH") or getattr(cfg, 'SHAREPOINT_BASE_PATH', "")
        except:
            self.site_url = site_url or os.getenv("SHAREPOINT_SITE_URL", "")
            self.client_id = client_id or os.getenv("SHAREPOINT_CLIENT_ID", "")
            self.client_secret = client_secret or os.getenv("SHAREPOINT_CLIENT_SECRET", "")
            self.tenant_id = tenant_id or os.getenv("SHAREPOINT_TENANT_ID", "")
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
                # base_path = "Documentos/PROYECTOS/Año 2024/..." (opcional)
                # ruta_sharepoint = "01SEP - 30SEP/01 OBLIGACIONES GENERALES/archivo.pdf"
                
                # Construir: /sites/OPERACIONES/[base_path]/01SEP - 30SEP/...
                path_parts = sitio_path_parts.copy()
                
                # Agregar base_path si está configurado (dividir en partes)
                if self.base_path:
                    # Normalizar base_path (eliminar barras iniciales/finales)
                    base_path_clean = self.base_path.strip('/').strip()
                    if base_path_clean:
                        # Dividir base_path en partes y agregar cada una
                        base_path_parts = [p for p in base_path_clean.split('/') if p]
                        path_parts.extend(base_path_parts)
                
                # Agregar la ruta del archivo
                ruta_archivo_clean = ruta_sharepoint.lstrip('/')
                server_relative_url = '/' + '/'.join(path_parts) + '/' + ruta_archivo_clean
                print(f"[DEBUG] SharePoint - Ruta relativa del servidor construida: {server_relative_url}")
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
                resultado = self._descargar_con_office365(server_relative_url, archivo_destino)
                if resultado:
                    return resultado
                # Si Office365 falla, intentar con requests como fallback
                print(f"[INFO] Office365 falló, intentando método alternativo con requests...")
            
            # Método 2: Usar requests con autenticación OAuth
            # Usar server_relative_url para construir la URL de API REST
            # No usar url_archivo porque puede tener la ruta duplicada
            print(f"[DEBUG] Intentando descargar con requests usando server_relative_url: {server_relative_url}")
            return self._descargar_con_requests(server_relative_url, archivo_destino)
            
        except Exception as e:
            print(f"[WARNING] Error al descargar archivo desde SharePoint: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _descargar_con_office365(self, server_relative_url: str, archivo_destino: Path) -> Optional[Path]:
        """Descarga usando Office365-REST-Python-Client"""
        try:
            print(f"[DEBUG] Intentando descargar con Office365: {server_relative_url}")
            # Obtener archivo usando ruta relativa del servidor
            file = self.ctx.web.get_file_by_server_relative_url(server_relative_url)
            self.ctx.load(file)
            self.ctx.execute_query()
            
            # Descargar contenido
            with open(archivo_destino, "wb") as f:
                file.download(f)
                self.ctx.execute_query()
            
            print(f"[INFO] Archivo descargado exitosamente con Office365: {archivo_destino}")
            return archivo_destino
        except Exception as e:
            error_msg = str(e)
            print(f"[WARNING] Error con Office365: {error_msg}")
            
            # Si es error 403, podría ser problema de permisos o ruta incorrecta
            if "403" in error_msg or "Forbidden" in error_msg:
                print(f"[INFO] Error 403 Forbidden - Posibles causas:")
                print(f"  1. La App Registration no tiene permisos suficientes")
                print(f"  2. La ruta del archivo no es correcta: {server_relative_url}")
                print(f"  3. El archivo no existe en esa ubicación")
                print(f"[INFO] Intentando método alternativo con requests...")
            
            return None
    
    def _descargar_con_requests(self, server_relative_url: str, archivo_destino: Path) -> Optional[Path]:
        """Descarga usando requests (método alternativo)"""
        try:
            # Obtener token OAuth con App Registration
            if not self.client_id or not self.client_secret:
                print("[WARNING] SHAREPOINT_CLIENT_ID y SHAREPOINT_CLIENT_SECRET son requeridos")
                return None
            
            # Intentar primero con SharePoint REST API
            token = self._obtener_token_oauth(usar_microsoft_graph=False)
            if not token:
                print("[WARNING] No se pudo obtener token OAuth para SharePoint")
                return None
            
            # Construir URL de API REST usando server_relative_url
            from urllib.parse import quote
            # Asegurar que server_relative_url comience con /
            if not server_relative_url.startswith('/'):
                server_relative_url = '/' + server_relative_url
            
            # Construir URL de API REST
            api_url = f"{self.site_url.rstrip('/')}/_api/web/GetFileByServerRelativeUrl('{quote(server_relative_url, safe='')}')/$value"
            
            print(f"[DEBUG] Descargando desde SharePoint REST API: {api_url}")
            
            # Headers con token OAuth
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/octet-stream",
            }
            
            # Descargar archivo
            response = requests.get(api_url, headers=headers, stream=True)
            
            # Si obtenemos "Unsupported app only token", intentar con Microsoft Graph API
            if response.status_code == 401:
                error_text = response.text
                if "Unsupported app only token" in error_text or "app only" in error_text.lower():
                    print(f"[INFO] SharePoint REST API no acepta tokens de aplicación, intentando con Microsoft Graph API...")
                    return self._descargar_con_microsoft_graph(server_relative_url, archivo_destino)
                
                print(f"[ERROR] 401 Unauthorized - El token OAuth no tiene permisos suficientes")
                print(f"[INFO] Ruta intentada: {server_relative_url}")
                print(f"[INFO] Verifica:")
                print(f"  1. Que la App Registration tenga permisos de SharePoint (no solo Microsoft Graph)")
                print(f"  2. En Azure Portal > App registrations > API permissions:")
                print(f"     - Agregar permisos de 'SharePoint' (no Microsoft Graph)")
                print(f"     - Seleccionar 'Application permissions'")
                print(f"     - Agregar: Sites.Read.All o Sites.ReadWrite.All")
                print(f"     - Dar 'Grant admin consent'")
                print(f"  3. Esperar unos minutos después de otorgar permisos para que se propaguen")
                # Intentar obtener detalles del error
                try:
                    error_detail = response.text[:500]
                    print(f"[DEBUG] Detalle del error 401: {error_detail}")
                except:
                    pass
                return None
            elif response.status_code == 403:
                print(f"[ERROR] 403 Forbidden - La App Registration no tiene permisos o la ruta es incorrecta")
                print(f"[INFO] Ruta intentada: {server_relative_url}")
                print(f"[INFO] Verifica:")
                print(f"  1. Que la App Registration tenga permisos de lectura en SharePoint")
                print(f"  2. Que la ruta del archivo sea correcta")
                print(f"  3. Que el archivo exista en esa ubicación")
                return None
            
            response.raise_for_status()
            
            # Guardar archivo
            with open(archivo_destino, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"[INFO] Archivo descargado exitosamente con SharePoint REST API: {archivo_destino}")
            return archivo_destino
            
        except Exception as e:
            print(f"[WARNING] Error con requests: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _descargar_con_microsoft_graph(self, server_relative_url: str, archivo_destino: Path) -> Optional[Path]:
        """
        Descarga archivo usando Microsoft Graph API (cuando SharePoint REST API no acepta app-only tokens)
        
        Args:
            server_relative_url: Ruta relativa del servidor (ej: /sites/OPERACIONES/Shared Documents/...)
            archivo_destino: Ruta donde guardar el archivo
        
        Returns:
            Path al archivo descargado o None si falla
        """
        try:
            # Obtener token OAuth para Microsoft Graph
            token = self._obtener_token_oauth(usar_microsoft_graph=True)
            if not token:
                print("[WARNING] No se pudo obtener token OAuth para Microsoft Graph")
                return None
            
            # Microsoft Graph API requiere un proceso de 3 pasos:
            # 1. Obtener el site-id usando el hostname y la ruta del sitio
            # 2. Obtener el drive-id del sitio
            # 3. Obtener el archivo usando el site-id, drive-id y la ruta del archivo
            
            parsed = urlparse(self.site_url)
            hostname = parsed.netloc  # ej: verytelcsp.sharepoint.com
            
            # Headers con token OAuth
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            }
            
            # Paso 1: Obtener el site-id
            # server_relative_url: /sites/OPERACIONES/Shared Documents/...
            # Necesitamos solo la parte del sitio: /sites/OPERACIONES
            site_path = server_relative_url.split('/Shared Documents')[0] if '/Shared Documents' in server_relative_url else server_relative_url.split('/')[0:3]
            if isinstance(site_path, list):
                site_path = '/' + '/'.join(site_path)
            site_path = site_path.lstrip('/')
            
            from urllib.parse import quote
            site_url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/{quote(site_path, safe='')}"
            print(f"[DEBUG] Obteniendo site-id desde: {site_url}")
            
            site_response = requests.get(site_url, headers=headers)
            if site_response.status_code != 200:
                print(f"[ERROR] No se pudo obtener site-id (status {site_response.status_code})")
                try:
                    error_detail = site_response.json()
                    print(f"[DEBUG] Detalle del error: {error_detail}")
                except:
                    print(f"[DEBUG] Respuesta: {site_response.text[:500]}")
                return None
            
            site_data = site_response.json()
            site_id = site_data.get('id')
            if not site_id:
                print(f"[ERROR] No se encontró site-id en la respuesta")
                return None
            
            print(f"[DEBUG] Site ID obtenido: {site_id}")
            
            # Paso 2: Obtener el drive-id (el drive de "Shared Documents")
            drives_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
            print(f"[DEBUG] Obteniendo drive-id desde: {drives_url}")
            
            drives_response = requests.get(drives_url, headers=headers)
            if drives_response.status_code != 200:
                print(f"[ERROR] No se pudo obtener drive-id (status {drives_response.status_code})")
                return None
            
            drives_data = drives_response.json()
            drives = drives_data.get('value', [])
            if not drives:
                print(f"[ERROR] No se encontraron drives en el sitio")
                return None
            
            # Buscar el drive de "Shared Documents" o usar el primero
            drive_id = None
            for drive in drives:
                if drive.get('name') == 'Documents' or 'Shared Documents' in drive.get('name', ''):
                    drive_id = drive.get('id')
                    break
            
            if not drive_id:
                drive_id = drives[0].get('id')  # Usar el primer drive si no encontramos "Shared Documents"
            
            print(f"[DEBUG] Drive ID obtenido: {drive_id}")
            
            # Paso 3: Obtener el archivo
            # Extraer la ruta del archivo relativa al drive
            # server_relative_url: /sites/OPERACIONES/Shared Documents/PROYECTOS/...
            # Necesitamos: PROYECTOS/... (sin /sites/OPERACIONES/Shared Documents/)
            if '/Shared Documents' in server_relative_url:
                file_path = server_relative_url.split('/Shared Documents/', 1)[1]
            elif '/Documents' in server_relative_url:
                file_path = server_relative_url.split('/Documents/', 1)[1]
            else:
                # Si no encontramos "Shared Documents", intentar extraer después de /sites/OPERACIONES/
                parts = server_relative_url.split('/')
                if len(parts) >= 4:
                    file_path = '/'.join(parts[3:])  # Después de /sites/OPERACIONES/
                else:
                    file_path = server_relative_url.lstrip('/')
            
            file_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{quote(file_path, safe='')}:/content"
            print(f"[DEBUG] Descargando archivo desde: {file_url}")
            
            # Cambiar Accept header para descargar el contenido binario
            headers['Accept'] = "application/octet-stream"
            response = requests.get(file_url, headers=headers, stream=True)
            
            if response.status_code == 401:
                print(f"[ERROR] 401 Unauthorized - El token OAuth no tiene permisos para Microsoft Graph")
                print(f"[INFO] Verifica que la App Registration tenga permisos de Microsoft Graph:")
                print(f"  - Sites.Read.All o Sites.ReadWrite.All")
                print(f"  - Files.Read.All o Files.ReadWrite.All")
                return None
            elif response.status_code == 404:
                print(f"[ERROR] 404 Not Found - El archivo no existe en la ruta especificada")
                print(f"[INFO] Ruta intentada: {file_path}")
                print(f"[INFO] URL completa: {file_url}")
                return None
            
            response.raise_for_status()
            
            # Guardar archivo
            with open(archivo_destino, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"[INFO] Archivo descargado exitosamente con Microsoft Graph API: {archivo_destino}")
            return archivo_destino
            
        except Exception as e:
            print(f"[WARNING] Error con Microsoft Graph API: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _obtener_token_oauth(self, usar_microsoft_graph: bool = False) -> Optional[str]:
        """
        Obtiene token OAuth para SharePoint o Microsoft Graph usando Client ID y Client Secret
        
        Args:
            usar_microsoft_graph: Si True, usa Microsoft Graph API (para permisos de Microsoft Graph)
                                 Si False, usa SharePoint REST API (para permisos de SharePoint)
        
        Returns:
            Token de acceso OAuth o None si falla
        """
        if not self.client_id or not self.client_secret:
            return None
        
        try:
            # Determinar el tenant a usar para OAuth
            # Prioridad: 1) Tenant ID (GUID), 2) Extraer del dominio
            if self.tenant_id:
                # Usar Tenant ID directamente (más confiable para permisos de aplicación)
                tenant = self.tenant_id
                print(f"[DEBUG] Usando Tenant ID configurado: {tenant[:8]}...")
            else:
                # Extraer tenant del dominio como fallback
                # Formato: https://{tenant}.sharepoint.com/sites/...
                parsed = urlparse(self.site_url)
                domain = parsed.netloc  # ej: verytelcsp.sharepoint.com
                tenant = domain.split('.')[0]  # ej: verytelcsp
                print(f"[DEBUG] Tenant extraído del dominio: {tenant}")
            
            # Para permisos de aplicación, usar el tenant específico
            token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
            
            # Determinar el scope según el tipo de API
            if usar_microsoft_graph:
                # Para Microsoft Graph API con permisos de aplicación
                scope = "https://graph.microsoft.com/.default"
                print(f"[DEBUG] Usando Microsoft Graph API (scope: {scope})")
            else:
                # Para SharePoint REST API con permisos de aplicación
                # NOTA: Si usamos Tenant ID, necesitamos el dominio del sitio para el scope
                if self.tenant_id:
                    # Si tenemos Tenant ID, extraer el dominio del site_url para el scope
                    parsed = urlparse(self.site_url)
                    domain = parsed.netloc  # ej: verytelcsp.sharepoint.com
                    scope = f"https://{domain}/.default"
                else:
                    # Si no hay Tenant ID, usar el tenant extraído
                    scope = f"https://{tenant}.sharepoint.com/.default"
                print(f"[DEBUG] Usando SharePoint REST API (scope: {scope})")
            
            # Datos para la solicitud con permisos de aplicación (client_credentials)
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": scope,
                "grant_type": "client_credentials"
            }
            
            print(f"[DEBUG] Intentando obtener token OAuth")
            print(f"[DEBUG] Tenant: {tenant}")
            print(f"[DEBUG] Scope: {scope}")
            print(f"[DEBUG] Token URL: {token_url}")
            print(f"[DEBUG] Grant type: client_credentials (permisos de aplicación)")
            
            # Realizar solicitud
            print(f"[DEBUG] Realizando solicitud OAuth...")
            response = requests.post(token_url, data=data)
            
            if response.status_code != 200:
                print(f"[ERROR] Error al obtener token OAuth: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"[ERROR] Detalle del error: {error_detail}")
                    # Mostrar información útil del error
                    if 'error_description' in error_detail:
                        print(f"[ERROR] Descripción: {error_detail['error_description']}")
                    if 'error' in error_detail:
                        print(f"[ERROR] Tipo de error: {error_detail['error']}")
                except:
                    print(f"[ERROR] Respuesta: {response.text[:500]}")
                
                print(f"[DEBUG] Información de la solicitud:")
                print(f"  - Tenant: {tenant}")
                print(f"  - Scope: {scope}")
                print(f"  - Token URL: {token_url}")
                print(f"  - Grant type: client_credentials")
                print(f"  - Client ID: {self.client_id[:20]}...")
                
                return None
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            if access_token:
                print(f"[INFO] Token OAuth obtenido exitosamente")
                print(f"[DEBUG] Token expira en: {token_data.get('expires_in', 'N/A')} segundos")
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


