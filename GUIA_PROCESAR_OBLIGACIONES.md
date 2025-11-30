# GUÍA: PROCESAR OBLIGACIONES DE LA SECCIÓN 1.5

## 🎯 OBJETIVO

Procesar las obligaciones de la sección 1.5 (Generales, Específicas, Ambientales) y generar observaciones dinámicamente desde los anexos de SharePoint usando LLM.

## 📋 ESTRUCTURA DE DATOS

### Archivo JSON de Obligaciones

**Ubicación:** `data/fuentes/obligaciones_{mes}_{anio}.json`

**Estructura:**
```json
{
  "obligaciones_generales": [
    {
      "item": 1,
      "obligacion": "Texto de la obligación...",
      "periodicidad": "Permanente",
      "cumplio": "Cumplió",
      "observaciones": "",  // Se genera dinámicamente
      "anexo": "11. 01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ archivo.pdf",
      "regenerar_observacion": true,  // Si debe regenerar la observación
      "revisaranexo": true,  // Si debe revisar el anexo
      "defaultobservaciones": ""  // Observación por defecto si revisaranexo=false
    }
  ],
  "obligaciones_especificas": [...],
  "obligaciones_ambientales": [...],
  "obligaciones_anexos": []
}
```

### Campos Importantes

- **`regenerar_observacion`**: Si `true`, regenera la observación incluso si ya existe
- **`revisaranexo`**: Si `false`, usa `defaultobservaciones` sin verificar el anexo
- **`defaultobservaciones`**: Observación por defecto cuando `revisaranexo=false`
- **`anexo`**: Ruta relativa del archivo en SharePoint (ej: "11. 01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ archivo.pdf")

## 🔧 USO

### Opción 1: Script de Línea de Comandos

```bash
# Procesar obligaciones de Septiembre 2025
python procesar_obligaciones_seccion1.py 2025 9

# Solo especificar año (usa mes actual)
python procesar_obligaciones_seccion1.py 2025
```

### Opción 2: API REST (si tienes FastAPI configurado)

```bash
POST /api/obligaciones/procesar
Content-Type: application/json

{
  "anio": 2025,
  "mes": 9,
  "regenerar_todas": false,
  "guardar_json": true
}
```

### Opción 3: Desde Python

```python
from src.services.obligaciones_service import ObligacionesService

service = ObligacionesService()

# Procesar todas las obligaciones
obligaciones = service.procesar_todas_las_obligaciones(
    anio=2025,
    mes=9,
    regenerar_todas=False  # Solo regenera las que tienen regenerar_observacion=true
)

# Guardar resultados
service.guardar_obligaciones_procesadas(
    obligaciones,
    anio=2025,
    mes=9,
    crear_backup=True
)
```

## 🔄 FLUJO DE PROCESAMIENTO

```
1. Cargar obligaciones desde JSON
   ↓
2. Para cada obligación:
   ├─ Si regenerar_observacion=false y ya tiene observación → Saltar
   ├─ Si revisaranexo=false → Usar defaultobservaciones
   └─ Si revisaranexo=true:
      ├─ Resolver ruta del anexo (SharePoint o local)
      ├─ Descargar archivo desde SharePoint (si aplica)
      ├─ Extraer texto (PDF/Word/Excel)
      ├─ Generar observación con LLM
      └─ Actualizar obligación con observación
   ↓
3. Guardar obligaciones procesadas en JSON (con backup)
```

## ⚙️ CONFIGURACIÓN REQUERIDA

### Variables de Entorno (.env)

```env
# SharePoint (Microsoft Graph API)
SHAREPOINT_SITE_URL=https://empresa.sharepoint.com/sites/Sitio
SHAREPOINT_CLIENT_ID=tu-client-id
SHAREPOINT_CLIENT_SECRET=tu-client-secret
SHAREPOINT_TENANT_ID=tu-tenant-id
SHAREPOINT_BASE_PATH=Shared Documents/PROYECTOS/...

# OpenAI (LLM)
OPENAI_API_KEY=tu-api-key
OPENAI_MODEL=gpt-4o-mini
```

## 📊 RESULTADO

Después de procesar, el archivo JSON se actualiza con:

- **`observaciones`**: Texto generado dinámicamente desde el anexo
- **`observacion_generada_llm`**: `true` si fue generada con LLM, `false` si es por defecto

El archivo original se guarda como backup: `obligaciones_{mes}_{anio}.backup_{mes}_{anio}.json`

## 🔍 EJEMPLOS

### Ejemplo 1: Obligación que revisa anexo

```json
{
  "item": 2,
  "obligacion": "Cumplir con lo previsto...",
  "periodicidad": "Permanente",
  "cumplio": "Cumplió",
  "observaciones": "",  // Se generará desde el anexo
  "anexo": "11. 01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ INFORME MENSUAL SEPTIEMBRE 2025.pdf",
  "regenerar_observacion": true,
  "revisaranexo": true,
  "defaultobservaciones": ""
}
```

**Resultado:**
- Descarga el PDF desde SharePoint
- Extrae texto del PDF
- Genera observación con LLM basándose en el contenido
- Actualiza `observaciones` con el texto generado

### Ejemplo 2: Obligación con observación por defecto

```json
{
  "item": 1,
  "obligacion": "Ejecutar el contrato...",
  "periodicidad": "Permanente",
  "cumplio": "Cumplió",
  "observaciones": "",
  "anexo": "11. 01SEP - 30SEP / 02 OBLIGACIONES ESPECIFICAS / OBLIGACIÓN 1,9,10...",
  "regenerar_observacion": true,
  "revisaranexo": false,  // No revisa anexo
  "defaultobservaciones": "Se da cumplimiento con el presente informe y sus anexos."
}
```

**Resultado:**
- No descarga ni revisa el anexo
- Usa directamente `defaultobservaciones`
- Actualiza `observaciones` con el texto por defecto

## 🚨 TROUBLESHOOTING

### Error: "No se pudo inicializar extractor de observaciones"

- Verifica que las variables de entorno de SharePoint estén configuradas
- Verifica que `OPENAI_API_KEY` esté configurada
- Revisa los logs para más detalles

### Error: "El archivo no existe en SharePoint"

- Verifica que la ruta del anexo sea correcta
- Verifica permisos de la App Registration en SharePoint
- Verifica que `SHAREPOINT_BASE_PATH` esté correctamente configurado

### Observaciones vacías

- Verifica que el archivo del anexo tenga contenido extraíble
- Verifica que `OPENAI_API_KEY` sea válida
- Revisa los logs para ver si hubo errores en la extracción o generación

## 📝 NOTAS

- El proceso puede tardar varios minutos dependiendo del número de obligaciones y tamaño de los anexos
- Se crea un backup automático antes de guardar los cambios
- Las observaciones generadas son profesionales y contextualizadas según el contenido del anexo

