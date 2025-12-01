# INSTRUCCIONES PARA ACTUALIZAR TEMPLATE SECCIÓN 1

## CAMBIOS NECESARIOS EN `templates/seccion_1_info_general.docx`

### 1. AGREGAR TABLA 1 - INFORMACIÓN GENERAL DEL CONTRATO

**Ubicación:** Al inicio de la sección, después del título "1. INFORMACIÓN GENERAL DEL CONTRATO SCJ-1809-2024"

**Estructura de la tabla:**

```
INFORMACIÓN GENERAL CONTRATO SCJ-1809-2024
NIT: {{ tabla_1_info_general.nit }}
RAZÓN SOCIAL: {{ tabla_1_info_general.razon_social }}
CIUDAD: {{ tabla_1_info_general.ciudad }}
DIRECCIÓN: {{ tabla_1_info_general.direccion }}
TELÉFONO: {{ tabla_1_info_general.telefono }}

DATOS DEL CONTRATO
CONTRATO NO.: {{ tabla_1_info_general.numero_contrato }}
FECHA DE INICIO: {{ tabla_1_info_general.fecha_inicio }}
PLAZO DE EJECUCIÓN INICIAL: {{ tabla_1_info_general.plazo_ejecucion }}
FECHA DE TERMINACIÓN: {{ tabla_1_info_general.fecha_terminacion }}
VALOR INICIAL DEL CONTRATO: {{ tabla_1_info_general.valor_inicial }}
ADICIÓN I: {{ tabla_1_info_general.adicion_1 }}
TOTAL: {{ tabla_1_info_general.valor_total }}

OBJETO:
{{ tabla_1_info_general.objeto }}

FECHA FIRMA ACTA DE INICIO: {{ tabla_1_info_general.fecha_firma_acta }}
FECHA SUSCRIPCIÓN DEL CONTRATO: {{ tabla_1_info_general.fecha_suscripcion }}
VIGENCIA PÓLIZA INICIAL: {{ tabla_1_info_general.vigencia_poliza_inicial }}
VIGENCIA PÓLIZA ACTA INICIAL: {{ tabla_1_info_general.vigencia_poliza_acta }}
```

**Título de tabla:** "Tabla 1. INFORMACIÓN GENERAL CONTRATO SCJ-1809-2024"

### 2. AGREGAR TEXTO INTRODUCTORIO

**Ubicación:** Justo después del título principal, antes de la Tabla 1

**Texto:**
```
{{ texto_intro }}
```

### 3. AGREGAR TABLAS EN 1.3 - DESCRIPCIÓN DE INFRAESTRUCTURA

#### Tabla 2: Componentes por Subsistema

**Ubicación:** Dentro de la subsección 1.3, después del texto descriptivo

**Estructura:**
```
Tabla 2. COMPONENTES POR CADA SUBSISTEMA SEGÚN ANEXO 1.

| SISTEMA DE VIDEO VIGILANCIA | CANTIDAD DE UBICACIONES | CANTIDAD DE PUNTOS DE CÁMARA | CANTIDAD CENTROS DE MONITOREO – C4 | CANTIDAD VISUALIZADAS LOCALMENTE |
| {% for comp in tabla_componentes %} {{ comp.sistema }} | {{ comp.ubicaciones }} | {{ comp.puntos_camara }} | {{ comp.centros_monitoreo_c4 }} | {{ comp.visualizadas_localmente }} {% endfor %}
```

#### Tabla 3: Centros de Monitoreo

**Ubicación:** Después de la Tabla 2

**Estructura:**
```
Tabla 3. CENTRO DE MONITOREO

Los Centros de Monitoreo que actualmente están bajo la supervisión de la MEBOG para la operación y monitoreo de video vigilancia se relacionan a continuación:

| N° | CENTRO DE MONITOREO | DIRECCIÓN | LOCALIDAD |
| {% for cm in tabla_centros_monitoreo %} {{ cm.numero }} | {{ cm.nombre }} | {{ cm.direccion }} | {{ cm.localidad }} {% endfor %}

Nota: Los centros de monitoreo Rafael Uribe se encuentra en garantía y el centro monitoreo Santa Fe aún no ha sido entregado oficialmente.
```

#### Tabla 4: Forma de Pago

**Ubicación:** Después de la Tabla 3

**Estructura:**
```
Tabla 4. FORMA DE PAGO SDSCJ

La SDSCJ pagará al contratista los servicios prestados y elementos utilizados mensualmente de acuerdo con las condiciones establecidas para este Acuerdo No 9, oferta de servicio mensualizado y el uso de la bolsa de repuestos y servicios, así:

| N° | DESCRIPCIÓN | TIPO SERVICIO |
| {% for fp in tabla_forma_pago %} {{ fp.numero }} | {{ fp.descripcion }} | {{ fp.tipo_servicio }} {% endfor %}
```

### 4. VERIFICAR TEXTO DE 1.1 OBJETO

**Cambiar de:**
```
{{ objeto_contrato }}
```

**A:**
```
{{ objeto_contrato }}

MANTENIMIENTO PREVENTIVO, MANTENIMIENTO CORRECTIVO Y SOPORTE AL SISTEMA DE VIDEOVIGILANCIA DE BOGOTÁ D.C., CON DISPONIBILIDAD DE BOLSA DE REPUESTOS, en las mejores condiciones técnicas y financieras y en aplicación de los principios de colaboración entre entidades públicas, de eficiencia y economía, resulta necesario adelantar un contrato interadministrativo de prestación de servicios con la EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ SA ESP - ETB S.A. E.S.P., para el desarrollo del objeto contractual requerido.
```

## NOTAS IMPORTANTES

1. **Mantener el estilo visual:** Usar la misma fuente, tamaños y formato que el resto del documento
2. **Placeholders Jinja2:** Asegurarse de usar la sintaxis correcta `{{ variable }}` y `{% for %}`
3. **Tablas:** En docxtpl, para tablas dinámicas, el `{% for %}` debe estar en la primera celda y `{% endfor %}` en la última celda de la fila template
4. **Formato de valores:** Los valores monetarios ya vienen formateados desde el generador

## VERIFICACIÓN

Después de actualizar el template, ejecutar:

```bash
python main.py --anio 2025 --mes 9
```

Y verificar que la Sección 1 se genere correctamente con todas las tablas y datos.

