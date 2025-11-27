"""
Script para ejecutar todos los seeders
"""
import asyncio
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from seeders.access_roles import seed_access_roles


async def run_all_seeders():
    """Ejecuta todos los seeders en orden"""
    print("\n" + "=" * 60)
    print("EJECUTANDO SEEDERS")
    print("=" * 60 + "\n")
    
    # Ejecutar seeders
    await seed_access_roles()
    
    print("\n" + "=" * 60)
    print("[OK] Todos los seeders completados")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all_seeders())

