# 📋 INSTRUCCIONES: Corregir Template con Error en Word

## 🎯 Objetivo

Corregir el template para que el archivo Word generado se abra sin errores.

---

## 🔧 PASOS PARA CORREGIR EL TEMPLATE

### Paso 1: Abrir el Template

1. Abre `templates/seccion_1_info_general.docx` en Microsoft Word
2. Navega hasta la tabla de "OBLIGACIONES GENERALES"

### Paso 2: Verificar la Estructura de la Tabla

La tabla debe tener:
- **Fila 1:** Encabezados (ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ / NO CUMPLIÓ | OBSERVACIONES | ANEXO)
- **Fila 2:** Loop de Jinja2 (solo esta fila, sin más filas de datos)

### Paso 3: Limpiar las Celdas de la Fila 2

**IMPORTANTE:** Cada celda debe contener **SOLO** el texto necesario, sin espacios extra.

#### Celda 1 (ÍTEM):
1. Selecciona la celda
2. Presiona `Ctrl+A` para seleccionar todo
3. Escribe exactamente (sin espacios al inicio o final):
   ```
   {% for obligacion in tabla_obligaciones_generales %}
   ```
4. Presiona `Enter` para crear un salto de línea
5. Escribe:
   ```
   {{ obligacion.item }}
   ```

#### Celda 2 (OBLIGACIÓN):
1. Selecciona la celda
2. Escribe exactamente:
   ```
   {{ obligacion.obligacion }}
   ```

#### Celda 3 (PERIODICIDAD):
1. Selecciona la celda
2. Escribe exactamente:
   ```
   {{ obligacion.periodicidad }}
   ```

#### Celda 4 (CUMPLIÓ):
1. Selecciona la celda
2. Escribe exactamente:
   ```
   {{ obligacion.cumplio }}
   ```

#### Celda 5 (OBSERVACIONES):
1. Selecciona la celda
2. Escribe exactamente:
   ```
   {{ obligacion.observaciones }}
   ```

#### Celda 6 (ANEXO):
1. Selecciona la celda
2. Escribe exactamente:
   ```
   {{ obligacion.anexo }}
   ```
3. Presiona `Enter` para crear un salto de línea
4. Escribe:
   ```
   {% endfor %}
   ```

### Paso 4: Eliminar Espacios y Caracteres Invisibles

1. **Selecciona toda la fila 2** (haz clic en el borde izquierdo de la fila)
2. **Presiona `Ctrl+H`** (Buscar y Reemplazar)
3. **En "Buscar"**, escribe un espacio (presiona la barra espaciadora)
4. **En "Reemplazar"**, deja vacío
5. **Haz clic en "Reemplazar todo"** (solo en la fila seleccionada)
6. **Repite** para eliminar espacios dobles

### Paso 5: Verificar que No Haya Filas Extra

1. **Asegúrate de que solo haya 2 filas** en la tabla:
   - Fila 1: Encabezados
   - Fila 2: Loop de Jinja2
2. **Elimina cualquier otra fila** que pueda existir

### Paso 6: Guardar el Template

1. **Guarda el template** (`Ctrl+S`)
2. **Cierra Word**

---

## ✅ VERIFICACIÓN FINAL

Después de corregir el template, verifica:

- [ ] La tabla tiene exactamente 2 filas
- [ ] La fila 1 tiene los encabezados
- [ ] La fila 2 tiene el loop completo:
  - Celda 1: `{% for obligacion in tabla_obligaciones_generales %}` + `{{ obligacion.item }}`
  - Celda 2: `{{ obligacion.obligacion }}`
  - Celda 3: `{{ obligacion.periodicidad }}`
  - Celda 4: `{{ obligacion.cumplio }}`
  - Celda 5: `{{ obligacion.observaciones }}`
  - Celda 6: `{{ obligacion.anexo }}` + `{% endfor %}`
- [ ] No hay espacios extra al inicio o final de las celdas
- [ ] El template está guardado

---

## 🧪 PROBAR EL TEMPLATE

1. **Genera el documento usando el API:**
   ```bash
   POST /api/seccion1/generar
   {
     "anio": 2025,
     "mes": 9
   }
   ```

2. **Abre el archivo generado en Word**
3. **Verifica que:**
   - ✅ Se abre sin errores
   - ✅ Las tablas tienen las filas correctas
   - ✅ Los datos están completos

---

## 🚨 SI PERSISTE EL ERROR

### Opción 1: Recrear la Tabla desde Cero

1. **Elimina la tabla actual**
2. **Crea una nueva tabla** con 6 columnas y 2 filas
3. **Sigue los pasos anteriores** para agregar el loop

### Opción 2: Usar Reemplazo Programático

Si el error persiste, puedes usar el método de reemplazo programático:

1. **En el template, deja la tabla vacía** (solo encabezados, sin fila de datos)
2. **El código la llenará automáticamente** usando `_reemplazar_tabla_obligaciones_generales()`

Para esto, modifica `generar()` en `seccion_1_info_general.py` para usar el reemplazo programático en lugar de Jinja2.

