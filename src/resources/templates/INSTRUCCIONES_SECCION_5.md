# Instrucciones para Crear Template Sección 5

## Archivo: `templates/seccion_5_laboratorio.docx`

### Estructura del Template

1. **Título Principal**
   - Estilo: Título 1
   - Texto: `5. INFORME DE LABORATORIO`

2. **Texto Introductorio**
   - Párrafo normal
   - Texto: `{{ texto_intro }}`

3. **5.1. ACTIVIDADES GENERALES**
   - Estilo: Título 2
   - Texto: `5.1. ACTIVIDADES GENERALES`

4. **5.1.1. REINTEGRADOS AL INVENTARIO**
   - Estilo: Título 3
   - Texto: `5.1.1. REINTEGRADOS AL INVENTARIO`
   
   - Párrafo: `Total de equipos reintegrados: {{ total_reintegrados }}`
   
   - **Tabla**: Crear tabla en Word con 6 columnas:
     - Encabezados: Equipo | Serial | Fecha Reintegro | Motivo Ingreso | Estado Final | Ubicación Destino
     - En la primera fila de datos (después de encabezados), usar:
       ```
       {% for reintegrado in reintegrados %}
       {{ reintegrado.equipo }} | {{ reintegrado.serial }} | {{ reintegrado.fecha_reintegro }} | {{ reintegrado.motivo_ingreso }} | {{ reintegrado.estado_final }} | {{ reintegrado.ubicacion_destino }}
       {% endfor %}
       ```

5. **5.1.2. NO OPERATIVIDAD**
   - Estilo: Título 3
   - Texto: `5.1.2. NO OPERATIVIDAD`
   
   - Párrafo: `Total de equipos no operativos: {{ total_no_operativos }}`
   
   - **Tabla**: Crear tabla en Word con 6 columnas:
     - Encabezados: Equipo | Serial | Fecha Ingreso | Causa No Operatividad | Diagnóstico | Disposición
     - En la primera fila de datos:
       ```
       {% for equipo in no_operativos %}
       {{ equipo.equipo }} | {{ equipo.serial }} | {{ equipo.fecha_ingreso }} | {{ equipo.causa_no_operatividad }} | {{ equipo.diagnostico }} | {{ equipo.disposicion }}
       {% endfor %}
       ```

6. **5.1.3. RMA**
   - Estilo: Título 3
   - Texto: `5.1.3. RMA`
   
   - Párrafo: `Total de equipos en RMA: {{ total_rma }}`
   
   - **Tabla**: Crear tabla en Word con 7 columnas:
     - Encabezados: Equipo | Serial | Fecha Envío | Proveedor | Número RMA | Motivo | Estado
     - En la primera fila de datos:
       ```
       {% for item in rma %}
       {{ item.equipo }} | {{ item.serial }} | {{ item.fecha_envio }} | {{ item.proveedor }} | {{ item.numero_rma }} | {{ item.motivo }} | {{ item.estado }}
       {% endfor %}
       ```

7. **5.2. PENDIENTE POR PARTE**
   - Estilo: Título 2
   - Texto: `5.2. PENDIENTE POR PARTE`
   
   - Párrafo: `Total de equipos pendientes por parte: {{ total_pendiente }}`
   
   - **Tabla**: Crear tabla en Word con 7 columnas:
     - Encabezados: Equipo | Serial | Fecha Ingreso | Parte Requerida | Proveedor | Tiempo Espera | Estado
     - En la primera fila de datos:
       ```
       {% for item in pendiente_por_parte %}
       {{ item.equipo }} | {{ item.serial }} | {{ item.fecha_ingreso }} | {{ item.parte_requerida }} | {{ item.proveedor }} | {{ item.tiempo_espera }} | {{ item.estado }}
       {% endfor %}
       ```

8. **Pie de Sección**
   - Línea separadora: `═══════════════════════════════════════════════════════════`
   - Texto: `Fin Sección 5 - Informe de Laboratorio`
   - Estilo: Cursiva, color gris

## Notas Importantes

- Las tablas deben crearse manualmente en Word usando Insertar > Tabla
- Los placeholders `{{ variable }}` y `{% for %}` deben insertarse como texto normal en las celdas
- Aplicar estilos de tabla según el formato del documento (ej: "Light Grid Accent 1")
- Si una lista está vacía, docxtpl no generará filas en la tabla

## Variables Disponibles en el Contexto

- `texto_intro`: Texto introductorio fijo
- `total_reintegrados`: Número total de equipos reintegrados
- `reintegrados`: Lista de equipos reintegrados
- `total_no_operativos`: Número total de equipos no operativos
- `no_operativos`: Lista de equipos no operativos
- `total_rma`: Número total de equipos en RMA
- `rma`: Lista de equipos en RMA
- `total_pendiente`: Número total de equipos pendientes
- `pendiente_por_parte`: Lista de equipos pendientes por parte

