# INSTRUCCIONES PARA EDITAR EL TEMPLATE DE LA SECCIÓN 1

## 📋 CONTEXTO

El template `templates/seccion_1_info_general.docx` ha sido copiado desde el documento de referencia `data/segmentos/Seccion 1.docx`.

Ahora necesitas editarlo manualmente en Microsoft Word para agregar las variables Jinja2 en los lugares dinámicos.

---

## 🎯 OBJETIVO

Reemplazar los valores estáticos con variables Jinja2 (`{{ variable }}` y `{% for %}`) para que el generador pueda llenar automáticamente el documento cada mes.

---

## 📝 PASOS PARA EDITAR EL TEMPLATE

### 1. Abrir el Template

Abre el archivo `templates/seccion_1_info_general.docx` en Microsoft Word.

### 2. Reemplazar Texto Introductorio

**Buscar:**
```
Se celebra el número de proceso SECOP II SCJ-SIF-CD-480-2024 bajo número de contrato SCJ-1809-2024 con vigencia de doce (12) meses luego de suscripción de acta de inicio suscrita el 19 de noviembre de 2024...
```

**Reemplazar con:**
```
{{ texto_intro }}
```

---

### 3. Tabla 1: Información General del Contrato

**Estructura:** 17 filas x 4 columnas (formato Campo | Valor)

**En la primera fila de datos (fila 2), reemplazar:**

**Columna 1 (Campo):** Mantener "NIT"
**Columna 2 (Valor):** Reemplazar con `{{ tabla_1_filas[0].valor }}`

**Para las siguientes filas, usar:**
- Fila 3: `{{ tabla_1_filas[1].campo }}` | `{{ tabla_1_filas[1].valor }}`
- Fila 4: `{{ tabla_1_filas[2].campo }}` | `{{ tabla_1_filas[2].valor }}`
- ... y así sucesivamente

**O mejor aún, usar un loop:**
```
{% for fila in tabla_1_filas %}
{{ fila.campo }} | {{ fila.valor }}
{% endfor %}
```

**Nota:** En Word, debes insertar esto en las celdas de la tabla. Para cada fila de datos, reemplaza el contenido de las celdas con las variables.

---

### 4. Textos sobre Anexos (Opcionales)

**Buscar y reemplazar:**

- Ruta acta inicio: `{{ ruta_acta_inicio }}`
- Número adición: `{{ numero_adicion }}`
- Ruta póliza: `{{ ruta_poliza }}`

**Si no aplica en algún mes, usar condicional:**
```
{% if numero_adicion %}
Se presenta ADICIÓN Nro. {{ numero_adicion }} AL CONTRATO...
{% endif %}
```

---

### 5. Objeto del Contrato

**Buscar:** El texto del objeto completo
**Reemplazar con:** `{{ objeto_contrato }}`

---

### 6. Alcance

**Buscar:** El texto completo del alcance
**Reemplazar con:** `{{ alcance }}`

**Nota:** Este es texto fijo que se carga desde `data/fijos/alcance.txt`

---

### 7. Tabla 2: Componentes por Subsistema

**Estructura:** 9 filas x 6 columnas

**Encabezados:** Mantener como están
**Filas de datos:** Reemplazar con loop

**En la primera fila de datos (fila 2), insertar en cada celda:**
```
{% for comp in componentes %}
{{ comp.numero }} | {{ comp.sistema }} | {{ comp.ubicaciones }} | {{ comp.puntos_camara }} | {{ comp.centros_monitoreo_c4 }} | {{ comp.visualizadas_localmente }}
{% endfor %}
```

**Nota:** En Word, esto se hace fila por fila. Para cada fila de datos, reemplaza el contenido con las variables correspondientes.

---

### 8. Tabla 3: Centros de Monitoreo

**Estructura:** 12 filas x 4 columnas

**Encabezados:** Mantener como están
**Filas de datos:** Reemplazar con loop

```
{% for centro in centros %}
{{ centro.numero }} | {{ centro.nombre }} | {{ centro.direccion }} | {{ centro.localidad }}
{% endfor %}
```

---

### 9. Tabla 4: Forma de Pago

**Estructura:** 4 filas x 3 columnas

**Encabezados:** Mantener como están
**Filas de datos:** Reemplazar con loop

```
{% for pago in forma_pago %}
{{ pago.numero }} | {{ pago.descripcion }} | {{ pago.tipo_servicio }}
{% endfor %}
```

---

### 10. Glosario

**Estructura:** Múltiples tablas (aproximadamente tablas 23-31)

**Cada tabla tiene:** Término | Definición

**Para cada tabla de glosario, usar:**
```
{% for termino in glosario %}
{{ termino.termino }} | {{ termino.definicion }}
{% endfor %}
```

**Nota:** El glosario se divide en múltiples tablas. Puedes usar un loop que itere sobre `glosario` y crear una tabla por cada término, o agruparlos.

---

### 11. Tablas de Obligaciones

**Estructura:** Variable (4-8 filas) x 6 columnas
**Columnas:** ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ/NO CUMPLIÓ | OBSERVACIONES | ANEXO

**Para cada tabla de obligaciones, usar:**
```
{% for oblig in tabla_obligaciones_generales %}
{{ oblig.item }} | {{ oblig.obligacion }} | {{ oblig.periodicidad }} | {{ oblig.cumplio }} | {{ oblig.observaciones }} | {{ oblig.anexo }}
{% endfor %}
```

**Aplicar a:**
- `tabla_obligaciones_generales`
- `tabla_obligaciones_especificas`
- `tabla_obligaciones_ambientales`
- `tabla_obligaciones_anexos`

**Nota:** Si una lista está vacía, docxtpl no generará filas. Puedes usar condicionales:
```
{% if tabla_obligaciones_generales %}
{% for oblig in tabla_obligaciones_generales %}
...
{% endfor %}
{% else %}
No se registran obligaciones para el periodo.
{% endif %}
```

---

### 12. Tablas de Comunicados

**Estructura:** Variable (25-40 filas) x 4 columnas
**Columnas:** ÍTEM | FECHA | CONSECUTIVO ETB | DESCRIPCIÓN

**Comunicados Emitidos:**
```
{% for com in tabla_comunicados_emitidos %}
{{ com.item }} | {{ com.fecha }} | {{ com.consecutivo }} | {{ com.descripcion }}
{% endfor %}
```

**Comunicados Recibidos:**
```
{% for com in tabla_comunicados_recibidos %}
{{ com.item }} | {{ com.fecha }} | {{ com.consecutivo }} | {{ com.descripcion }}
{% endfor %}
```

---

### 13. Tablas de Personal

**Personal Mínimo:**
```
{% for p in tabla_personal_minimo %}
{{ p.cargo }} | {{ p.cantidad }} | {{ p.nombre }}
{% endfor %}
```

**Personal de Apoyo:**
```
{% for p in tabla_personal_apoyo %}
{{ p.cargo }} | {{ p.cantidad }} | {{ p.nombre }}
{% endfor %}
```

---

## ⚠️ IMPORTANTE: CÓMO USAR LOOPS EN TABLAS DE WORD

### Método 1: Loop en Primera Fila de Datos

1. Selecciona la primera fila de datos (después del encabezado)
2. En cada celda, reemplaza el contenido con la variable correspondiente
3. Usa `{% for %}` en la primera celda de la fila
4. Usa `{% endfor %}` en la última celda de la fila

**Ejemplo para Tabla de Componentes:**

**Fila 2, Celda 1:** `{% for comp in componentes %}`
**Fila 2, Celda 2:** `{{ comp.numero }}`
**Fila 2, Celda 3:** `{{ comp.sistema }}`
**Fila 2, Celda 4:** `{{ comp.ubicaciones }}`
**Fila 2, Celda 5:** `{{ comp.puntos_camara }}`
**Fila 2, Celda 6:** `{{ comp.centros_monitoreo_c4 }}`
**Fila 2, Celda 7:** `{{ comp.visualizadas_localmente }}{% endfor %}`

**Eliminar las filas de datos restantes** - docxtpl las generará automáticamente.

### Método 2: Usar Sintaxis `{% tbl_nombre %}` (si docxtpl lo soporta)

Algunas versiones de docxtpl soportan:
```
{% tbl_componentes %}
{% for comp in componentes %}
{{ comp.numero }} | {{ comp.sistema }} | ...
{% endfor %}
{% endtbl_componentes %}
```

---

## ✅ CHECKLIST DE EDICIÓN

- [ ] Texto introductorio reemplazado con `{{ texto_intro }}`
- [ ] Tabla 1: Valores reemplazados con variables o loop
- [ ] Textos de anexos reemplazados con variables (si aplican)
- [ ] Objeto del contrato reemplazado con `{{ objeto_contrato }}`
- [ ] Alcance reemplazado con `{{ alcance }}`
- [ ] Tabla 2 (Componentes): Loop agregado
- [ ] Tabla 3 (Centros): Loop agregado
- [ ] Tabla 4 (Forma de pago): Loop agregado
- [ ] Glosario: Loops agregados en cada tabla
- [ ] Tablas de obligaciones: Loops agregados
- [ ] Tablas de comunicados: Loops agregados
- [ ] Tablas de personal: Loops agregados
- [ ] Guardar el template

---

## 🧪 PROBAR EL TEMPLATE

Después de editar, prueba con:

```python
from src.generadores.seccion_1_info_general import GeneradorSeccion1
from pathlib import Path

gen = GeneradorSeccion1(anio=2025, mes=9)
gen.cargar_datos()
gen.guardar(Path("output/test/seccion_1_test.docx"))
```

---

## 📚 REFERENCIA DE VARIABLES DISPONIBLES

### Variables de Texto
- `{{ texto_intro }}` - Texto introductorio completo
- `{{ objeto_contrato }}` - Objeto del contrato
- `{{ alcance }}` - Texto del alcance
- `{{ descripcion_infraestructura }}` - Descripción de infraestructura
- `{{ obligaciones_generales }}` - Texto de obligaciones generales
- `{{ obligaciones_especificas }}` - Texto de obligaciones específicas
- `{{ obligaciones_ambientales }}` - Texto de obligaciones ambientales
- `{{ obligaciones_anexos }}` - Texto de obligaciones anexos

### Variables de Tablas (Listas)
- `{{ tabla_1_filas }}` - Lista de filas para Tabla 1
- `{{ componentes }}` - Lista de componentes por subsistema
- `{{ centros }}` - Lista de centros de monitoreo
- `{{ forma_pago }}` - Lista de formas de pago
- `{{ glosario }}` - Lista de términos del glosario
- `{{ tabla_obligaciones_generales }}` - Lista de obligaciones generales
- `{{ tabla_obligaciones_especificas }}` - Lista de obligaciones específicas
- `{{ tabla_obligaciones_ambientales }}` - Lista de obligaciones ambientales
- `{{ tabla_obligaciones_anexos }}` - Lista de obligaciones anexos
- `{{ tabla_comunicados_emitidos }}` - Lista de comunicados emitidos
- `{{ tabla_comunicados_recibidos }}` - Lista de comunicados recibidos
- `{{ tabla_personal_minimo }}` - Lista de personal mínimo
- `{{ tabla_personal_apoyo }}` - Lista de personal de apoyo

### Variables Opcionales
- `{{ ruta_acta_inicio }}` - Ruta del acta de inicio
- `{{ numero_adicion }}` - Número de adición
- `{{ ruta_poliza }}` - Ruta de modificación de póliza
- `{{ nota_infraestructura }}` - Nota adicional sobre infraestructura

---

## 🔍 ESTRUCTURA DE DATOS

### Tabla 1 (tabla_1_filas)
```python
[
    {"campo": "NIT", "valor": "899.999.115-8"},
    {"campo": "RAZÓN SOCIAL", "valor": "EMPRESA DE TELECOMUNICACIONES..."},
    # ...
]
```

### Componentes
```python
[
    {"numero": 1, "sistema": "CIUDADANA", "ubicaciones": 4451, ...},
    # ...
]
```

### Comunicados
```python
[
    {"item": 1, "fecha": "09/09/2025", "consecutivo": "VVG-CCS-ETB-751-25", "descripcion": "..."},
    # ...
]
```

### Obligaciones
```python
[
    {"item": 1, "obligacion": "...", "periodicidad": "Permanente", "cumplio": "Cumplió", "observaciones": "...", "anexo": "..."},
    # ...
]
```

---

## 💡 TIPS

1. **Guardar copia de seguridad** antes de editar
2. **Probar con datos pequeños** primero
3. **Verificar sintaxis Jinja2** - debe ser exacta
4. **No eliminar encabezados** de las tablas
5. **Mantener formato** de Word (estilos, colores, etc.)
6. **Usar condicionales** para contenido opcional: `{% if variable %}...{% endif %}`

---

## 🚨 PROBLEMAS COMUNES

### Error: Variable no definida
- Verificar que el nombre de la variable coincida exactamente
- Revisar el método `procesar()` del generador

### Tabla no se genera
- Verificar que el loop esté correctamente en la primera fila de datos
- Asegurarse de que la lista no esté vacía

### Formato incorrecto
- Los estilos de Word se mantienen, solo se reemplaza el contenido
- Verificar que los estilos estén aplicados correctamente en el template

---

**¡Listo! Una vez editado el template, el generador podrá llenar automáticamente todos los datos dinámicos cada mes.**

