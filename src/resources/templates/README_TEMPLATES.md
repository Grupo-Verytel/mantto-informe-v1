# Guía para Crear Templates Word

Los templates Word deben crearse manualmente con el formato y estilos deseados. Estos archivos usarán placeholders de Jinja2 que serán reemplazados por el sistema.

## Crear Template para Sección 1

1. Abrir Microsoft Word
2. Crear un nuevo documento
3. Guardar como `seccion_1_info_general.docx` en la carpeta `templates/`

## Placeholders a Incluir

### Variables simples
```
{{ variable }}
```

### Ejemplos de placeholders para Sección 1:

```
EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ S.A. E.S.P.
INFORME PERIODO {{ mes|upper }} {{ anio }}
CONTRATO {{ contrato_numero }}

═══════════════════════════════════════════════════════════

1. INFORMACIÓN GENERAL DEL CONTRATO {{ contrato_numero }}

1.1 OBJETO CONTRATO {{ contrato_numero }}

{{ objeto_contrato }}

1.2 ALCANCE

{{ alcance }}

1.3 DESCRIPCIÓN DE LA INFRAESTRUCTURA DEL SISTEMA

{{ descripcion_infraestructura }}

Subsistemas del contrato:

{% for subsistema in subsistemas %}
• {{ subsistema }}
{% endfor %}

1.4 GLOSARIO

{% for item in glosario %}
{{ item.termino }}: {{ item.definicion }}

{% endfor %}

1.5 OBLIGACIONES

1.5.1 OBLIGACIONES GENERALES

{{ obligaciones_generales }}

1.5.2 OBLIGACIONES ESPECÍFICAS DEL CONTRATISTA

{{ obligaciones_especificas }}

1.5.3 OBLIGACIONES ESPECÍFICAS EN MATERIA AMBIENTAL

{{ obligaciones_ambientales }}

1.5.4 OBLIGACIONES ANEXOS

{{ obligaciones_anexos }}

1.6 COMUNICADOS CONTRATO {{ contrato_numero }}

1.6.1 EMITIDOS CONTRATO {{ contrato_numero }}

Durante el mes de {{ mes }} de {{ anio }} se emitieron {{ total_comunicados_emitidos }} comunicados:

{% tbl_comunicados_emitidos %}
{% for com in comunicados_emitidos %}
{{ com.numero }} | {{ com.fecha }} | {{ com.asunto }} | {{ com.adjuntos }}
{% endfor %}
{% endtbl_comunicados_emitidos %}

1.6.2 RECIBIDOS CONTRATO {{ contrato_numero }}

Se recibieron {{ total_comunicados_recibidos }} comunicados:

{% tbl_comunicados_recibidos %}
{% for com in comunicados_recibidos %}
{{ com.numero }} | {{ com.fecha }} | {{ com.asunto }} | {{ com.adjuntos }}
{% endfor %}
{% endtbl_comunicados_recibidos %}

1.7 PERSONAL MÍNIMO REQUERIDO

{% tbl_personal_minimo %}
{% for p in personal_minimo %}
{{ p.cargo }} | {{ p.cantidad }} | {{ p.nombre }}
{% endfor %}
{% endtbl_personal_minimo %}

1.8 PERSONAL DE APOYO

{% tbl_personal_apoyo %}
{% for p in personal_apoyo %}
{{ p.cargo }} | {{ p.cantidad }} | {{ p.nombre }}
{% endfor %}
{% endtbl_personal_apoyo %}
```

## Notas Importantes

1. **Tablas en Word**: Para crear tablas, usa la sintaxis `{% tbl_nombre_tabla %}` con bucles `{% for %}` dentro. O crea manualmente las tablas en Word y usa `{% for %}` dentro de las filas.

2. **Formato**: Aplica los estilos deseados directamente en Word (fuentes, tamaños, colores, etc.).

3. **Placeholders**: Los placeholders `{{ variable }}` y `{% for %}` son sintaxis Jinja2 que serán procesados por docxtpl.

4. **Estructura**: Mantén la estructura jerárquica de títulos y subtítulos usando estilos de Word.

## Referencia de docxtpl

Para más información sobre sintaxis de templates, consultar:
- https://docxtpl.readthedocs.io/


