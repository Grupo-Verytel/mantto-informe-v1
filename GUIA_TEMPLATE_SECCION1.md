# GUÍA: CONFIGURACIÓN DEL TEMPLATE DE SECCIÓN 1

## 📋 OBJETIVO

Configurar el template `seccion_1_info_general.docx` para que use Jinja2 (docxtpl) y cargue datos dinámicos desde MongoDB y variables estáticas desde `config.py`.

---

## 🔧 VARIABLES DISPONIBLES EN EL TEMPLATE

### Variables Simples (desde config.py)

Estas variables vienen del archivo `config.py` y se pueden usar directamente en el template:

```jinja2
{{ contrato_numero }}          # Número del contrato
{{ entidad }}                  # Nombre completo de la entidad
{{ entidad_corto }}            # Nombre corto de la entidad
{{ periodo }}                 # "Septiembre de 2025"
{{ mes }}                     # "Septiembre"
{{ anio }}                     # 2025
{{ mes_numero }}               # 9

{{ texto_intro }}              # Texto introductorio del contrato

{{ objeto_contrato }}          # Objeto del contrato (corto)
{{ alcance }}                  # Texto del alcance
{{ descripcion_infraestructura }}  # Descripción de infraestructura

{{ obligaciones_generales }}   # Texto introductorio de obligaciones generales
{{ obligaciones_especificas }} # Texto introductorio de obligaciones específicas
{{ obligaciones_ambientales }} # Texto introductorio de obligaciones ambientales
{{ obligaciones_anexos }}      # Texto introductorio de obligaciones anexos

{{ ruta_acta_inicio }}         # Ruta del acta de inicio
{{ numero_adicion }}           # Número de adición
{{ ruta_poliza }}              # Ruta de la póliza
{{ nota_infraestructura }}      # Nota adicional sobre infraestructura
```

### Tabla 1: Información General del Contrato

**Opción 1: Usar objeto con campos individuales**
```jinja2
{{ tabla_1_info_general.nit }}
{{ tabla_1_info_general.razon_social }}
{{ tabla_1_info_general.ciudad }}
{{ tabla_1_info_general.direccion }}
{{ tabla_1_info_general.telefono }}
{{ tabla_1_info_general.numero_contrato }}
{{ tabla_1_info_general.fecha_inicio }}
{{ tabla_1_info_general.plazo_ejecucion }}
{{ tabla_1_info_general.fecha_terminacion }}
{{ tabla_1_info_general.valor_inicial }}
{{ tabla_1_info_general.adicion_1 }}
{{ tabla_1_info_general.valor_total }}
{{ tabla_1_info_general.objeto }}
{{ tabla_1_info_general.fecha_firma_acta }}
{{ tabla_1_info_general.fecha_suscripcion }}
{{ tabla_1_info_general.vigencia_poliza_inicial }}
{{ tabla_1_info_general.vigencia_poliza_acta }}
```

**Opción 2: Usar lista de filas (Campo | Valor)**
```jinja2
{% for fila in tabla_1_filas %}
{{ fila.campo }}: {{ fila.valor }}
{% endfor %}
```

### Tablas Dinámicas (desde MongoDB)

#### Tabla de Obligaciones Generales (1.5.1)

```jinja2
{% for obligacion in tabla_obligaciones_generales %}
{{ obligacion.item }} | {{ obligacion.obligacion }} | {{ obligacion.periodicidad }} | {{ obligacion.cumplio }} | {{ obligacion.observaciones }} | {{ obligacion.anexo }}
{% endfor %}
```

**Campos disponibles:**
- `item`: Número de ítem
- `obligacion`: Texto de la obligación
- `periodicidad`: Periodicidad (Permanente, Mensual, etc.)
- `cumplio`: "Cumplió" o "No Cumplió"
- `observaciones`: Observaciones generadas (pueden venir de LLM)
- `anexo`: Ruta del anexo

#### Tabla de Obligaciones Específicas (1.5.2)

```jinja2
{% for obligacion in tabla_obligaciones_especificas %}
{{ obligacion.item }} | {{ obligacion.obligacion }} | {{ obligacion.periodicidad }} | {{ obligacion.cumplio }} | {{ obligacion.observaciones }} | {{ obligacion.anexo }}
{% endfor %}
```

#### Tabla de Obligaciones Ambientales (1.5.3)

```jinja2
{% for obligacion in tabla_obligaciones_ambientales %}
{{ obligacion.item }} | {{ obligacion.obligacion }} | {{ obligacion.periodicidad }} | {{ obligacion.cumplio }} | {{ obligacion.observaciones }} | {{ obligacion.anexo }}
{% endfor %}
```

#### Tabla de Obligaciones Anexos (1.5.4)

```jinja2
{% for obligacion in tabla_obligaciones_anexos %}
{{ obligacion.item }} | {{ obligacion.obligacion }} | {{ obligacion.periodicidad }} | {{ obligacion.cumplio }} | {{ obligacion.observaciones }} | {{ obligacion.anexo }}
{% endfor %}
```

**Nota:** Para 1.5.4, el formato puede ser diferente:
```jinja2
{% for anexo in tabla_obligaciones_anexos %}
{{ anexo.item }} | {{ anexo.archivo_existe }} | {{ anexo.anexo }}
{% endfor %}
```

#### Tabla de Comunicados Emitidos (1.6.1)

```jinja2
{% for comunicado in tabla_comunicados_emitidos %}
{{ comunicado.item }} | {{ comunicado.fecha }} | {{ comunicado.consecutivo }} | {{ comunicado.descripcion }}
{% endfor %}
```

**Campos disponibles:**
- `item`: Número de ítem (consecutivo)
- `fecha`: Fecha del comunicado (DD/MM/YYYY)
- `consecutivo`: Radicado o número del comunicado
- `descripcion`: Asunto del comunicado

#### Tabla de Comunicados Recibidos (1.6.2)

```jinja2
{% for comunicado in tabla_comunicados_recibidos %}
{{ comunicado.item }} | {{ comunicado.fecha }} | {{ comunicado.consecutivo }} | {{ comunicado.descripcion }}
{% endfor %}
```

### Otras Tablas (desde config.py)

#### Tabla de Componentes

```jinja2
{% for componente in tabla_componentes %}
{{ componente.numero }} | {{ componente.sistema }} | {{ componente.ubicaciones }} | {{ componente.puntos_camara }} | {{ componente.centros_monitoreo_c4 }} | {{ componente.visualizadas_localmente }}
{% endfor %}
```

#### Tabla de Centros de Monitoreo

```jinja2
{% for centro in tabla_centros_monitoreo %}
{{ centro.numero }} | {{ centro.nombre }} | {{ centro.direccion }} | {{ centro.localidad }}
{% endfor %}
```

#### Tabla de Forma de Pago

```jinja2
{% for pago in tabla_forma_pago %}
{{ pago.numero }} | {{ pago.descripcion }} | {{ pago.tipo_servicio }}
{% endfor %}
```

#### Tabla de Personal Mínimo

```jinja2
{% for personal in tabla_personal_minimo %}
{{ personal.cargo }} | {{ personal.cantidad }} | {{ personal.nombre }}
{% endfor %}
```

#### Tabla de Personal de Apoyo

```jinja2
{% for personal in tabla_personal_apoyo %}
{{ personal.cargo }} | {{ personal.cantidad }} | {{ personal.nombre }}
{% endfor %}
```

#### Tabla de Glosario

```jinja2
{% for termino in glosario_tablas %}
{{ termino.termino }} | {{ termino.definicion }}
{% endfor %}
```

---

## 📝 EJEMPLO DE USO EN TEMPLATE

### Ejemplo 1: Variable Simple

```jinja2
El contrato {{ contrato_numero }} tiene vigencia desde {{ fecha_inicio }} hasta {{ fecha_terminacion }}.
```

### Ejemplo 2: Tabla Dinámica

En el template Word, crea una tabla con encabezados y luego usa:

```jinja2
{% for obligacion in tabla_obligaciones_generales %}
{{ obligacion.item }} | {{ obligacion.obligacion }} | {{ obligacion.periodicidad }} | {{ obligacion.cumplio }} | {{ obligacion.observaciones }} | {{ obligacion.anexo }}
{% endfor %}
```

**Nota:** En docxtpl, para tablas dinámicas, generalmente se usa el método de reemplazo programático (como se hace en `_reemplazar_tabla_obligaciones_generales`), pero también puedes usar loops de Jinja2 si el template está configurado correctamente.

---

## 🔄 FLUJO DE DATOS

1. **Variables Simples**: Se cargan desde `config.py` → `GeneradorSeccion1.procesar()` → Template
2. **Tablas Dinámicas**: Se cargan desde MongoDB → `Seccion1Service.cargar_datos_desde_mongodb()` → `GeneradorSeccion1` → Template

---

## 📊 ESTRUCTURA DE DATOS EN MONGODB

### Colección: `obligaciones`

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "obligaciones_generales": [
    {
      "item": 1,
      "obligacion": "...",
      "periodicidad": "...",
      "cumplio": "...",
      "observaciones": "...",
      "anexo": "..."
    }
  ],
  "obligaciones_especificas": [...],
  "obligaciones_ambientales": [...],
  "obligaciones_anexos": [...]
}
```

### Colección: `comunicados`

```json
{
  "anio": 2025,
  "mes": 9,
  "seccion": 1,
  "subseccion": "1.6.1",
  "comunicados_emitidos": [
    {
      "item": 1,
      "radicado": "GSC-7444-2025",
      "fecha": "23/09/2025",
      "asunto": "...",
      "nombre_archivo": "..."
    }
  ]
}
```

---

## ✅ CHECKLIST PARA CONFIGURAR EL TEMPLATE

- [ ] Variables simples están definidas en `config.py`
- [ ] Tablas dinámicas están guardadas en MongoDB
- [ ] El template usa sintaxis Jinja2 correcta
- [ ] Los nombres de variables coinciden con los del generador
- [ ] Las tablas en el template tienen el formato correcto

---

## 🚀 USO DEL ENDPOINT

```bash
POST /api/seccion1/generar
Content-Type: application/json

{
  "anio": 2025,
  "mes": 9,
  "usar_llm_observaciones": false,
  "output_path": "ruta/opcional/archivo.docx"
}
```

El sistema:
1. Carga variables desde `config.py`
2. Consulta MongoDB para obtener tablas dinámicas
3. Genera el documento Word usando el template
4. Retorna la ruta del archivo generado

