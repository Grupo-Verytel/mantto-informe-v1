"""
Servicio para integración con API externa de autenticación
"""
import os
import requests
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class ExternalAuthService:
    """Servicio para comunicarse con la API externa de autenticación"""
    
    def __init__(self):
        self.api_url = os.getenv("EXTERNAL_AUTH_API_URL", "http://localhost:4000")
        self.timeout = int(os.getenv("EXTERNAL_AUTH_API_TIMEOUT", "10"))
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Autentica un usuario contra la API externa
        
        Args:
            username: Username o email del usuario
            password: Contraseña del usuario
            
        Returns:
            Dict con información del usuario y token JWT de la API externa
            
        Raises:
            HTTPException: Si las credenciales son inválidas o hay error en la API
        """
        try:
            url = f"{self.api_url}/api/auth/login"
            payload = {
                "username": username,
                "password": password
            }
            
            logger.info(f"Intentando autenticar usuario: {username}")
            print(url)
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Autenticación exitosa para usuario: {username}")
                return data
            elif response.status_code == 401:
                logger.warning(f"Credenciales inválidas para usuario: {username}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas"
                )
            else:
                logger.error(f"Error en API externa: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Error al comunicarse con el servicio de autenticación"
                )
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout al comunicarse con API externa para usuario: {username}")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="El servicio de autenticación no responde"
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión con API externa: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error al comunicarse con el servicio de autenticación"
            )
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica un token JWT con la API externa
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Dict con información del usuario
            
        Raises:
            HTTPException: Si el token es inválido
        """
        try:
            url = f"{self.api_url}/auth/verify"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido o expirado"
                )
            else:
                logger.error(f"Error al verificar token: {response.status_code}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Error al verificar token con el servicio externo"
                )
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al verificar token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error al comunicarse con el servicio de autenticación"
            )



