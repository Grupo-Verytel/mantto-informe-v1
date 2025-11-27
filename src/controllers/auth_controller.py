"""
Controlador de autenticación
"""
from typing import Dict, Any
from fastapi import HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from bson import ObjectId
import jwt
from ..services.external_auth_service import ExternalAuthService
from ..services.role_mapping_service import RoleMappingService
from ..services.jwt_service import JWTService

from ..services.database import get_database
from ..models.user import User, UserResponse
import logging

logger = logging.getLogger(__name__)


class AuthController:
    """Controlador para manejar la autenticación"""
    
    def __init__(self):
        self.external_auth_service = ExternalAuthService()
        self.jwt_service = JWTService()
    
    async def login(self, credentials: Dict[str, str], db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """
        Inicia sesión con email/username y contraseña
        
        Args:
            credentials: Dict con 'email' o 'username' y 'password'
            db: Instancia de la base de datos
            
        Returns:
            Dict con token JWT y datos del usuario
        """
        email = credentials.get("username")
        password = credentials.get("password")
        
        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email/username y contraseña son requeridos"
            )
        
        try:
            # 1. Autenticar con API externa
            external_auth_result = await self.external_auth_service.login(email, password)
            
            
            
            
            
            
            # 2. Obtener rol del usuario desde la API externa
            token = external_auth_result.get("token") 
            
            payload = jwt.decode(token, options={"verify_signature": False})
            
            
            # 3. Mapear rol externo a rol interno
            role_mapping_service = RoleMappingService(db)
           
            access_role_name = await role_mapping_service.map_external_role_to_access_role(
                payload.get("id_role"), 
                payload.get("username")
            )
            
            if not access_role_name:
                logger.warning(f"No se pudo mapear el rol para usuario: {email}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario no tiene permisos asignados en el sistema"
                )
            
            # # 4. Obtener módulos asignados
            modules = await role_mapping_service.get_user_modules_from_role(access_role_name)
            
            # # 5. Extraer información del usuario del payload
            username = payload.get("username") or email
            user_email = payload.get("email") or email
            user_id = str(payload.get("sub") or payload.get("id") or payload.get("user_id") or "")
            
            # # 6. Preparar respuesta
            user_response = UserResponse(
                id=user_id,
                email=user_email,
                username=username,
                access_role_name=access_role_name,
                modules=modules,
                is_active=True,
                last_login=None
            )
            
            return {
                "success": True,
                "message": "Login exitoso",
                "data": {
                    "token": external_auth_result.get("token"),
                    "user": user_response.model_dump()
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en login: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def verify_token(self, token_payload: Dict[str, Any], db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """
        Verifica un token JWT y retorna información del usuario
        
        Args:
            token_payload: Payload del token JWT decodificado
            db: Instancia de la base de datos
            
        Returns:
            Dict con datos del usuario
        """
        user_id = token_payload.get("sub")
        email = token_payload.get("email")
        
        users_collection = db.users
        user = await users_collection.find_one({"email": email})
        
        if not user or not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo"
            )
        
        user_response = UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            username=user.get("username", ""),
            access_role_name=user.get("access_role_name"),
            modules=user.get("modules", []),
            is_active=user.get("is_active", True),
            last_login=user.get("last_login")
        )
        
        return {
            "success": True,
            "data": user_response.model_dump()
        }
 

