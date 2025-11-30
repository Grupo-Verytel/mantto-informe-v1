# 📋 GUÍA: Usar Jinja2 Directamente en Tablas del Template

## ✅ Estado Actual

El código está configurado para usar **Jinja2 directamente** en las tablas del template Word. No se necesita código Python adicional para llenar las tablas - docxtpl lo hace automáticamente.

---

## 📝 CÓMO CONFIGURAR EL TEMPLATE

### Estructura de Cada Tabla

Cada tabla debe tener **exactamente 2 filas**:

1. **Fila 1 (Encabezado)**: Solo los nombres de las columnas
2. **Fila 2 (Datos)**: El loop de Jinja2 con las variables

---

## 🔧 CONFIGURACIÓN POR TABLA

### Tabla 1.5.1: OBLIGACIONES GENERALES

**Fila 1 (Encabezado):**
```
ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ / NO CUMPLIÓ | OBSERVACIONES | ANEXO
```

**Fila 2 (Datos - PRIMERA FILA):**

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

### Tabla 1.6.1: COMUNICADOS EMITIDOS

**Fila 1 (Encabezado):**
```
ÍTEM | FECHA | CONSECUTIVO | ASUNTO
```

**Fila 2 (Datos):**

**Celda 1 (ÍTEM):**
```
{% for comunicado in tabla_comunicados_emitidos %}
{{ comunicado.item }}
```

**Celda 2 (FECHA):**
```
{{ comunicado.fecha }}
```

**Celda 3 (CONSECUTIVO):**
```
{{ comunicado.consecutivo }}
```

**Celda 4 (ASUNTO):**
```
{{ comunicado.asunto }}
{% endfor %}
```

---

### Tabla 1.6.2: COMUNICADOS RECIBIDOS

**Fila 1 (Encabezado):**
```
ÍTEM | FECHA | CONSECUTIVO | ASUNTO
```

**Fila 2 (Datos):**

**Celda 1 (ÍTEM):**
```
{% for comunicado in tabla_comunicados_recibidos %}
{{ comunicado.item }}
```

**Celda 2 (FECHA):**
```
{{ comunicado.fecha }}
```

**Celda 3 (CONSECUTIVO):**
```
{{ comunicado.consecutivo }}
```

**Celda 4 (ASUNTO):**
```
{{ comunicado.asunto }}
{% endfor %}
```

---

## ⚠️ REGLAS IMPORTANTES

1. **El `{% for %}` debe estar en la PRIMERA celda** de la fila de datos
2. **El `{% endfor %}` debe estar en la ÚLTIMA celda** de la misma fila
3. **Solo debe haber 2 filas**: encabezado + fila con loop
4. **Elimina todas las demás filas de datos** - docxtpl las generará automáticamente
5. **No uses espacios extra** al inicio o final de las celdas

---

## 📊 VARIABLES DISPONIBLES

### Para `tabla_obligaciones_generales`, `tabla_obligaciones_especificas`, `tabla_obligaciones_ambientales`:

- `obligacion.item` - Número de ítem
- `obligacion.obligacion` - Texto de la obligación
- `obligacion.periodicidad` - Periodicidad (Permanente, Mensual, etc.)
- `obligacion.cumplio` - "Cumplió" o "No Cumplió"
- `obligacion.observaciones` - Observaciones generadas
- `obligacion.anexo` - Ruta del anexo

### Para `tabla_comunicados_emitidos`, `tabla_comunicados_recibidos`:

- `comunicado.item` - Número de ítem
- `comunicado.fecha` - Fecha del comunicado
- `comunicado.consecutivo` - Número de radicado/consecutivo
- `comunicado.asunto` - Asunto del comunicado
- `comunicado.descripcion` - Alias de asunto

---

## 🔧 PASOS EN WORD

1. **Abre** `templates/seccion_1_info_general.docx` en Word
2. **Navega** hasta cada tabla
3. **Asegúrate** de que tenga solo 2 filas (encabezado + fila de datos)
4. **Agrega** el loop de Jinja2 según la estructura mostrada arriba
5. **Guarda** el template
6. **Prueba** generando el documento

---

## ✅ VENTAJAS DE ESTE ENFOQUE

- ✅ **Control total**: Tú decides exactamente cómo se estructura cada tabla
- ✅ **Más simple**: No necesitas código Python adicional
- ✅ **Fácil de mantener**: Los cambios se hacen directamente en Word
- ✅ **Funciona automáticamente**: docxtpl detecta los loops y genera las filas

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

---

## 🚨 SI HAY PROBLEMAS

### El archivo se corrompe al abrir

- Verifica que no haya espacios extra en las celdas
- Asegúrate de que el `{% for %}` y `{% endfor %}` estén en la misma fila
- Limpia cada celda manualmente

### No se generan filas

- Verifica que el nombre de la variable coincida exactamente
- Revisa los logs del servidor para ver si hay datos en MongoDB
- Asegúrate de que el loop esté correctamente cerrado

### Solo se genera una fila

- Verifica que haya múltiples elementos en la lista
- Revisa los logs para ver cuántos elementos se cargaron

