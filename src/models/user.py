"""
Modelo de Usuario
Nota: Los usuarios se validan contra una API externa, pero almacenamos
la información de roles localmente en MongoDB
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Wrapper para ObjectId de MongoDB compatible con Pydantic v2"""
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            )
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")


class User(BaseModel):
    """Modelo de Usuario"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(..., description="Email del usuario")
    username: str = Field(..., description="Username del usuario")
    access_role_id: Optional[PyObjectId] = Field(None, description="ID del rol de acceso")
    access_role_name: Optional[str] = Field(None, description="Nombre del rol de acceso")
    modules: Optional[List[str]] = Field(default=[], description="Lista de módulos asignados")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")
    external_user_id: Optional[str] = Field(None, description="ID del usuario en el sistema externo")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(None, description="Última vez que inició sesión")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "username": "usuario",
                "access_role_name": "admin_info_general",
                "modules": ["info_general"],
                "is_active": True
            }
        }


class UserResponse(BaseModel):
    """Esquema de respuesta para usuario (sin información sensible)"""
    id: Optional[str] = Field(default="", description="ID del usuario")
    email: Optional[str] = Field(default="", description="Email del usuario")
    username: str = Field(..., description="Username del usuario")
    access_role_name: Optional[str] = Field(None, description="Nombre del rol de acceso")
    modules: List[str] = Field(default=[], description="Lista de módulos asignados")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")
    last_login: Optional[datetime] = Field(None, description="Última vez que inició sesión")

    class Config:
        json_encoders = {ObjectId: str}



