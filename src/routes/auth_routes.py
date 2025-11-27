"""
Rutas de autenticación
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field, model_validator

from ..controllers.auth_controller import AuthController
from ..middleware.auth_middleware import auth_middleware, get_current_user
from ..services.database import get_database

router = APIRouter(prefix="/auth", tags=["Autenticación"])

auth_controller = AuthController()


class LoginRequest(BaseModel):
    """Esquema para request de login"""
   
    username: Optional[str] = Field(None, description="Username del usuario")
    password: str = Field(..., description="Contraseña del usuario")
    
    @model_validator(mode='after')
    def validate_or_username(self):
        """Valida que se proporcione email o username"""
        if not self.username:
            raise ValueError('Debe proporcionar email o username')
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "username": "usuario@example.com",
                "password": "password123"
            }
        }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    
    """
    Inicia sesión con email/username y contraseña
    
    - **email** o **username**: Email o nombre de usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT y los datos del usuario.
    """
    login_data = {
        "username": credentials.username,
        "password": credentials.password
    }
    return await auth_controller.login(login_data, db)
   


@router.get("/verify", status_code=status.HTTP_200_OK)
async def verify_token(
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Verifica si el token JWT es válido
    
    Requiere autenticación mediante Bearer token.
    Retorna los datos del usuario si el token es válido.
    """
    return await auth_controller.verify_token(token_payload, db)


@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_profile(
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Obtiene el perfil del usuario autenticado
    
    Requiere autenticación mediante Bearer token.
    Retorna los datos completos del perfil del usuario.
    """
    user_id = token_payload.get("user_id")
    return await auth_controller.get_profile(user_id, db)

