"""
Script de prueba para diagnosticar problemas con MongoDB
"""
import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import json

# Cargar variables de entorno
load_dotenv()

# Configuración - Usar las variables específicas del .env
MONGO_URI = os.getenv("MONGODB_URI", "")
MONGO_DB = os.getenv("MONGODB_DB_NAME", "")

# JSON de prueba
json_prueba = {
    "anio": 2025,
    "mes": 9,
    "seccion": 1,
    "subseccion": "1.5.1",
    "obligaciones_generales": [
        {
            "item": 1,
            "obligacion": "Obligación de prueba",
            "periodicidad": "Permanente",
            "cumplio": "Cumplió",
            "observaciones": "Esta es una observación de prueba",
            "anexo": "test/anexo.pdf"
        }
    ],
    "user_created": 1,
    "user_updated": 1,
    "created_at": datetime.now(),
    "updated_at": datetime.now()
}


async def test_mongodb_connection():
    """Prueba la conexión a MongoDB"""
    print("=" * 80)
    print("PRUEBA DE CONEXIÓN A MONGODB")
    print("=" * 80)
    
    # Verificar variables de entorno
    print(f"\n1. Verificando variables de entorno:")
    print(f"   MONGODB_URI: {'✅ Configurado' if MONGO_URI else '❌ NO configurado'}")
    if MONGO_URI:
        # Ocultar credenciales en la URI
        uri_oculta = MONGO_URI.split('@')[-1] if '@' in MONGO_URI else MONGO_URI
        print(f"   URI: mongodb://...@{uri_oculta}")
    print(f"   MONGODB_DB_NAME: {'✅ Configurado' if MONGO_DB else '❌ NO configurado'}")
    if MONGO_DB:
        print(f"   Base de datos: {MONGO_DB}")
    
    if not MONGO_URI or not MONGO_DB:
        print("\n❌ ERROR: MONGODB_URI y MONGODB_DB_NAME deben estar configurados en .env")
        print("\nAgrega estas líneas a tu archivo .env:")
        print("MONGODB_URI=mongodb://localhost:27017")
        print("MONGODB_DB_NAME=nombre_base_datos")
        return False
    
    # Intentar conectar
    print(f"\n2. Intentando conectar a MongoDB...")
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        # Probar conexión con ping
        await client.admin.command('ping')
        print("   ✅ Conexión exitosa a MongoDB")
    except Exception as e:
        print(f"   ❌ Error al conectar: {e}")
        print("\nPosibles causas:")
        print("   - MongoDB no está corriendo")
        print("   - La URI es incorrecta")
        print("   - Problemas de red/firewall")
        return False
    
    # Obtener base de datos
    print(f"\n3. Accediendo a la base de datos '{MONGO_DB}'...")
    try:
        db = client[MONGO_DB]
        # Listar colecciones existentes
        colecciones = await db.list_collection_names()
        print(f"   ✅ Base de datos accesible")
        print(f"   Colecciones existentes: {colecciones if colecciones else 'Ninguna'}")
    except Exception as e:
        print(f"   ❌ Error al acceder a la base de datos: {e}")
        return False
    
    # Intentar guardar documento de prueba
    print(f"\n4. Intentando guardar documento de prueba...")
    try:
        collection = db["obligaciones"]
        
        # Construir filtro
        filtro = {
            "anio": json_prueba["anio"],
            "mes": json_prueba["mes"],
            "seccion": json_prueba["seccion"],
            "subseccion": json_prueba["subseccion"]
        }
        
        # Preparar documento (convertir datetime a formato compatible)
        documento = json_prueba.copy()
        documento["created_at"] = datetime.now()
        documento["updated_at"] = datetime.now()
        
        # Intentar upsert
        resultado = await collection.update_one(
            filtro,
            {"$set": documento},
            upsert=True
        )
        
        if resultado.upserted_id:
            print(f"   ✅ Documento creado exitosamente")
            print(f"   ID del documento: {resultado.upserted_id}")
        else:
            print(f"   ✅ Documento actualizado exitosamente")
            print(f"   Documentos modificados: {resultado.modified_count}")
        
        # Verificar que se guardó correctamente
        documento_guardado = await collection.find_one(filtro)
        if documento_guardado:
            print(f"\n5. Verificando documento guardado...")
            print(f"   ✅ Documento encontrado en MongoDB")
            print(f"   ID: {documento_guardado['_id']}")
            print(f"   Año: {documento_guardado['anio']}")
            print(f"   Mes: {documento_guardado['mes']}")
            print(f"   Sección: {documento_guardado['seccion']}")
            print(f"   Subsección: {documento_guardado['subseccion']}")
            print(f"   Obligaciones: {len(documento_guardado.get('obligaciones_generales', []))}")
        else:
            print(f"   ⚠️ Documento no encontrado después de guardar")
        
        # Mostrar JSON guardado
        print(f"\n6. JSON guardado en MongoDB:")
        print(json.dumps({
            "anio": documento_guardado["anio"],
            "mes": documento_guardado["mes"],
            "seccion": documento_guardado["seccion"],
            "subseccion": documento_guardado["subseccion"],
            "obligaciones_count": len(documento_guardado.get("obligaciones_generales", []))
        }, indent=2, ensure_ascii=False))
        
        print("\n" + "=" * 80)
        print("✅ PRUEBA EXITOSA: MongoDB está funcionando correctamente")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error al guardar documento: {e}")
        import traceback
        print("\nDetalles del error:")
        traceback.print_exc()
        return False
    finally:
        client.close()


if __name__ == "__main__":
    print("\n")
    resultado = asyncio.run(test_mongodb_connection())
    if not resultado:
        print("\n" + "=" * 80)
        print("❌ PRUEBA FALLIDA: Revisa los errores arriba")
        print("=" * 80)
        print("\nSugerencias:")
        print("1. Verifica que MongoDB esté corriendo")
        print("2. Verifica las variables MONGO_URI y MONGO_DB en .env")
        print("3. Verifica que la URI sea correcta")
        print("4. Si usas MongoDB Atlas, verifica que tu IP esté en la whitelist")

