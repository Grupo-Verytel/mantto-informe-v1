# EJEMPLO PRÁCTICO: Crear Tabla Dinámica en Template Word con docxtpl

## 🎯 Objetivo

Crear una tabla de obligaciones generales que se llene automáticamente desde MongoDB usando docxtpl y Jinja2.

---

## 📝 PASOS DETALLADOS

### Paso 1: Abrir el Template en Word

1. Abre `templates/seccion_1_info_general.docx` en Microsoft Word
2. Navega hasta la sección "1.5.1. OBLIGACIONES GENERALES"

### Paso 2: Crear la Tabla

1. Inserta una tabla con **6 columnas** y **2 filas** (1 encabezado + 1 fila de datos)
2. En la **fila 1 (encabezado)**, escribe:
   - Columna 1: `ÍTEM`
   - Columna 2: `OBLIGACIÓN`
   - Columna 3: `PERIODICIDAD`
   - Columna 4: `CUMPLIÓ / NO CUMPLIÓ`
   - Columna 5: `OBSERVACIONES`
   - Columna 6: `ANEXO`

3. **Formatea el encabezado** (negrita, fondo gris, etc.)

### Paso 3: Agregar el Loop de Jinja2

En la **fila 2 (primera fila de datos)**, coloca las variables de Jinja2:

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

### Paso 4: Formatear la Fila de Datos

1. Aplica el formato que desees a la fila 2 (fuentes, tamaños, alineación)
2. Este formato se copiará automáticamente a todas las filas generadas

### Paso 5: Guardar el Template

Guarda el template. El resultado debería verse así:

```
┌──────┬──────────────────────┬──────────────┬──────────────────┬──────────────┬──────────┐
│ ÍTEM │ OBLIGACIÓN          │ PERIODICIDAD │ CUMPLIÓ         │ OBSERVACIONES│ ANEXO    │
├──────┼──────────────────────┼──────────────┼──────────────────┼──────────────┼──────────┤
│ {%   │ {{ obligacion.      │ {{ obligacion│ {{ obligacion.  │ {{ obligacion│ {{ obligacion.anexo }}│
│ for  │ obligacion }}       │ .periodicidad│ cumplio }}      │ .observaciones│ {% endfor %}│
│ ...  │                     │ }}           │                 │ }}           │          │
└──────┴──────────────────────┴──────────────┴──────────────────┴──────────────┴──────────┘
```

---

## ✅ RESULTADO ESPERADO

Cuando generes el documento usando el API:

```bash
POST /api/seccion1/generar
{
  "anio": 2025,
  "mes": 9
}
```

docxtpl:
1. Encontrará el loop `{% for obligacion in tabla_obligaciones_generales %}`
2. Iterará sobre cada obligación en la lista
3. Generará una fila por cada obligación
4. Mantendrá el formato de la fila original

**Ejemplo de salida generada:**

```
┌──────┬──────────────────────┬──────────────┬──────────────────┬──────────────┬──────────┐
│ ÍTEM │ OBLIGACIÓN          │ PERIODICIDAD │ CUMPLIÓ         │ OBSERVACIONES│ ANEXO    │
├──────┼──────────────────────┼──────────────┼──────────────────┼──────────────┼──────────┤
│ 1    │ Texto obligación 1  │ Permanente   │ Cumplió         │ Observación 1│ Anexo1   │
│ 2    │ Texto obligación 2  │ Mensual      │ Cumplió         │ Observación 2│ Anexo2   │
│ 3    │ Texto obligación 3  │ Permanente   │ No Cumplió      │ Observación 3│ Anexo3   │
└──────┴──────────────────────┴──────────────┴──────────────────┴──────────────┴──────────┘
```

---

## 🔍 ¿CÓMO SABE DOCXTPL DÓNDE CONSTRUIR LA TABLA?

docxtpl **NO** busca tablas por nombre. En su lugar:

1. **Analiza el XML interno** del documento Word
2. **Detecta cuando un loop `{% for %}` está dentro de una fila de tabla** (elemento `<w:tr>` en el XML)
3. **Replica automáticamente esa fila** para cada elemento en la lista

**Por eso es importante:**
- ✅ Poner el loop en una **fila de datos** (no en el encabezado)
- ✅ Cerrar el loop con `{% endfor %}` en la misma fila
- ✅ La tabla debe estar creada en Word (no solo texto con `|`)

Para más detalles, consulta: **`COMO_FUNCIONA_DETECCION_TABLAS.md`**

---

## 🔧 TROUBLESHOOTING

### Problema: La tabla no se genera

**Solución:**
- Verifica que el loop esté correctamente cerrado con `{% endfor %}`
- Asegúrate de que `tabla_obligaciones_generales` esté en el contexto del generador
- Revisa que los nombres de las variables coincidan exactamente
- **Verifica que el loop esté dentro de una fila de tabla real en Word** (no solo texto)

### Problema: Solo se genera una fila

**Solución:**
- Verifica que `tabla_obligaciones_generales` sea una lista con múltiples elementos
- Revisa los logs del generador para ver cuántas obligaciones se cargaron desde MongoDB
- Asegúrate de que el `{% for %}` y `{% endfor %}` estén en la misma fila

### Problema: El formato no se mantiene

**Solución:**
- Asegúrate de aplicar el formato a la fila 2 (la que contiene el loop)
- docxtpl copia el formato de la fila que contiene el loop

---

## 📚 REFERENCIA RÁPIDA

**Sintaxis básica:**
```jinja2
{% for item in lista %}
{{ item.campo1 }} | {{ item.campo2 }} | {{ item.campo3 }}
{% endfor %}
```

**Con condicional:**
```jinja2
{% if lista %}
{% for item in lista %}
{{ item.campo1 }} | {{ item.campo2 }}
{% endfor %}
{% else %}
No hay datos disponibles.
{% endif %}
```

---

## 🎨 FORMATO ADICIONAL

Si quieres aplicar formato condicional (ej: color rojo si no cumplió):

```jinja2
{% for obligacion in tabla_obligaciones_generales %}
{{ obligacion.item }} | {{ obligacion.obligacion }} | {{ obligacion.periodicidad }} | 
{% if obligacion.cumplio == "No Cumplió" %}
🔴 {{ obligacion.cumplio }}
{% else %}
✅ {{ obligacion.cumplio }}
{% endif %}
| {{ obligacion.observaciones }} | {{ obligacion.anexo }}
{% endfor %}
```

**Nota:** El formato condicional de colores requiere usar RichText de docxtpl, lo cual es más avanzado. Por ahora, usa el formato básico.

