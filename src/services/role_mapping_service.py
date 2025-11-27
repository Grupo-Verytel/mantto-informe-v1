"""
Servicio para mapear roles de la API externa a roles internos del sistema
"""
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class RoleMappingService:
    """Servicio para mapear y homologar roles entre sistemas"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.access_roles_collection = db.access_roles
    
    async def map_external_role_to_access_role(
        self, 
        external_role_id: Any, 
        external_user_data: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Mapea el ID de rol devuelto por la API externa al rol de acceso interno
        
        Args:
            external_role_id: ID del rol devuelto por la API externa (puede ser int, str, etc.)
            external_user_data: Datos adicionales del usuario de la API externa (opcional)
            
        Returns:
            Nombre del rol de acceso interno o None si no se encuentra mapeo
        """
        if external_role_id is None:
            logger.warning("ID de rol externo es None")
            return None
        
        # Convertir el ID a string para búsqueda consistente
        external_role_id_str = str(external_role_id)
        
        # 1. Buscar rol por external_role_id (campo que almacena el ID del sistema externo)
        role = await self.access_roles_collection.find_one({"external_role_id": external_role_id_str})
        if role:
            logger.info(f"Rol encontrado por external_role_id: {external_role_id_str} -> {role['name']}")
            return role["name"]
        
        # 2. Buscar también por external_role_id como número (por si se guardó como int)
        try:
            external_role_id_int = int(external_role_id)
            role = await self.access_roles_collection.find_one({"external_role_id": external_role_id_int})
            if role:
                logger.info(f"Rol encontrado por external_role_id (int): {external_role_id_int} -> {role['name']}")
                return role["name"]
        except (ValueError, TypeError):
            pass
        
        # 3. Fallback: buscar por nombre si external_role_id es un string que parece un nombre
        if isinstance(external_role_id, str):
            role = await self.access_roles_collection.find_one({"name": external_role_id})
            if role:
                logger.info(f"Rol encontrado por nombre (fallback): {external_role_id} -> {role['name']}")
                return role["name"]
        
        # 4. Mapeo por defecto (puede ser configurado en base de datos o archivo de configuración)
        default_mapping = {
            "admin": "superadmin",
            "user": "readonly_info_general",
        }
        
        if isinstance(external_role_id, str):
            mapped_role = default_mapping.get(external_role_id.lower())
            if mapped_role:
                # Verificar que el rol mapeado existe
                role = await self.access_roles_collection.find_one({"name": mapped_role})
                if role:
                    logger.info(f"Rol mapeado por defecto: {external_role_id} -> {mapped_role}")
                    return mapped_role
        
        logger.warning(f"No se encontró mapeo para rol externo ID: {external_role_id}")
        return None
    
    async def get_user_modules_from_role(self, access_role_name: str) -> list:
        """
        Obtiene los módulos asignados a un rol de acceso
        
        Args:
            access_role_name: Nombre del rol de acceso
            
        Returns:
            Lista de módulos asignados
        """
        if access_role_name == "superadmin":
            # Superadmin tiene acceso a todos los módulos
            return [
                "info_general",
                "mesa_servicio",
                "ans",
                "bienes_servicios",
                "laboratorio",
                "visitas",
                "siniestros",
                "presupuesto",
                "riesgos",
                "sgsst",
                "valores",
                "conclusiones",
                "anexos",
                "control_cambios"
            ]
        
        # Extraer módulo del nombre del rol (ej: admin_info_general -> info_general)
        if "_" in access_role_name:
            parts = access_role_name.split("_", 1)
            if len(parts) > 1:
                module = parts[1]
                # Mapear nombres de módulos
                module_mapping = {
                    "info_general": "info_general",
                    "mesa_servicio": "mesa_servicio",
                    "ans": "ans",
                    "bienes": "bienes_servicios",
                    "laboratorio": "laboratorio",
                    "visitas": "visitas",
                    "siniestros": "siniestros",
                    "presupuesto": "presupuesto",
                    "riesgos": "riesgos",
                    "sgsst": "sgsst",
                    "valores": "valores",
                    "conclusiones": "conclusiones",
                    "anexos": "anexos",
                    "control_cambios": "control_cambios"
                }
                mapped_module = module_mapping.get(module, module)
                return [mapped_module] if mapped_module else []
        
        return []



