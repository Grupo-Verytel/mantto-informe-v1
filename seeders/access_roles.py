"""
Seeder para roles de acceso
Crea los roles predefinidos del sistema
"""
import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()


# Módulos del sistema según la documentación
MODULES = [
    {
        "name": "info_general",
        "description": "Información General del Contrato",
        "display_name": "Información General del Contrato"
    },
    {
        "name": "mesa_servicio",
        "description": "Informe de Mesa de servicio",
        "display_name": "Informe de Mesa de servicio"
    },
    {
        "name": "ans",
        "description": "Informes de medición de niveles de servicio ANS",
        "display_name": "Informes de medición de niveles de servicio ANS"
    },
    {
        "name": "bienes_servicios",
        "description": "Informe de Bienes y servicios",
        "display_name": "Informe de Bienes y servicios"
    },
    {
        "name": "laboratorio",
        "description": "Informe de laboratorio",
        "display_name": "Informe de laboratorio"
    },
    {
        "name": "visitas",
        "description": "Informe de Visitas Ejecutadas",
        "display_name": "Informe de Visitas Ejecutadas"
    },
    {
        "name": "siniestros",
        "description": "Informe de Siniestros",
        "display_name": "Informe de Siniestros"
    },
    {
        "name": "presupuesto",
        "description": "Ejecución presupuestal",
        "display_name": "Ejecución presupuestal"
    },
    {
        "name": "riesgos",
        "description": "Matriz de riesgos",
        "display_name": "Matriz de riesgos"
    },
    {
        "name": "sgsst",
        "description": "Informe mensual de gestión SGSST",
        "display_name": "Informe mensual de gestión SGSST"
    },
    {
        "name": "valores",
        "description": "Valores públicos",
        "display_name": "Valores públicos"
    },
    {
        "name": "conclusiones",
        "description": "Conclusiones",
        "display_name": "Conclusiones"
    },
    {
        "name": "anexos",
        "description": "Anexos",
        "display_name": "Anexos"
    },
    {
        "name": "control_cambios",
        "description": "Control de Revisiones y Cambios",
        "display_name": "Control de Revisiones y Cambios"
    }
]


async def seed_access_roles():
    """Crea los roles de acceso en la base de datos"""
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "mantto_informe")
    
    client = AsyncIOMotorClient(mongodb_uri)
    db = client[db_name]
    collection = db.access_roles
    
    print("=" * 60)
    print("Seeder: Roles de Acceso")
    print("=" * 60)
    
    # Contador para asignar IDs externos secuenciales
    external_role_id_counter = 1
    
    # 1. Crear rol superadmin
    superadmin_role = {
        "name": "superadmin",
        "description": "Super Administrador - Acceso total a todos los módulos",
        "module": None,
        "permission_level": "superadmin",
        "external_role_id": external_role_id_counter,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await collection.update_one(
        {"name": "superadmin"},
        {"$setOnInsert": superadmin_role},
        upsert=True
    )
    
    if result.upserted_id:
        print(f"[✓] Creado rol: superadmin (external_role_id: {external_role_id_counter})")
    else:
        print(f"[→] Rol ya existe: superadmin (external_role_id: {external_role_id_counter})")
    
    external_role_id_counter += 1
    
    # 2. Crear roles por módulo (admin y readonly para cada módulo)
    roles_created = 0
    roles_existing = 0
    
    for module in MODULES:
        module_name = module["name"]
        
        # Rol admin para el módulo
        admin_role = {
            "name": f"admin_{module_name}",
            "description": f"Administrador del módulo: {module['display_name']}",
            "module": module_name,
            "permission_level": "admin",
            "external_role_id": external_role_id_counter,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await collection.update_one(
            {"name": f"admin_{module_name}"},
            {"$setOnInsert": admin_role},
            upsert=True
        )
        
        if result.upserted_id:
            print(f"[✓] Creado rol: admin_{module_name} (external_role_id: {external_role_id_counter})")
            roles_created += 1
        else:
            print(f"[→] Rol ya existe: admin_{module_name} (external_role_id: {external_role_id_counter})")
            roles_existing += 1
        
        external_role_id_counter += 1
        
        # Rol readonly para el módulo
        readonly_role = {
            "name": f"readonly_{module_name}",
            "description": f"Solo lectura del módulo: {module['display_name']}",
            "module": module_name,
            "permission_level": "readonly",
            "external_role_id": external_role_id_counter,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await collection.update_one(
            {"name": f"readonly_{module_name}"},
            {"$setOnInsert": readonly_role},
            upsert=True
        )
        
        if result.upserted_id:
            print(f"[✓] Creado rol: readonly_{module_name} (external_role_id: {external_role_id_counter})")
            roles_created += 1
        else:
            print(f"[→] Rol ya existe: readonly_{module_name} (external_role_id: {external_role_id_counter})")
            roles_existing += 1
        
        external_role_id_counter += 1
    
    print("=" * 60)
    print(f"[OK] Proceso completado")
    print(f"   Roles creados: {roles_created}")
    print(f"   Roles existentes: {roles_existing}")
    print(f"   Total de roles: {1 + (len(MODULES) * 2)}")  # 1 superadmin + (14 módulos * 2 roles)
    print("=" * 60)
    
    client.close()


if __name__ == "__main__":
    asyncio.run(seed_access_roles())



