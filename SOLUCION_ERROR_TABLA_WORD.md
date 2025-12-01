# 🔧 SOLUCIÓN: Error al Abrir Archivo Word Generado

## 🐛 Problema

Cuando generas el documento Word usando el template con loops de Jinja2, el archivo generado tiene errores al abrirlo en Word.

## 🔍 Causas Posibles

### 1. **Conflicto entre Jinja2 y Reemplazo Programático**

El código actual está haciendo **dos cosas a la vez**:
- Primero: docxtpl renderiza el template con Jinja2 (genera las filas de la tabla)
- Segundo: `_reemplazar_tabla_obligaciones_generales()` intenta manipular la tabla programáticamente

Esto puede corromper el XML del documento.

### 2. **Espacios o Saltos de Línea en las Celdas**

Word puede agregar espacios o saltos de línea invisibles en las celdas que rompen el XML cuando docxtpl procesa el template.

### 3. **Formato Incorrecto del Template**

El loop `{% for %}` y `{% endfor %}` deben estar exactamente en las celdas correctas, sin espacios extra.

---

## ✅ SOLUCIONES

### Solución 1: Deshabilitar Reemplazo Programático (RECOMENDADO)

Si usas Jinja2 directamente en el template, **NO** debes usar el reemplazo programático.

**Modifica el método `generar()` en `seccion_1_info_general.py`:**

```python
def generar(self):
    """
    Genera la sección completa usando Jinja2 directamente
    """
    # Generar el documento base usando el método de la clase padre
    doc_template = super().generar()
    
    # Si usas Jinja2 en el template, NO llames a los métodos de reemplazo programático
    # doc = doc_template.docx
    # self._reemplazar_tabla_obligaciones_generales(doc)  # ← COMENTAR ESTO
    # self._reemplazar_tabla_obligaciones_especificas(doc)  # ← COMENTAR ESTO
    
    return doc_template
```

### Solución 2: Corregir el Template en Word

**Pasos para corregir el template:**

1. **Abre el template en Word**
2. **Selecciona la fila 2 (la que tiene el loop)**
3. **Presiona Ctrl+H (Buscar y Reemplazar)**
4. **Busca espacios dobles o saltos de línea** y reemplázalos
5. **Asegúrate de que cada celda tenga exactamente:**

   **Celda 1:**
   ```
   {% for obligacion in tabla_obligaciones_generales %}
   ```
   (Sin espacios al inicio o final)

   **Celda 2:**
   ```
   {{ obligacion.item }}
   ```
   (Sin espacios extra)

   **Celda 3:**
   ```
   {{ obligacion.obligacion }}
   ```

   **Celda 4:**
   ```
   {{ obligacion.periodicidad }}
   ```

   **Celda 5:**
   ```
   {{ obligacion.cumplio }}
   ```

   **Celda 6:**
   ```
   {{ obligacion.observaciones }}
   ```

   **Celda 7:**
   ```
   {{ obligacion.anexo }}
   {% endfor %}
   ```
   (El `{% endfor %}` debe estar en la última celda, sin espacios)

6. **Guarda el template**

### Solución 3: Usar Método Alternativo (Sin Jinja2 en Tablas)

Si prefieres mantener el reemplazo programático, **NO** uses loops de Jinja2 en las tablas. En su lugar:

1. **En el template, deja la tabla vacía** (solo encabezados)
2. **El código programático la llenará automáticamente**

---

## 🔧 IMPLEMENTACIÓN RÁPIDA

### Opción A: Solo Jinja2 (Sin código programático)

1. **Modifica `seccion_1_info_general.py`:**

```python
def generar(self):
    """Genera la sección completa usando solo Jinja2"""
    doc_template = super().generar()
    # NO llamar a _reemplazar_tabla_obligaciones_generales
    return doc_template
```

2. **Asegúrate de que el template tenga el loop correctamente formateado**

### Opción B: Solo Reemplazo Programático (Sin Jinja2 en tablas)

1. **En el template, deja las tablas vacías** (solo encabezados)
2. **Mantén el código actual** que usa `_reemplazar_tabla_obligaciones_generales`

---

## 🧪 VERIFICACIÓN

Después de aplicar la solución:

1. **Genera el documento:**
   ```bash
   POST /api/seccion1/generar
   {
     "anio": 2025,
     "mes": 9
   }
   ```

2. **Abre el archivo generado en Word**
3. **Verifica que:**
   - ✅ El archivo se abre sin errores
   - ✅ Las tablas tienen las filas correctas
   - ✅ Los datos están completos

---

## 📝 CHECKLIST DE CORRECCIÓN

- [ ] El loop `{% for %}` está en la primera celda de la fila de datos
- [ ] El `{% endfor %}` está en la última celda de la misma fila
- [ ] No hay espacios extra al inicio o final de las celdas
- [ ] No hay saltos de línea dentro de las celdas (excepto donde sea necesario)
- [ ] El método `generar()` NO llama a `_reemplazar_tabla_*` si usas Jinja2
- [ ] El template está guardado correctamente

---

## 🚨 ERRORES COMUNES

### Error: "El archivo está dañado"

**Causa:** Conflicto entre Jinja2 y reemplazo programático

**Solución:** Deshabilita el reemplazo programático (Solución 1)

### Error: "No se puede leer el contenido"

**Causa:** Espacios o caracteres especiales en las celdas

**Solución:** Limpia el template (Solución 2)

### Error: "Formato no reconocido"

**Causa:** Template corrupto o mal formateado

**Solución:** Recrea la tabla desde cero en Word

