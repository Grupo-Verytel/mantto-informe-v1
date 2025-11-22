# Generador de Informes Mensuales ETB

Sistema automatizado en Python para generar informes mensuales de ~100 páginas para el contrato de mantenimiento **SCJ-1809-2024** de ETB (Empresa de Telecomunicaciones de Bogotá).

## Características

- ✅ Generación automática de informes mensuales
- ✅ Arquitectura modular por secciones
- ✅ Soporte para múltiples fuentes de datos (Excel, CSV, GLPI, MySQL, SharePoint)
- ✅ Templates Word con placeholders Jinja2
- ✅ Manejo de contenido fijo y dinámico

## Estructura del Proyecto

```
mantto-informe-v1/
├── main.py                    # Punto de entrada principal
├── config.py                  # Configuración global
├── requirements.txt           # Dependencias
├── templates/                 # Templates Word con placeholders
├── data/                      # Datos de entrada
│   ├── fuentes/              # Archivos fuente (Excel, CSV)
│   ├── fijos/                # Contenido fijo del contrato
│   └── configuracion/        # Archivos de configuración
├── output/                    # Informes generados
└── src/                       # Código fuente modular
    ├── generadores/          # Generadores por sección
    ├── extractores/          # Extractores de datos
    ├── utils/                # Utilidades
    └── ia/                   # Módulos de IA (Fase 4-5)
```

## Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Generar informe mensual

```bash
# Generar informe de Septiembre 2025
python main.py --anio 2025 --mes 9

# Generar informe con versión específica
python main.py -a 2025 -m 9 -v 2
```

### Parámetros

- `--anio, -a`: Año del informe (default: año actual)
- `--mes, -m`: Mes del informe 1-12 (default: mes actual)
- `--version, -v`: Versión del documento (default: 1)

## Configuración

Editar `config.py` para ajustar:

- Información del contrato
- Rutas de directorios
- Configuración de subsistemas
- Parámetros del contrato

## Archivos de Datos

### Contenido Fijo

Los archivos en `data/fijos/` contienen contenido que no cambia entre informes:

- `alcance.txt`
- `obligaciones_generales.txt`
- `obligaciones_especificas.txt`
- `obligaciones_ambientales.txt`
- `glosario.json`
- `personal_requerido.json`

### Datos Fuente

Los archivos en `data/fuentes/` contienen datos variables que se extraen mensualmente:

- `comunicados_{mes}_{anio}.json`
- Excel/CSV con datos de tickets, inventario, etc.

## Templates Word

Los templates deben crearse manualmente en `templates/` con formato y estilos deseados, usando placeholders Jinja2:

```
{{ variable }}
{% for item in lista %}
  {{ item.campo }}
{% endfor %}
```

## Secciones del Informe

1. **Información General del Contrato** - ✅ Implementado
2. Mesa de Servicio (GLPI)
3. ANS (Disponibilidad)
4. Bienes y Servicios
5. Laboratorio
6. Visitas Técnicas
7. Siniestros
8. Ejecución Presupuestal
9. Matriz de Riesgos
10. SGSST
11. Valores Públicos
12. Conclusiones
13. Anexos
14. Control de Cambios

## Desarrollo

### Agregar nueva sección

1. Crear generador en `src/generadores/seccion_X_nombre.py`
2. Crear template en `templates/seccion_X_nombre.docx`
3. Agregar a la lista de generadores en `main.py`

### Extractores de datos

Los extractores en `src/extractores/` están preparados para:

- **Excel/CSV**: `excel_extractor.py` ✅
- **GLPI**: `glpi_extractor.py` (TODO)
- **MySQL**: `mysql_extractor.py` (TODO)
- **SharePoint**: `sharepoint_extractor.py` (TODO)

## Notas

- Los templates Word deben crearse manualmente con el formato deseado
- El contenido fijo debe completarse desde el Anexo Técnico del contrato real
- Para producción, configurar conexiones a fuentes de datos externas (GLPI, MySQL, SharePoint)

## Licencia

Proyecto interno para ETB - Contrato SCJ-1809-2024


