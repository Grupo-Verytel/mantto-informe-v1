# 📋 INSTRUCCIONES: Configurar Márgenes de Tablas en Sección 4

## 🎯 OBJETIVO

Configurar el template `seccion_4_bienes_servicios.docx` para que las tablas respeten los márgenes izquierdo y derecho del documento, igual que en la sección 2.

## 🔧 PASOS PARA CONFIGURAR EL TEMPLATE

### Paso 1: Abrir el Template

1. Abre el archivo `src/resources/templates/seccion_4_bienes_servicios.docx` en Microsoft Word

### Paso 2: Verificar Márgenes del Documento

1. Ve a la pestaña **"Diseño"** (o **"Diseño de página"** en versiones anteriores)
2. Haz clic en **"Márgenes"**
3. Verifica que los márgenes sean los mismos que en `seccion_2_mesa_servicio.docx`:
   - **Superior**: 2.5 cm (o el que uses)
   - **Inferior**: 2.5 cm (o el que uses)
   - **Izquierdo**: 2.5 cm (o el que uses)
   - **Derecho**: 2.5 cm (o el que uses)

### Paso 3: Configurar las Tablas en el Template

Para cada placeholder de tabla (`[[TABLE_41]]`, `[[TABLE_42]]`, `[[TABLE_43]]`, `[[TABLE_44]]`):

1. **Selecciona el placeholder** (por ejemplo, `[[TABLE_42]]`)
2. Ve a la pestaña **"Diseño"** (en la barra de herramientas de tabla)
3. En el grupo **"Tamaño de celda"**, haz clic en **"Autoajustar"**
4. Selecciona **"Autoajustar a la ventana"** (o **"Autoajustar al contenido"** si prefieres)

**IMPORTANTE:** Si no ves la opción "Autoajustar a la ventana", puedes:
- Hacer clic derecho en el placeholder → **"Propiedades de tabla"** → Pestaña **"Tabla"** → En **"Tamaño"**, marca **"Ajustar automáticamente al ancho de la ventana"**

### Paso 4: Verificar que no haya Ancho Fijo

1. Si hay una tabla de ejemplo en el template (aunque esté vacía):
   - Haz clic derecho en la tabla → **"Propiedades de tabla"**
   - Pestaña **"Tabla"**
   - En **"Tamaño"**, asegúrate de que **NO** esté marcado "Ancho preferido" con un valor fijo
   - Si está marcado, desmárcalo o cambia a "Ajustar automáticamente al ancho de la ventana"

### Paso 5: Guardar el Template

1. **Guarda el template** (`Ctrl+S`)
2. Cierra Word

## ✅ VERIFICACIÓN

Después de configurar el template:

1. **Genera un documento** usando el endpoint de la sección 4
2. **Abre el documento generado** en Word
3. **Verifica que las tablas**:
   - ✅ Respeten los márgenes izquierdo y derecho
   - ✅ No se estiren más allá del área de contenido
   - ✅ Se vean igual que las tablas de la sección 2

## 🔍 SOLUCIÓN ALTERNATIVA: Si las Tablas Siguen Estiradas

Si después de seguir estos pasos las tablas siguen estiradas:

### Opción 1: Copiar Configuración desde Sección 2

1. Abre `seccion_2_mesa_servicio.docx` en Word
2. Selecciona una tabla que se vea bien
3. Haz clic derecho → **"Propiedades de tabla"**
4. Anota la configuración (especialmente en la pestaña "Tabla")
5. Aplica la misma configuración a las tablas en `seccion_4_bienes_servicios.docx`

### Opción 2: Eliminar Tablas de Ejemplo del Template

Si el template tiene tablas de ejemplo con ancho fijo:

1. **Elimina las tablas de ejemplo** del template
2. **Deja solo el placeholder** `[[TABLE_XX]]` en un párrafo normal
3. El código creará la tabla automáticamente con la configuración correcta

### Opción 3: Verificar Estilos de Tabla

1. Selecciona el placeholder o una tabla de ejemplo
2. Ve a la pestaña **"Diseño"** (herramientas de tabla)
3. En **"Estilos de tabla"**, verifica que no haya un estilo que fuerce el ancho
4. Si es necesario, cambia a un estilo más simple como **"Tabla con cuadrícula"**

## 📝 NOTAS IMPORTANTES

- **El código ya está configurado** para usar `autofit` y respetar márgenes
- **El problema suele estar en el template** si tiene configuraciones de ancho fijo
- **Las tablas se crean programáticamente**, así que el template solo necesita el placeholder
- **No es necesario** tener tablas de ejemplo en el template, solo el placeholder `[[TABLE_XX]]`

## 🎯 RESULTADO ESPERADO

Después de configurar correctamente:

- ✅ Las tablas respetan los márgenes izquierdo y derecho
- ✅ Las tablas no se estiran más allá del área de contenido
- ✅ Las tablas se ven igual que en la sección 2
- ✅ El encabezado se repite en cada página (ya configurado en el código)

