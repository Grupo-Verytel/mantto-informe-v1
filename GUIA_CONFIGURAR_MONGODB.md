# GUÍA: Configurar MongoDB

## ✅ Solución Implementada

He actualizado el código para que MongoDB sea **opcional**. Si MongoDB no está configurado:
- ✅ El endpoint funcionará normalmente
- ✅ Las obligaciones se procesarán correctamente
- ✅ Se guardarán en el archivo JSON (si `guardar_json: true`)
- ⚠️ Solo se registrará un warning en los logs (no fallará)

## 📝 Configuración de MongoDB

### Opción 1: MongoDB Local

Si tienes MongoDB instalado localmente:

1. **Asegúrate de que MongoDB esté corriendo:**
   ```bash
   # Verificar si MongoDB está corriendo
   # En Windows, verifica el servicio en "Servicios"
   ```

2. **Agrega estas variables a tu archivo `.env`:**
   ```env
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=informes_etb
   ```

### Opción 2: MongoDB Atlas (Cloud)

Si usas MongoDB Atlas:

1. **Obtén tu connection string desde MongoDB Atlas:**
   - Ve a tu cluster en MongoDB Atlas
   - Click en "Connect"
   - Selecciona "Connect your application"
   - Copia el connection string

2. **Agrega estas variables a tu archivo `.env`:**
   ```env
   MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/?retryWrites=true&w=majority
   MONGO_DB=informes_etb
   ```

   **Nota:** Reemplaza `usuario` y `password` con tus credenciales reales.

### Opción 3: Sin MongoDB (Funcionalidad Limitada)

Si no quieres usar MongoDB por ahora:

- ✅ **No necesitas hacer nada**
- ✅ El sistema funcionará sin MongoDB
- ⚠️ Solo no se guardará en la base de datos (pero sí en JSON)

## 🔍 Verificar Configuración

### 1. Verificar que las variables estén en `.env`:

Abre tu archivo `.env` y verifica que tengas:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB=informes_etb
```

### 2. Verificar que MongoDB esté corriendo:

**Windows:**
```powershell
# Verificar si el servicio está corriendo
Get-Service -Name MongoDB
```

**O prueba conectarte:**
```powershell
# Si tienes mongo shell instalado
mongo --eval "db.version()"
```

### 3. Probar la conexión desde Python:

```python
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    # Probar conexión
    result = await db.command("ping")
    print("✅ Conexión exitosa a MongoDB")
    print(f"Base de datos: {MONGO_DB}")
except Exception as e:
    print(f"❌ Error al conectar: {e}")
```

## 📋 Estructura de la Base de Datos

Cuando MongoDB esté configurado, se creará automáticamente:

- **Base de datos:** La especificada en `MONGO_DB`
- **Colección:** `obligaciones`

### Ejemplo de documento:

```json
{
  "_id": ObjectId("..."),
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "subseccion": "1.5.1",
  "obligaciones_generales": [...],
  "user_created": 1,
  "user_updated": 1,
  "created_at": ISODate("2025-11-28T16:23:58Z"),
  "updated_at": ISODate("2025-11-28T16:23:58Z")
}
```

## 🚀 Después de Configurar

1. **Reinicia el servidor FastAPI:**
   ```bash
   # Detén el servidor (Ctrl+C) y vuelve a iniciarlo
   python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Prueba el endpoint:**
   ```json
   POST http://localhost:8000/api/obligaciones/procesar
   {
     "anio": 2025,
     "mes": 9,
     "seccion": 1,
     "subseccion": "1.5.1",
     "regenerar_todas": false,
     "guardar_json": true
   }
   ```

3. **Verifica los logs:**
   - Si MongoDB está configurado: Verás `"Obligaciones guardadas en MongoDB..."`
   - Si no está configurado: Verás `"MongoDB no está configurado o no está disponible"` (solo warning, no error)

## ⚠️ Solución de Problemas

### Error: "MONGO_URI no está configurado"

**Solución:** Agrega `MONGO_URI` y `MONGO_DB` a tu archivo `.env`

### Error: "Connection refused"

**Solución:** 
- Verifica que MongoDB esté corriendo
- Verifica que el puerto sea correcto (por defecto 27017)
- Verifica que no haya firewall bloqueando la conexión

### Error: "Authentication failed"

**Solución:**
- Verifica las credenciales en `MONGO_URI`
- Si usas MongoDB Atlas, asegúrate de que tu IP esté en la whitelist

### La base de datos no se crea automáticamente

**Solución:** 
- MongoDB crea la base de datos automáticamente cuando insertas el primer documento
- No necesitas crearla manualmente

## 📝 Notas Importantes

1. **MongoDB es opcional:** El sistema funciona sin MongoDB, solo no guardará en la base de datos.

2. **La base de datos se crea automáticamente:** No necesitas crear la base de datos manualmente, se creará cuando se inserte el primer documento.

3. **La colección se crea automáticamente:** La colección `obligaciones` se creará automáticamente cuando se guarde el primer documento.

4. **Upsert:** Si el documento ya existe (mismo año, mes, sección y subsección), se actualizará. Si no existe, se creará.

