# ANÁLISIS DE ESTRUCTURA - SECCIÓN 1

## 📋 ESTRUCTURA IDENTIFICADA DEL DOCUMENTO DE REFERENCIA

### TÍTULOS PRINCIPALES (Heading 1)

1. **INFORMACIÓN GENERAL DEL CONTRATO SCJ-1809-2024**
2. **OBJETO CONTRATO SCJ-1809-2024**
3. **ALCANCE**
4. **DESCRIPCIÓN DE LA INFRAESTRUCTURA DEL SISTEMA**
5. **GLOSARIO**
6. **OBLIGACIONES**
   - OBLIGACIONES GENERALES (Heading 2)
   - OBLIGACIONES ESPECÍFICAS DEL CONTRATISTA (Heading 2)
   - OBLIGACIONES ESPECÍFICAS EN MATERIA AMBIENTAL (Heading 2)
   - OBLIGACIONES ANEXOS (Heading 2)
7. **COMUNICADOS CONTRATO SCJ-1809-2024**
   - EMITIDOS CONTRATO SCJ-1809-2024 (Heading 2)
   - RECIBIDOS CONTRATO SCJ-1809-2024 (Heading 2)
8. **PERSONAL MÍNIMO REQUERIDO**
9. **PERSONAL DE APOYO**

---

## 🟦 CONTENIDO FIJO (NO CAMBIA ENTRE MESES)

### 1. Títulos y Subtítulos
- Todos los títulos de secciones y subsecciones
- Estructura jerárquica (Heading 1, Heading 2)

### 2. Textos Descriptivos
- **Alcance**: Texto completo del alcance del contrato
- **Descripción de Infraestructura**: Texto descriptivo del sistema
- **Obligaciones Generales**: Texto introductorio
- **Obligaciones Específicas**: Texto introductorio
- **Obligaciones Ambientales**: Texto introductorio
- **Obligaciones Anexos**: Texto introductorio

### 3. Estructura de Tablas
- Encabezados de todas las tablas
- Formato y estilo de tablas
- Columnas y estructura

### 4. Glosario
- Lista completa de términos y definiciones (puede ser fijo o actualizable)

---

## 🟩 CONTENIDO DINÁMICO (CAMBIA CADA MES)

### 1. Texto Introductorio
**Variable:** `{{ texto_intro }}`
**Formato:** "Se celebra el número de proceso {numero_proceso} bajo número de contrato {numero} con vigencia de doce (12) meses luego de suscripción de acta de inicio suscrita el {fecha_inicio}..."

### 2. Tabla 1: Información General del Contrato
**Estructura:** 17 filas x 4 columnas
**Formato:** Dos columnas (Campo | Valor)
**Datos dinámicos:**
- NIT, Razón Social, Ciudad, Dirección, Teléfono
- Número de contrato, Fechas, Plazo, Valores
- Objeto, Pólizas, etc.

### 3. Textos sobre Anexos (Opcionales)
**Variables:**
- `{{ ruta_acta_inicio }}` - Ruta del acta de inicio
- `{{ numero_adicion }}` - Número de adición (si aplica)
- `{{ ruta_poliza }}` - Ruta de modificación de póliza (si aplica)

### 4. Objeto del Contrato
**Variable:** `{{ objeto_contrato }}`
**Origen:** `config.CONTRATO["objeto_corto"]`

### 5. Tabla 2: Componentes por Subsistema
**Estructura:** 9 filas x 6 columnas
**Columnas:** N° | Sistema | Ubicaciones | Puntos Cámara | Centros Monitoreo C4 | Visualizadas Localmente
**Datos dinámicos:** Lista de componentes con cantidades

### 6. Tabla 3: Centros de Monitoreo
**Estructura:** 12 filas x 4 columnas
**Columnas:** N° | Centro de Monitoreo | Dirección | Localidad
**Datos dinámicos:** Lista de centros (puede ser fija o actualizable)

### 7. Tabla 4: Forma de Pago
**Estructura:** 4 filas x 3 columnas
**Columnas:** N° | Descripción Tipo Servicio | Característica
**Datos dinámicos:** Lista de formas de pago (puede ser fija)

### 8. Tablas de Glosario
**Estructura:** Múltiples tablas (aproximadamente 23-31)
**Columnas:** Término | Definición
**Datos dinámicos:** Lista de términos del glosario

### 9. Tablas de Obligaciones (Múltiples)
**Estructura:** Variable (4-8 filas) x 6 columnas
**Columnas:** ÍTEM | OBLIGACIÓN | PERIODICIDAD | CUMPLIÓ/NO CUMPLIÓ | OBSERVACIONES | ANEXO
**Datos dinámicos:**
- Lista de obligaciones con su estado de cumplimiento
- Observaciones específicas del mes
- Rutas de anexos

**Nota:** Hay múltiples tablas de obligaciones (una por cada categoría o grupo)

### 10. Tablas de Comunicados
**Estructura:** Variable (25-40 filas) x 4 columnas
**Columnas:** ÍTEM | FECHA | CONSECUTIVO ETB | DESCRIPCIÓN
**Datos dinámicos:**
- **Emitidos:** Lista de comunicados emitidos en el mes
- **Recibidos:** Lista de comunicados recibidos en el mes

### 11. Tablas de Personal
**Estructura:** Variable (4-25 filas) x 4 columnas
**Columnas:** (Depende de la tabla específica)
**Datos dinámicos:**
- **Personal Mínimo:** Lista con cargo, cantidad, nombre
- **Personal de Apoyo:** Lista con cargo, cantidad, nombre

---

## 📊 ESTRUCTURA DE DATOS PARA EL GENERADOR

### Tabla 1: Información General
```python
tabla_1_info_general = {
    "filas": [
        {"campo": "NIT", "valor": "899.999.115-8"},
        {"campo": "RAZÓN SOCIAL", "valor": "EMPRESA DE TELECOMUNICACIONES..."},
        {"campo": "CIUDAD", "valor": "BOGOTÁ – COLOMBIA"},
        # ... más filas
    ]
}
```

### Tabla de Comunicados
```python
comunicados_emitidos = [
    {
        "item": 27,
        "fecha": "09/09/2025",
        "consecutivo": "VVG-CCS-ETB-751-25",
        "descripcion": "Remisión comunicado No. VVG-CCS-ETB-751-25..."
    },
    # ... más comunicados
]
```

### Tabla de Obligaciones
```python
obligaciones_generales = [
    {
        "item": 1,
        "obligacion": "Acatar la Constitución, la Ley...",
        "periodicidad": "Permanente",
        "cumplio": "Cumplió",
        "observaciones": "La EMPRESA DE TELECOMUNICACIONES...",
        "anexo": "01SEP - 30SEP / 01 OBLIGACIONES GENERALES/..."
    },
    # ... más obligaciones
]
```

### Tabla de Personal
```python
personal_minimo = [
    {
        "cargo": "Director de Proyecto",
        "cantidad": 1,
        "nombre": "Nombre del Director"
    },
    # ... más personal
]
```

---

## 🔧 ACTUALIZACIONES NECESARIAS EN EL GENERADOR

### 1. Método `procesar()` - Agregar variables faltantes

```python
def procesar(self) -> Dict[str, Any]:
    return {
        # ... variables existentes ...
        
        # Variables para textos de anexos (opcionales)
        "ruta_acta_inicio": self._obtener_ruta_acta_inicio(),
        "numero_adicion": self._obtener_numero_adicion(),
        "ruta_poliza": self._obtener_ruta_poliza(),
        
        # Tabla 1 en formato de lista para docxtpl
        "tabla_1_filas": self._formatear_tabla_1(),
        
        # Tablas de obligaciones en formato de lista
        "tabla_obligaciones_generales": self._formatear_obligaciones_generales(),
        "tabla_obligaciones_especificas": self._formatear_obligaciones_especificas(),
        "tabla_obligaciones_ambientales": self._formatear_obligaciones_ambientales(),
        "tabla_obligaciones_anexos": self._formatear_obligaciones_anexos(),
        
        # Tablas de comunicados en formato correcto
        "tabla_comunicados_emitidos": self._formatear_comunicados_emitidos(),
        "tabla_comunicados_recibidos": self._formatear_comunicados_recibidos(),
        
        # Tablas de personal en formato correcto
        "tabla_personal_minimo": self._formatear_personal_minimo(),
        "tabla_personal_apoyo": self._formatear_personal_apoyo(),
        
        # Glosario en formato de lista para múltiples tablas
        "glosario_tablas": self._formatear_glosario_tablas(),
    }
```

### 2. Nuevos métodos necesarios

```python
def _formatear_tabla_1(self) -> List[Dict]:
    """Formatea la tabla 1 como lista de filas"""
    return [
        {"campo": "NIT", "valor": config.CONTRATO["nit_entidad"]},
        {"campo": "RAZÓN SOCIAL", "valor": config.CONTRATO["razon_social"]},
        # ... más filas
    ]

def _formatear_comunicados_emitidos(self) -> List[Dict]:
    """Formatea comunicados emitidos para tabla"""
    return [
        {
            "item": i+1,
            "fecha": com.get("fecha", ""),
            "consecutivo": com.get("numero", ""),
            "descripcion": com.get("asunto", "")
        }
        for i, com in enumerate(self.comunicados_emitidos)
    ]

def _formatear_obligaciones_generales(self) -> List[Dict]:
    """Formatea obligaciones generales para tabla"""
    # TODO: Cargar desde fuente de datos real
    return []
```

---

## 📝 INSTRUCCIONES PARA CREAR EL TEMPLATE

### Opción 1: Copiar y Modificar Template de Referencia

1. Copiar `data/segmentos/Seccion 1.docx` a `templates/seccion_1_info_general.docx`
2. Reemplazar contenido dinámico con variables Jinja2:
   - Textos fijos → mantener igual
   - Valores en tablas → reemplazar con `{{ variable }}`
   - Filas de tablas → usar `{% for item in lista %}`

### Opción 2: Crear Template desde Cero

1. Crear documento Word nuevo
2. Aplicar estructura según análisis
3. Insertar tablas con encabezados
4. Agregar variables Jinja2 en celdas de datos

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] Analizar estructura completa del documento de referencia
- [ ] Identificar todas las tablas y su estructura
- [ ] Crear template Word con estructura correcta
- [ ] Agregar variables Jinja2 en lugares dinámicos
- [ ] Actualizar generador para formatear datos correctamente
- [ ] Probar generación con datos de ejemplo
- [ ] Validar formato y estructura del documento generado

