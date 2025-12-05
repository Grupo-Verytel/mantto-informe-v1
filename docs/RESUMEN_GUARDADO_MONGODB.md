# RESUMEN: GUARDADO DE OBLIGACIONES EN MONGODB

## ✅ Cambios Implementados

### 1. Nuevo Repositorio de MongoDB

Se creó `src/repositories/obligaciones_repository.py` con las siguientes funcionalidades:

- **`guardar_obligaciones()`**: Guarda o actualiza obligaciones en MongoDB
- **`obtener_obligaciones()`**: Obtiene obligaciones desde MongoDB
- **`eliminar_obligaciones()`**: Elimina obligaciones de MongoDB

### 2. Estructura del Documento en MongoDB

Los documentos se guardan en la colección `obligaciones` con la siguiente estructura:

```json
{
  "_id": ObjectId("..."),
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "subseccion": "1.5.1",  // Opcional, solo si se procesa una subsección específica
  "obligaciones_generales": [...],  // Si aplica
  "obligaciones_especificas": [...],  // Si aplica
  "obligaciones_ambientales": [...],  // Si aplica
  "obligaciones_anexos": [...],  // Si aplica
  "user_created": 1,  // Opcional
  "user_updated": 1,  // Opcional
  "created_at": ISODate("2025-01-15T10:30:00Z"),
  "updated_at": ISODate("2025-01-15T10:30:00Z")
}
```

### 3. Integración en el Service

Se agregó el método `guardar_obligaciones_en_mongodb()` al `ObligacionesService`:

```python
await service.guardar_obligaciones_en_mongodb(
    obligaciones=obligaciones_procesadas,
    anio=2025,
    mes=9,
    seccion=1,
    subseccion="1.5.1",  # Opcional
    user_id=1  # Opcional
)
```

### 4. Integración en el Controller

El controller ahora guarda automáticamente en MongoDB después de procesar las obligaciones:

- Si se procesa una subsección específica, guarda solo esa subsección
- Si se procesan todas las obligaciones, guarda todas las subsecciones
- Si MongoDB falla, no interrumpe la respuesta (solo registra un warning)

### 5. Respuesta del Endpoint

La respuesta ahora incluye el ID de MongoDB (si se guardó exitosamente):

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_generales": [...],
  "mongodb_id": "65a1b2c3d4e5f6g7h8i9j0k1"  // Opcional, solo si se guardó en MongoDB
}
```

## 📡 Ejemplo de Uso

### Request con guardado en MongoDB:

**POST** `http://localhost:8000/api/obligaciones/procesar`

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "subseccion": "1.5.1",
  "regenerar_todas": false,
  "guardar_json": true,
  "user_id": 1  // Opcional
}
```

### Respuesta:

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_generales": [
    {
      "item": 1,
      "obligacion": "...",
      "observaciones": "...",
      ...
    }
  ],
  "mongodb_id": "65a1b2c3d4e5f6g7h8i9j0k1"
}
```

## ⚙️ Configuración Requerida

Asegúrate de tener las siguientes variables en tu archivo `.env`:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB=nombre_base_datos
```

O en `config.py`:

```python
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "nombre_base_datos")
```

## 🔍 Consultas en MongoDB

### Obtener obligaciones de una subsección específica:

```javascript
db.obligaciones.findOne({
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "subseccion": "1.5.1"
})
```

### Obtener todas las obligaciones de un mes:

```javascript
db.obligaciones.findOne({
  "anio": 2025,
  "mes": 9,
  "seccion": 1
})
```

### Obtener todas las obligaciones de un año:

```javascript
db.obligaciones.find({
  "anio": 2025,
  "seccion": 1
})
```

## ⚠️ Notas Importantes

1. **Upsert**: Si el documento ya existe (mismo año, mes, sección y subsección), se actualiza. Si no existe, se crea.

2. **Subsecciones**: Si procesas una subsección específica, solo se guarda esa subsección. Si procesas todas, se guardan todas las subsecciones en el mismo documento.

3. **Manejo de Errores**: Si MongoDB falla, el endpoint no falla. Solo se registra un warning en los logs.

4. **User ID**: El `user_id` es opcional. Si se proporciona, se guarda en `user_created` (si es nuevo) y `user_updated` (siempre).

5. **Timestamps**: Se guardan automáticamente `created_at` (solo en creación) y `updated_at` (siempre).

