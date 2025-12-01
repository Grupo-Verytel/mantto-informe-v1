# 🔍 CÓMO SABE JINJA2/DOCXTPL DÓNDE CONSTRUIR LA TABLA

## 📋 Explicación Técnica

docxtpl **NO** busca tablas por nombre o ubicación. En su lugar, **analiza la estructura XML interna del documento Word** y detecta automáticamente cuando un loop `{% for %}` está dentro de una fila de tabla.

---

## 🔬 MECANISMO DE DETECCIÓN

### 1. Estructura XML de Word

Un documento Word (.docx) es en realidad un archivo ZIP que contiene XML. Cuando creas una tabla en Word, internamente se representa así:

```xml
<w:tbl>  <!-- Inicio de tabla -->
  <w:tr>  <!-- Fila 1: Encabezado -->
    <w:tc>  <!-- Celda 1 -->
      <w:p><w:r><w:t>ÍTEM</w:t></w:r></w:p>
    </w:tc>
    <w:tc>  <!-- Celda 2 -->
      <w:p><w:r><w:t>OBLIGACIÓN</w:t></w:r></w:p>
    </w:tc>
    <!-- ... más celdas ... -->
  </w:tr>
  
  <w:tr>  <!-- Fila 2: Datos (con loop) -->
    <w:tc>
      <w:p><w:r><w:t>{% for obligacion in tabla_obligaciones_generales %}</w:t></w:r></w:p>
    </w:tc>
    <w:tc>
      <w:p><w:r><w:t>{{ obligacion.item }}</w:t></w:r></w:p>
    </w:tc>
    <!-- ... más celdas ... -->
    <w:tc>
      <w:p><w:r><w:t>{% endfor %}</w:t></w:r></w:p>
    </w:tc>
  </w:tr>
</w:tbl>  <!-- Fin de tabla -->
```

### 2. Proceso de Detección de docxtpl

Cuando ejecutas `doc.render(contexto)`, docxtpl:

1. **Descomprime el .docx** y lee el XML interno
2. **Analiza cada elemento** del documento (párrafos, tablas, imágenes, etc.)
3. **Detecta tags de Jinja2** (`{% for %}`, `{{ variable }}`, etc.)
4. **Verifica el contexto XML**: Si encuentra un `{% for %}` dentro de un elemento `<w:tr>` (fila de tabla), **sabe que debe replicar esa fila**
5. **Replica la fila** para cada elemento en la lista, manteniendo:
   - El formato de la fila original
   - La estructura de celdas
   - Los estilos aplicados

---

## 🎯 EJEMPLO VISUAL

### En el Template Word (lo que ves):

```
┌──────┬──────────────────────┬──────────────┬──────────────────┐
│ ÍTEM │ OBLIGACIÓN          │ PERIODICIDAD │ CUMPLIÓ         │
├──────┼──────────────────────┼──────────────┼──────────────────┤
│ {%   │ {{ obligacion.      │ {{ obligacion│ {{ obligacion.  │
│ for  │ item }}             │ .periodicidad│ cumplio }}      │
│ ...  │                     │ }}           │                 │
│ end  │                     │              │                 │
│ for  │                     │              │                 │
└──────┴──────────────────────┴──────────────┴──────────────────┘
```

### Lo que docxtpl "ve" en el XML:

```xml
<w:tbl>  <!-- ← docxtpl detecta: "Esto es una tabla" -->
  <w:tr>  <!-- Fila 1: Encabezado (no se toca) -->
    ...
  </w:tr>
  <w:tr>  <!-- ← docxtpl detecta: "Esto es una fila de tabla" -->
    <w:tc>
      <w:p><w:r><w:t>{% for obligacion in tabla_obligaciones_generales %}</w:t></w:r></w:p>
      <!-- ↑ docxtpl detecta: "Hay un loop dentro de una fila de tabla" -->
    </w:tc>
    <w:tc>
      <w:p><w:r><w:t>{{ obligacion.item }}</w:t></w:r></w:p>
    </w:tc>
    <!-- ... más celdas ... -->
    <w:tc>
      <w:p><w:r><w:t>{% endfor %}</w:t></w:r></w:p>
    </w:tc>
  </w:tr>
</w:tbl>
```

### Resultado después de `doc.render()`:

```xml
<w:tbl>
  <w:tr>  <!-- Encabezado (sin cambios) -->
    ...
  </w:tr>
  <w:tr>  <!-- Fila 1: Obligación 1 (replicada) -->
    <w:tc><w:p><w:r><w:t>1</w:t></w:r></w:p></w:tc>
    <w:tc><w:p><w:r><w:t>Texto obligación 1</w:t></w:r></w:p></w:tc>
    ...
  </w:tr>
  <w:tr>  <!-- Fila 2: Obligación 2 (replicada) -->
    <w:tc><w:p><w:r><w:t>2</w:t></w:r></w:p></w:tc>
    <w:tc><w:p><w:r><w:t>Texto obligación 2</w:t></w:r></w:p></w:tc>
    ...
  </w:tr>
  <!-- ... más filas replicadas ... -->
</w:tbl>
```

---

## ✅ REGLAS DE DETECCIÓN

docxtpl detecta que debe construir una tabla cuando:

1. ✅ Encuentra un `{% for %}` dentro de un elemento `<w:tr>` (fila de tabla)
2. ✅ El `{% endfor %}` está en la misma fila o en una celda posterior de la misma fila
3. ✅ La fila está dentro de un elemento `<w:tbl>` (tabla)

**NO funciona si:**
- ❌ El `{% for %}` está fuera de una tabla (en un párrafo normal)
- ❌ El `{% for %}` está en el encabezado de la tabla
- ❌ El `{% endfor %}` está en una fila diferente

---

## 🔧 POR QUÉ DEBES PONER EL LOOP EN UNA FILA DE DATOS

### ✅ CORRECTO:

```
Fila 1 (Encabezado): ÍTEM | OBLIGACIÓN | PERIODICIDAD
Fila 2 (Datos):      {% for ... %} | {{ item }} | {{ obligacion }} | ... | {% endfor %}
```

**docxtpl detecta:**
- "Hay un loop en la fila 2"
- "La fila 2 está dentro de una tabla"
- "Debo replicar la fila 2 para cada elemento"

### ❌ INCORRECTO:

```
Fila 1 (Encabezado): {% for ... %} ÍTEM | OBLIGACIÓN | PERIODICIDAD {% endfor %}
Fila 2 (Datos):      1 | Texto | Permanente
```

**docxtpl detecta:**
- "Hay un loop en la fila 1 (encabezado)"
- "No debo replicar encabezados"
- "Solo reemplazo las variables, no replico la fila"

---

## 📝 RESUMEN

**docxtpl sabe dónde construir la tabla porque:**

1. **Analiza el XML interno** del documento Word
2. **Detecta la estructura** `<w:tbl>` → `<w:tr>` → `<w:tc>`
3. **Encuentra el loop** `{% for %}` dentro de una fila de tabla
4. **Replica automáticamente** esa fila para cada elemento en la lista

**No necesitas:**
- ❌ Nombrar la tabla
- ❌ Usar IDs o marcadores especiales
- ❌ Indicar la ubicación manualmente

**Solo necesitas:**
- ✅ Crear la tabla en Word
- ✅ Poner el loop `{% for %}` en una fila de datos (no en el encabezado)
- ✅ Cerrar el loop con `{% endfor %}` en la misma fila

---

## 🎓 EJEMPLO COMPLETO

### Template Word:

```
1.5.1. OBLIGACIONES GENERALES

┌──────┬──────────────────────┬──────────────┬──────────────────┐
│ ÍTEM │ OBLIGACIÓN          │ PERIODICIDAD │ CUMPLIÓ         │
├──────┼──────────────────────┼──────────────┼──────────────────┤
│ {%   │ {{ obligacion.      │ {{ obligacion│ {{ obligacion.  │
│ for  │ item }}             │ .periodicidad│ cumplio }}      │
│ ...  │                     │ }}           │                 │
│ end  │                     │              │                 │
│ for  │                     │              │                 │
└──────┴──────────────────────┴──────────────┴──────────────────┘
```

### Código Python:

```python
from docxtpl import DocxTemplate

doc = DocxTemplate("template.docx")
contexto = {
    "tabla_obligaciones_generales": [
        {"item": 1, "obligacion": "Texto 1", "periodicidad": "Permanente", "cumplio": "Cumplió"},
        {"item": 2, "obligacion": "Texto 2", "periodicidad": "Mensual", "cumplio": "Cumplió"},
    ]
}
doc.render(contexto)
doc.save("output.docx")
```

### Resultado:

```
1.5.1. OBLIGACIONES GENERALES

┌──────┬──────────────────────┬──────────────┬──────────────────┐
│ ÍTEM │ OBLIGACIÓN          │ PERIODICIDAD │ CUMPLIÓ         │
├──────┼──────────────────────┼──────────────┼──────────────────┤
│ 1    │ Texto 1             │ Permanente   │ Cumplió         │
│ 2    │ Texto 2              │ Mensual      │ Cumplió         │
└──────┴──────────────────────┴──────────────┴──────────────────┘
```

**docxtpl automáticamente:**
- Detectó el loop en la fila de datos
- Replicó la fila 2 veces (una por cada obligación)
- Reemplazó las variables con los valores reales
- Mantuvo el formato de la fila original

