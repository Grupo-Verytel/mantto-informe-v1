"""
Middleware de autenticación JWT
"""
from typing import Optional, Callable
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..services.jwt_service import JWTService
from ..services.database import get_database
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


async def auth_middleware(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> dict:
    """
    Middleware que verifica el token JWT en cada petición
    
    ⚠️ AUTENTICACIÓN DESACTIVADA TEMPORALMENTE ⚠️
    Para reactivar, descomentar el código de verificación abajo.
    
    Args:
        request: Request object para verificar el método HTTP
        credentials: Credenciales HTTP Bearer con el token (opcional)
        db: Instancia de la base de datos
        
    Returns:
        Payload del token decodificado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    # ⚠️ AUTENTICACIÓN DESACTIVADA - Retornar payload de prueba
    logger.warning("⚠️ AUTENTICACIÓN DESACTIVADA - Acceso permitido sin token")
    return {
        "email": "test@example.com",
        "user_id": "test_user_id",
        "user": {
            "_id": "test_user_id",
            "email": "test@example.com",
            "is_active": True,
            "access_role_name": "superadmin"
        }
    }
    
    # ============================================================================
    # CÓDIGO DE AUTENTICACIÓN ORIGINAL (COMENTADO)
    # ============================================================================
    # # Permitir solicitudes OPTIONS sin autenticación (preflight)
    # if request.method == "OPTIONS":
    #     return {}
    # 
    # # Si no hay credenciales, lanzar error
    # if not credentials:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Token de autenticación requerido",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # 
    # token = credentials.credentials
    # jwt_service = JWTService()
    # 
    # try:
    #     # Verificar y decodificar token
    #     payload = jwt_service.verify_token(token)
    # 
    #     # Verificar que el usuario existe y está activo
    #     users_collection = db.users
    #     user = await users_collection.find_one({"email": payload.get("email")})
    # 
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Usuario no encontrado",
    #             headers={"WWW-Authenticate": "Bearer"},
    #         )
    # 
    #     if not user.get("is_active", True):
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Usuario inactivo",
    #             headers={"WWW-Authenticate": "Bearer"},
    #         )
    # 
    #     # Agregar información del usuario al payload
    #     payload["user_id"] = str(user["_id"])
    #     payload["user"] = user
    # 
    #     return payload
    #     
    # except HTTPException:
    #     raise
    # except Exception as e:
    #     logger.error(f"Error en auth_middleware: {str(e)}")
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Token inválido",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )


def get_current_user(token_payload: dict = Depends(auth_middleware)) -> dict:
    """
    Dependency que retorna el usuario actual autenticado
    
    Args:
        token_payload: Payload del token (inyectado por auth_middleware)
        
    Returns:
        Dict con información del usuario
    """
    return token_payload.get("user", {})



