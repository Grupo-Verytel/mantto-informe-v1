# INSTRUCCIONES: EJECUTAR LA API PARA POSTMAN

## 🚀 Iniciar el Servidor

### Opción 1: Ejecutar directamente con Python

```bash
python app.py
```

### Opción 2: Ejecutar con uvicorn (Recomendado)

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Opción 3: Ejecutar en segundo plano (Windows PowerShell)

```powershell
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
```

### Opción 4: Ejecutar en segundo plano (Linux/Mac)

```bash
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
```

## 📍 URL Base

Una vez iniciado, la API estará disponible en:

- **URL Base:** `http://localhost:8000`
- **Documentación Swagger:** `http://localhost:8000/docs`
- **Documentación ReDoc:** `http://localhost:8000/redoc`

## 🔧 Configuración de Puerto

Puedes cambiar el puerto usando variables de entorno:

**Windows PowerShell:**
```powershell
$env:API_PORT="3000"
python app.py
```

**Windows CMD:**
```cmd
set API_PORT=3000
python app.py
```

**Linux/Mac:**
```bash
export API_PORT=3000
python app.py
```

O crear/editar archivo `.env`:
```env
API_PORT=8000
API_HOST=0.0.0.0
DEBUG=true
```

## 📡 Endpoints Disponibles

### 1. Procesar Obligaciones

**POST** `http://localhost:8000/api/obligaciones/procesar`

**Body (JSON):**
```json
{
  "anio": 2025,
  "mes": 9,
  "regenerar_todas": false,
  "guardar_json": true
}
```

**Ejemplo en Postman:**
1. Método: `POST`
2. URL: `http://localhost:8000/api/obligaciones/procesar`
3. Headers:
   - `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "anio": 2025,
     "mes": 9,
     "regenerar_todas": false,
     "guardar_json": true
   }
   ```

### 2. Health Check

**GET** `http://localhost:8000/health`

### 3. Root

**GET** `http://localhost:8000/`

## 🧪 Probar en Postman

### Paso 1: Verificar que el servidor esté corriendo

1. Abre Postman
2. Crea una nueva petición GET
3. URL: `http://localhost:8000/health`
4. Envía la petición
5. Deberías recibir: `{"status": "healthy", "service": "informes-api"}`

### Paso 2: Procesar Obligaciones

1. Crea una nueva petición POST
2. URL: `http://localhost:8000/api/obligaciones/procesar`
3. En la pestaña "Headers", agrega:
   - Key: `Content-Type`
   - Value: `application/json`
4. En la pestaña "Body":
   - Selecciona "raw"
   - Selecciona "JSON" en el dropdown
   - Pega el siguiente JSON:
   ```json
   {
     "anio": 2025,
     "mes": 9,
     "regenerar_todas": false,
     "guardar_json": true
   }
   ```
5. Envía la petición

### Respuesta Esperada

```json
{
  "success": true,
  "message": "Obligaciones procesadas exitosamente",
  "data": {
    "anio": 2025,
    "mes": 9,
    "archivo_guardado": "data/fuentes/obligaciones_9_2025.json",
    "resumen": {
      "obligaciones_generales": 16,
      "obligaciones_especificas": 41,
      "obligaciones_ambientales": 5,
      "obligaciones_anexos": 0,
      "observaciones_generadas": 62
    }
  }
}
```

## 📚 Documentación Interactiva

Puedes acceder a la documentación interactiva de Swagger en:

**http://localhost:8000/docs**

Desde ahí puedes:
- Ver todos los endpoints
- Probar los endpoints directamente desde el navegador
- Ver los esquemas de request/response

## ⚠️ Solución de Problemas

### Error: "Address already in use"

El puerto 8000 está en uso. Cambia el puerto:

```bash
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

### Error: "ModuleNotFoundError"

Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Error: "Connection refused" en Postman

1. Verifica que el servidor esté corriendo
2. Verifica que estés usando la URL correcta: `http://localhost:8000`
3. Verifica que no haya firewall bloqueando el puerto

### Ver logs del servidor

Si ejecutaste con `--reload`, los logs aparecen en la terminal. Si ejecutaste en segundo plano, revisa el archivo `api.log`.

## 🔄 Detener el Servidor

### Si está corriendo en terminal:
- Presiona `Ctrl + C`

### Si está corriendo en segundo plano (Windows):
```powershell
Get-Process python | Where-Object {$_.Path -like "*app.py*"} | Stop-Process
```

### Si está corriendo en segundo plano (Linux/Mac):
```bash
pkill -f "uvicorn app:app"
```

## 📝 Notas

- El servidor se reinicia automáticamente cuando cambias el código (si usas `--reload`)
- Los logs aparecen en la terminal donde ejecutaste el comando
- La documentación Swagger es muy útil para probar endpoints sin Postman

