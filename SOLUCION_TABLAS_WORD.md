# ✅ SOLUCIÓN: Tablas en Word con docxtpl

## 🐛 Problema Identificado

Cuando colocas loops de Jinja2 (`{% for %}`) **dentro de las celdas de una tabla** en Word, el archivo generado se corrompe.

**Pero funciona bien cuando:**
- ✅ Las variables están fuera de tablas (texto normal)
- ✅ Las variables están una debajo de otra (párrafos normales)

## 🔍 Causa

docxtpl tiene problemas al procesar loops de Jinja2 dentro de la estructura XML compleja de las tablas de Word. Esto puede causar:
- Corrupción del XML interno
- Errores al abrir el archivo
- Pérdida de formato

## ✅ SOLUCIÓN: Enfoque Híbrido

He configurado el código para usar un **enfoque híbrido**:

### 1. **Jinja2 para Variables Simples** (fuera de tablas)
- Textos, números, fechas
- Variables individuales
- Funciona perfectamente ✅

### 2. **Reemplazo Programático para Tablas** (más robusto)
- Las tablas se llenan desde Python
- Evita problemas de corrupción del XML
- Más control y confiable ✅

---

## 📋 CÓMO CONFIGURAR EL TEMPLATE

### Para Variables Simples (fuera de tablas):

Puedes usar Jinja2 normalmente:

```
El contrato {{ contrato_numero }} tiene vigencia desde {{ fecha_inicio }}.
```

### Para Tablas:

**IMPORTANTE:** Las tablas deben tener **SOLO encabezados**, sin loops de Jinja2.

**Estructura correcta:**

```
┌──────┬──────────────────────┬──────────────┬──────────────────┬──────────────┬──────────┐
│ ÍTEM │ OBLIGACIÓN          │ PERIODICIDAD │ CUMPLIÓ         │ OBSERVACIONES│ ANEXO    │
├──────┼──────────────────────┼──────────────┼──────────────────┼──────────────┼──────────┤
│      │                      │              │                 │              │          │
└──────┴──────────────────────┴──────────────┴──────────────────┴──────────────┴──────────┘
```

**Solo encabezados, sin filas de datos. El código Python las llenará automáticamente.**

---

## 🔧 QUÉ HACE EL CÓDIGO

1. **Renderiza variables simples** con Jinja2 (textos, números, etc.)
2. **Detecta las tablas** en el documento
3. **Busca cada tabla** por su título (1.5.1, 1.5.2, 1.5.3, 1.5.4)
4. **Llena cada tabla** con datos de MongoDB programáticamente
5. **Mantiene el formato** de los encabezados

---

## 📝 PASOS PARA CONFIGURAR EL TEMPLATE

### Paso 1: Abrir el Template

1. Abre `templates/seccion_1_info_general.docx` en Word
2. Navega hasta cada tabla

### Paso 2: Configurar las Tablas

Para cada tabla (1.5.1, 1.5.2, 1.5.3, 1.5.4):

1. **Asegúrate de que tenga solo 1 fila: los encabezados**
2. **Elimina cualquier fila de datos** (incluyendo filas con loops de Jinja2)
3. **Elimina cualquier loop de Jinja2** de las celdas

**Estructura final:**

```
Fila 1: ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ / NO CUMPLIÓ | OBSERVACIONES | ANEXO
(No más filas)
```

### Paso 3: Guardar

1. Guarda el template (`Ctrl+S`)
2. Cierra Word

---

## ✅ VENTAJAS DE ESTE ENFOQUE

- ✅ **No corrompe el archivo**: El XML se mantiene intacto
- ✅ **Más robusto**: El código Python tiene mejor control sobre las tablas
- ✅ **Mejor formato**: Puedes aplicar formato específico a cada celda
- ✅ **Funciona siempre**: No depende de la sintaxis exacta de Jinja2 en tablas

---

## 🧪 PROBAR

1. **Configura el template** con solo encabezados en las tablas
2. **Genera el documento:**
   ```bash
   POST /api/seccion1/generar
   {
     "anio": 2025,
     "mes": 9
   }
   ```
3. **Abre el archivo generado** - debería abrirse sin errores
4. **Verifica que todas las tablas** se llenaron correctamente

---

## 📊 TABLAS QUE SE LLENAN AUTOMÁTICAMENTE

El código llena automáticamente estas tablas desde MongoDB:

- ✅ **1.5.1. OBLIGACIONES GENERALES** → `tabla_obligaciones_generales`
- ✅ **1.5.2. OBLIGACIONES ESPECÍFICAS** → `tabla_obligaciones_especificas`
- ✅ **1.5.3. OBLIGACIONES AMBIENTALES** → `tabla_obligaciones_ambientales`
- ✅ **1.5.4. OBLIGACIONES ANEXOS** → `tabla_obligaciones_anexos`

---

## 🚨 SI AÚN HAY PROBLEMAS

Si después de configurar el template con solo encabezados aún hay errores:

1. **Verifica que no haya loops de Jinja2** en ninguna celda de tabla
2. **Asegúrate de que cada tabla tenga solo 1 fila** (encabezados)
3. **Revisa los logs del servidor** para ver qué tabla no se encontró
4. **Prueba con un template limpio** (solo encabezados, sin ningún loop)

---

## 📝 RESUMEN

**NO uses:**
- ❌ Loops de Jinja2 dentro de celdas de tabla
- ❌ Variables de Jinja2 dentro de tablas (excepto en encabezados si es necesario)

**SÍ usa:**
- ✅ Variables de Jinja2 fuera de tablas (textos, números, etc.)
- ✅ Solo encabezados en las tablas
- ✅ El código Python llenará las tablas automáticamente

