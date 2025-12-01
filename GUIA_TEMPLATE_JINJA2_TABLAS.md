# 📋 GUÍA: Configurar Tablas con Jinja2 en el Template

## 🎯 Objetivo

Configurar las tablas del template para que se llenen automáticamente usando loops de Jinja2 directamente en Word.

---

## ✅ VENTAJAS DE USAR JINJA2 EN EL TEMPLATE

- ✅ **Mayor control**: Tú decides exactamente cómo se estructura cada tabla
- ✅ **Más flexible**: Puedes agregar condicionales y lógica directamente en el template
- ✅ **Más simple**: No necesitas código Python adicional para cada tabla
- ✅ **Fácil de mantener**: Los cambios se hacen directamente en Word

---

## 📝 ESTRUCTURA CORRECTA PARA CADA TABLA

### Tabla 1.5.1: OBLIGACIONES GENERALES

**Fila 1 (Encabezado):**
```
ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ / NO CUMPLIÓ | OBSERVACIONES | ANEXO
```

**Fila 2 (Datos - PRIMERA FILA DE DATOS):**

**Celda 1 (ÍTEM):**
```
{% for obligacion in tabla_obligaciones_generales %}
{{ obligacion.item }}
```

**Celda 2 (OBLIGACIÓN):**
```
{{ obligacion.obligacion }}
```

**Celda 3 (PERIODICIDAD):**
```
{{ obligacion.periodicidad }}
```

**Celda 4 (CUMPLIÓ):**
```
{{ obligacion.cumplio }}
```

**Celda 5 (OBSERVACIONES):**
```
{{ obligacion.observaciones }}
```

**Celda 6 (ANEXO):**
```
{{ obligacion.anexo }}
{% endfor %}
```

**IMPORTANTE:**
- ✅ El `{% for %}` debe estar en la **primera celda** de la fila de datos
- ✅ El `{% endfor %}` debe estar en la **última celda** de la misma fila
- ✅ **Elimina todas las demás filas de datos** - docxtpl las generará automáticamente
- ✅ Solo debe haber **2 filas**: encabezado + fila con loop

---

### Tabla 1.5.2: OBLIGACIONES ESPECÍFICAS

**Fila 1 (Encabezado):**
```
ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ / NO CUMPLIÓ | OBSERVACIONES | ANEXO
```

**Fila 2 (Datos):**

**Celda 1:**
```
{% for obligacion in tabla_obligaciones_especificas %}
{{ obligacion.item }}
```

**Celda 2:**
```
{{ obligacion.obligacion }}
```

**Celda 3:**
```
{{ obligacion.periodicidad }}
```

**Celda 4:**
```
{{ obligacion.cumplio }}
```

**Celda 5:**
```
{{ obligacion.observaciones }}
```

**Celda 6:**
```
{{ obligacion.anexo }}
{% endfor %}
```

---

### Tabla 1.5.3: OBLIGACIONES AMBIENTALES

**Fila 1 (Encabezado):**
```
ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ / NO CUMPLIÓ | OBSERVACIONES | ANEXO
```

**Fila 2 (Datos):**

**Celda 1:**
```
{% for obligacion in tabla_obligaciones_ambientales %}
{{ obligacion.item }}
```

**Celda 2:**
```
{{ obligacion.obligacion }}
```

**Celda 3:**
```
{{ obligacion.periodicidad }}
```

**Celda 4:**
```
{{ obligacion.cumplio }}
```

**Celda 5:**
```
{{ obligacion.observaciones }}
```

**Celda 6:**
```
{{ obligacion.anexo }}
{% endfor %}
```

---

### Tabla 1.5.4: OBLIGACIONES ANEXOS

**Opción 1: Formato Simple (si los datos tienen `archivo_existe` y `anexo`)**

**Fila 1 (Encabezado):**
```
ÍTEM | ARCHIVO EXISTE | ANEXO
```

**Fila 2 (Datos):**

**Celda 1:**
```
{% for anexo in tabla_obligaciones_anexos %}
{{ loop.index }}
```

**Celda 2:**
```
{% if anexo.archivo_existe %}Sí{% else %}No{% endif %}
```

**Celda 3:**
```
{{ anexo.anexo }}
{% endfor %}
```

**Opción 2: Formato Estándar (si los datos tienen estructura completa)**

**Fila 1 (Encabezado):**
```
ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ / NO CUMPLIÓ | OBSERVACIONES | ANEXO
```

**Fila 2 (Datos):**

**Celda 1:**
```
{% for obligacion in tabla_obligaciones_anexos %}
{{ obligacion.item }}
```

**Celda 2:**
```
{{ obligacion.obligacion }}
```

**Celda 3:**
```
{{ obligacion.periodicidad }}
```

**Celda 4:**
```
{{ obligacion.cumplio }}
```

**Celda 5:**
```
{{ obligacion.observaciones }}
```

**Celda 6:**
```
{{ obligacion.anexo }}
{% endfor %}
```

---

## 🔧 PASOS PARA CONFIGURAR EN WORD

### Paso 1: Abrir el Template

1. Abre `templates/seccion_1_info_general.docx` en Microsoft Word
2. Navega hasta la tabla que quieres configurar

### Paso 2: Verificar la Estructura

1. **Asegúrate de que la tabla tenga solo 2 filas:**
   - Fila 1: Encabezados
   - Fila 2: Loop de Jinja2 (primera fila de datos)

2. **Elimina cualquier otra fila de datos**

### Paso 3: Agregar el Loop

1. **Selecciona la celda 1 de la fila 2**
2. **Escribe el loop de inicio:**
   ```
   {% for obligacion in tabla_obligaciones_generales %}
   ```
3. **Presiona Enter** para crear un salto de línea
4. **Escribe la variable:**
   ```
   {{ obligacion.item }}
   ```

5. **Repite para cada celda** según la estructura mostrada arriba

6. **En la última celda**, agrega `{% endfor %}` al final

### Paso 4: Limpiar Espacios

1. **Selecciona toda la fila 2**
2. **Presiona Ctrl+H** (Buscar y Reemplazar)
3. **Elimina espacios dobles** o caracteres invisibles

### Paso 5: Guardar

1. **Guarda el template** (`Ctrl+S`)
2. **Cierra Word**

---

## ⚠️ ERRORES COMUNES Y SOLUCIONES

### Error: "El archivo está dañado"

**Causa:** Espacios extra o saltos de línea incorrectos en las celdas

**Solución:**
1. Limpia cada celda manualmente
2. Asegúrate de que no haya espacios al inicio o final
3. Verifica que el `{% for %}` y `{% endfor %}` estén en la misma fila

### Error: "No se generan filas"

**Causa:** El loop no está correctamente cerrado o la variable no existe

**Solución:**
1. Verifica que `{% endfor %}` esté en la última celda de la misma fila
2. Verifica que el nombre de la variable coincida exactamente (ej: `tabla_obligaciones_generales`)
3. Revisa los logs del servidor para ver si hay errores

### Error: "Solo se genera una fila"

**Causa:** La lista en MongoDB está vacía o tiene solo un elemento

**Solución:**
1. Verifica que haya datos en MongoDB para esa subsección
2. Revisa los logs para ver cuántos elementos se cargaron

---

## 📊 VARIABLES DISPONIBLES

### Para `tabla_obligaciones_generales`, `tabla_obligaciones_especificas`, `tabla_obligaciones_ambientales`:

- `obligacion.item` - Número de ítem
- `obligacion.obligacion` - Texto de la obligación
- `obligacion.periodicidad` - Periodicidad (Permanente, Mensual, etc.)
- `obligacion.cumplio` - "Cumplió" o "No Cumplió"
- `obligacion.observaciones` - Observaciones generadas
- `obligacion.anexo` - Ruta del anexo

### Para `tabla_obligaciones_anexos` (formato simple):

- `anexo.archivo_existe` - Boolean (true/false)
- `anexo.anexo` - Ruta o mensaje del anexo
- `loop.index` - Número de iteración (1, 2, 3, ...)

---

## ✅ CHECKLIST

Antes de generar el documento, verifica:

- [ ] Cada tabla tiene exactamente 2 filas (encabezado + fila con loop)
- [ ] El `{% for %}` está en la primera celda de la fila de datos
- [ ] El `{% endfor %}` está en la última celda de la misma fila
- [ ] No hay espacios extra al inicio o final de las celdas
- [ ] Los nombres de las variables coinciden exactamente
- [ ] El template está guardado correctamente

---

## 🧪 PROBAR

1. **Configura todas las tablas** según esta guía
2. **Genera el documento:**
   ```bash
   POST /api/seccion1/generar
   {
     "anio": 2025,
     "mes": 9
   }
   ```
3. **Abre el archivo generado** y verifica que todas las tablas se llenaron correctamente

