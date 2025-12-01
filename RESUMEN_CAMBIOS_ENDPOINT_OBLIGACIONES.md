# RESUMEN: CAMBIOS EN ENDPOINT DE OBLIGACIONES

## ✅ Cambios Implementados

### 1. Nuevo Formato de Request

Ahora el endpoint acepta `seccion` y `subseccion`:

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "subseccion": "1.5.1",  // Opcional
  "regenerar_todas": false,
  "guardar_json": true
}
```

### 2. Mapeo de Subsecciones

- **1.5.1** → `obligaciones_generales`
- **1.5.2** → `obligaciones_especificas`
- **1.5.3** → `obligaciones_ambientales`
- **1.5.4** → `obligaciones_anexos` (con verificación de existencia de archivos)

### 3. Nuevo Formato de Respuesta

#### Para subsección 1.5.1 (Obligaciones Generales):
```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_generales": [
    {
      "item": 1,
      "obligacion": "...",
      "periodicidad": "Permanente",
      "cumplio": "Cumplió",
      "observaciones": "...",
      "anexo": "...",
      ...
    }
  ]
}
```

#### Para subsección 1.5.2 (Obligaciones Específicas):
```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_especificas": [...]
}
```

#### Para subsección 1.5.3 (Obligaciones Ambientales):
```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_ambientales": [...]
}
```

#### Para subsección 1.5.4 (Obligaciones de Anexos):
```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_anexos": [
    {
      "item": 1,
      "obligacion": "...",
      "anexo": "ruta/al/archivo.pdf",
      "archivo_existe": true,  // Verificado en SharePoint
      "ruta_anexo": "ruta/al/archivo.pdf",
      ...
    }
  ]
}
```

### 4. Si NO se especifica subsección

Si no se envía `subseccion`, procesa todas las obligaciones y retorna:

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_generales": [...],
  "obligaciones_especificas": [...],
  "obligaciones_ambientales": [...],
  "obligaciones_anexos": [...]
}
```

## 📡 Ejemplos de Uso en Postman

### Ejemplo 1: Procesar solo Obligaciones Generales (1.5.1)

**POST** `http://localhost:8000/api/obligaciones/procesar`

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "subseccion": "1.5.1",
  "regenerar_todas": false,
  "guardar_json": true
}
```

### Ejemplo 2: Verificar existencia de archivos de anexos (1.5.4)

**POST** `http://localhost:8000/api/obligaciones/procesar`

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "subseccion": "1.5.4",
  "regenerar_todas": false,
  "guardar_json": false
}
```

**Respuesta:**
```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_anexos": [
    {
      "item": 1,
      "obligacion": "...",
      "anexo": "11. 01SEP - 30SEP / ANEXO OBLIGACIONES.XLSX",
      "archivo_existe": true,
      "ruta_anexo": "11. 01SEP - 30SEP / ANEXO OBLIGACIONES.XLSX"
    }
  ]
}
```

## 🔧 Funcionalidades Nuevas

1. **Procesamiento por subsección**: Solo procesa la subsección solicitada
2. **Verificación de archivos**: Para 1.5.4, verifica si los archivos existen en SharePoint
3. **Formato de respuesta mejorado**: Respuesta más clara y estructurada
4. **Guardado selectivo**: Solo actualiza la subsección procesada en el JSON

## ⚠️ Notas

- Si `subseccion` no se especifica, procesa todas las obligaciones (comportamiento anterior)
- Para 1.5.4, el campo `archivo_existe` indica si el archivo fue encontrado en SharePoint
- El campo `ruta_anexo` contiene la ruta completa del archivo verificada

