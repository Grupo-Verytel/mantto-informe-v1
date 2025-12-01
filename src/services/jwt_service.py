"""
Servicio para manejo de tokens JWT
"""
import jwt
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import logging

import config

logger = logging.getLogger(__name__)


class JWTService:
    """Servicio para generar y validar tokens JWT"""
    
    def __init__(self):
        # Obtener configuración desde config.py
        self.secret_key = config.JWT_SECRET
        self.algorithm = config.JWT_ALGORITHM
        self.token_expiration = config.JWT_EXPIRES_IN_HOURS
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica y decodifica un token JWT
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Dict con el payload del token decodificado
            
        Raises:
            HTTPException: Si el token es inválido, expirado o tiene errores
        """
        try:
            # Decodificar y verificar el token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_signature": True, "verify_exp": True}
            )
            
            logger.debug(f"Token verificado exitosamente para usuario: {payload.get('email') or payload.get('username')}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token JWT expirado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token JWT inválido: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error(f"Error al verificar token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Error al verificar token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def decode_token_without_verification(self, token: str) -> Dict[str, Any]:
        """
        Decodifica un token JWT sin verificar la firma
        Útil para obtener información del token sin validar
        
        Args:
            token: Token JWT a decodificar
            
        Returns:
            Dict con el payload del token
            
        Raises:
            HTTPException: Si el token no puede ser decodificado
        """
        try:
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            return payload
        except Exception as e:
            logger.error(f"Error al decodificar token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token no válido"
            )
    
    def generate_token(self, payload: Dict[str, Any], expiration_hours: Optional[int] = None) -> str:
        """
        Genera un nuevo token JWT
        
        Args:
            payload: Datos a incluir en el token
            expiration_hours: Horas hasta la expiración (usa default si no se especifica)
            
        Returns:
            Token JWT como string
        """
        expiration = expiration_hours or self.token_expiration
        
        # Agregar tiempo de expiración
        exp = datetime.utcnow() + timedelta(hours=expiration)
        payload["exp"] = exp
        payload["iat"] = datetime.utcnow()
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token



