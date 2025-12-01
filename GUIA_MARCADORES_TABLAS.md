# Guía: Configuración de Tablas con Marcadores Únicos

## Problema Resuelto

El sistema anterior tenía problemas para identificar correctamente las tablas cuando había múltiples tablas en el documento. La solución es usar **marcadores únicos** en cada tabla del template Word.

## Cómo Funciona

Cada tabla que necesita ser llenada dinámicamente debe tener un **marcador único** en la primera celda de la primera fila de datos (después del encabezado). El sistema busca estos marcadores y reemplaza la tabla correspondiente con los datos de MongoDB.

## Marcadores Requeridos

Para cada tabla, agrega el marcador correspondiente en la **primera celda de la primera fila de datos** (no en el encabezado):

### 1. Tabla 1.5.1 - OBLIGACIONES GENERALES
- **Marcador**: `{{ TABLA_MARKER_OBLIGACIONES_GENERALES }}`
- **Ubicación**: Primera celda de la primera fila de datos (después del encabezado)

### 2. Tabla 1.5.2 - OBLIGACIONES ESPECÍFICAS DEL CONTRATISTA
- **Marcador**: `{{ TABLA_MARKER_OBLIGACIONES_ESPECIFICAS }}`
- **Ubicación**: Primera celda de la primera fila de datos

### 3. Tabla 1.5.3 - OBLIGACIONES ESPECÍFICAS EN MATERIA AMBIENTAL
- **Marcador**: `{{ TABLA_MARKER_OBLIGACIONES_AMBIENTALES }}`
- **Ubicación**: Primera celda de la primera fila de datos

### 4. Tabla 1.5.4 - OBLIGACIONES ANEXOS
- **Marcador**: `{{ TABLA_MARKER_OBLIGACIONES_ANEXOS }}`
- **Ubicación**: Primera celda de la primera fila de datos

### 5. Tabla 1.6.1 - EMITIDOS CONTRATO SCJ-1809-2024
- **Marcador**: `{{ TABLA_MARKER_COMUNICADOS_EMITIDOS }}`
- **Ubicación**: Primera celda de la primera fila de datos

### 6. Tabla 1.6.2 - RECIBIDOS CONTRATO SCJ-1809-2024
- **Marcador**: `{{ TABLA_MARKER_COMUNICADOS_RECIBIDOS }}`
- **Ubicación**: Primera celda de la primera fila de datos

## Pasos para Configurar el Template

### Paso 1: Abrir el Template
1. Abre el archivo `templates/seccion_1_info_general.docx` en Microsoft Word.

### Paso 2: Configurar Cada Tabla

Para cada tabla que necesita ser llenada dinámicamente:

**OPCIÓN A: Marcador en una fila de datos (RECOMENDADO)**

1. **Identifica la tabla**: Encuentra la tabla correspondiente (ej: "1.5.1. OBLIGACIONES GENERALES").

2. **Estructura de la tabla**:
   - La primera fila debe contener los **encabezados** (ÍTEM, OBLIGACIÓN, PERIODICIDAD, etc.)
   - La segunda fila es la **primera fila de datos** (donde irá el marcador)

3. **Agrega el marcador**:
   - Haz clic en la **primera celda** de la segunda fila (primera fila de datos)
   - Escribe el marcador correspondiente, por ejemplo: `{{ TABLA_MARKER_OBLIGACIONES_GENERALES }}`
   - **IMPORTANTE**: El marcador debe estar exactamente como se muestra, con las llaves dobles `{{` y `}}` y espacios entre las llaves y el nombre de la variable
   - Las otras celdas de esta fila pueden estar vacías

4. **Elimina cualquier contenido previo**: Asegúrate de que la celda solo contenga el marcador, sin texto adicional.

5. **Repite para todas las tablas**: Configura cada tabla con su marcador correspondiente.

**OPCIÓN B: Solo encabezados (ALTERNATIVA)**

Si prefieres una estructura más limpia:
1. Deja la tabla con **solo la fila de encabezados**
2. El sistema detectará la tabla por sus encabezados y la llenará automáticamente
3. **NOTA**: Esta opción requiere que los encabezados sean exactamente como se espera (ÍTEM, OBLIGACIÓN, PERIODICIDAD, etc.)

### Paso 3: Estructura de la Tabla

Cada tabla debe tener esta estructura:

```
┌─────────────────────────────────────────────────────────┐
│ ENCABEZADO (Fila 1)                                      │
│ ┌─────────┬──────────────┬──────────────┬─────────────┐ │
│ │ ÍTEM    │ OBLIGACIÓN   │ PERIODICIDAD │ ...         │ │
│ └─────────┴──────────────┴──────────────┴─────────────┘ │
│                                                           │
│ FILA DE DATOS (Fila 2) - AQUÍ VA EL MARCADOR            │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ {{ TABLA_MARKER_OBLIGACIONES_GENERALES }}           │ │
│ │ (marcador en la primera celda, otras celdas vacías) │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**NOTA**: Puedes usar **2 filas** en el template:
- Fila 1: Encabezados
- Fila 2: Primera fila de datos (con el marcador en la primera celda) - OPCIONAL

O solo **1 fila**:
- Fila 1: Encabezados solamente

El sistema eliminará automáticamente cualquier fila de datos existente y creará nuevas filas con los datos reales.

### Paso 4: Guardar y Probar

1. Guarda el template en Word.
2. Cierra Word completamente.
3. Reinicia el servidor FastAPI.
4. Genera el documento:
   ```bash
   POST /api/seccion1/generar
   {
     "anio": 2025,
     "mes": 9
   }
   ```
5. Verifica que todas las tablas se llenaron correctamente.

## Ejemplo Visual

### Antes (Template):
```
┌─────────────────────────────────────────────────────────┐
│ ÍTEM │ OBLIGACIÓN │ PERIODICIDAD │ CUMPLIÓ │ OBSERVACIONES │ ANEXO │
├─────────────────────────────────────────────────────────┤
│ {{ TABLA_MARKER_OBLIGACIONES_GENERALES }} │ │ │ │ │ │
└─────────────────────────────────────────────────────────┘
```

### Después (Documento Generado):
```
┌─────────────────────────────────────────────────────────┐
│ ÍTEM │ OBLIGACIÓN │ PERIODICIDAD │ CUMPLIÓ │ OBSERVACIONES │ ANEXO │
├─────────────────────────────────────────────────────────┤
│ 1    │ Texto...   │ Permanente   │ Cumplió │ Observación...│ Anexo │
│ 2    │ Texto...   │ Mensual      │ Cumplió │ Observación...│ Anexo │
│ 3    │ Texto...   │ Trimestral   │ Cumplió │ Observación...│ Anexo │
│ ...  │ ...        │ ...          │ ...     │ ...           │ ...   │
└─────────────────────────────────────────────────────────┘
```

## Ventajas de Este Enfoque

1. **Identificación precisa**: Cada tabla se identifica de forma única por su marcador, sin depender de índices o búsquedas por texto.

2. **Sin confusiones**: Aunque haya múltiples tablas en el documento, cada una se identifica correctamente.

3. **Fácil de mantener**: Si cambias el orden de las tablas o agregas nuevas, solo necesitas agregar el marcador correcto.

4. **Robusto**: No depende de la estructura del documento ni de la posición de las tablas.

## Solución de Problemas

### Error: "No se encontró tabla con marcador '...'"
- **Causa**: El marcador no está en el template o está mal escrito.
- **Solución**: 
  1. Verifica que el marcador esté exactamente como se muestra: `{{ TABLA_MARKER_XXXXX }}`
  2. Asegúrate de que esté en la primera celda de la primera fila de datos (no en el encabezado).
  3. Verifica que no haya espacios extra o caracteres invisibles.
  4. Asegúrate de que el marcador use la sintaxis correcta de Jinja2: `{{ variable }}` (con espacios)

### Error: Tabla se llena con datos incorrectos
- **Causa**: El marcador está en la tabla incorrecta.
- **Solución**: Verifica que cada tabla tenga el marcador correcto según su sección.

### Error: El marcador aparece en el documento generado
- **Causa**: El sistema no pudo limpiar el marcador correctamente.
- **Solución**: Asegúrate de que el marcador esté en una celda separada, sin texto adicional.

## Notas Importantes

- Los marcadores son **case-sensitive** (sensible a mayúsculas/minúsculas). Usa exactamente el formato mostrado.
- El marcador debe estar en la **primera celda** de la primera fila de datos.
- No mezcles marcadores: cada tabla debe tener su marcador único.
- El sistema eliminará automáticamente la fila que contiene el marcador y creará nuevas filas con los datos.
- **IMPORTANTE**: Los marcadores usan sintaxis válida de Jinja2 (`{{ variable }}`), por lo que Jinja2 los procesará y los convertirá en `[[TABLA_XXX]]` que luego el sistema buscará para identificar cada tabla.

