"""
Modelo de Rol de Acceso
Define los permisos de acceso a módulos específicos del sistema
"""
from typing import Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, Field
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


class AccessRole(BaseModel):
    """Modelo de Rol de Acceso"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., description="Nombre del rol (ej: superadmin, admin_info_general)")
    description: str = Field(..., description="Descripción del rol")
    module: Optional[str] = Field(None, description="Módulo asociado (si aplica)")
    permission_level: str = Field(..., description="Nivel de permiso: superadmin, admin, readonly")
    external_role_id: Optional[Union[str, int]] = Field(None, description="ID del rol en el sistema externo para mapeo")
    is_active: bool = Field(default=True, description="Indica si el rol está activo")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "admin_info_general",
                "description": "Administrador del módulo de Información General",
                "module": "info_general",
                "permission_level": "admin",
                "is_active": True
            }
        }


class AccessRoleCreate(BaseModel):
    """Esquema para crear un rol de acceso"""
    name: str
    description: str
    module: Optional[str] = None
    permission_level: str
    is_active: bool = True


class AccessRoleResponse(BaseModel):
    """Esquema de respuesta para rol de acceso"""
    id: str
    name: str
    description: str
    module: Optional[str]
    permission_level: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {ObjectId: str}



