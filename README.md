# Generador de Informes Mensuales ETB

Sistema automatizado en Python para generar informes mensuales de ~100 páginas para el contrato de mantenimiento **SCJ-1809-2024** de ETB (Empresa de Telecomunicaciones de Bogotá).

## Características

- ✅ Generación automática de informes mensuales
- ✅ Arquitectura modular por secciones
- ✅ Soporte para múltiples fuentes de datos (Excel, CSV, GLPI, MySQL, SharePoint)
- ✅ Templates Word con placeholders Jinja2
- ✅ Manejo de contenido fijo y dinámico

## Estructura del Proyecto

```text
mantto-informe-v1/
├── main.py                    # Punto de entrada principal
├── config.py                  # Configuración global unificada
├── requirements.txt           # Dependencias
├── .env.example               # Ejemplo de variables de entorno
│
├── templates/                 # Templates Word con placeholders
├── data/                      # Datos de entrada
│   ├── fuentes/              # Archivos fuente (Excel, CSV, JSON)
│   ├── fijos/                # Contenido fijo del contrato
│   └── configuracion/        # Archivos de configuración
├── output/                    # Informes generados
│
├── src/                       # Código fuente modular
│   ├── app.py                # Aplicación FastAPI
│   ├── controllers/          # Controladores (autenticación, etc.)
│   ├── routes/               # Rutas de la API
│   ├── services/              # Servicios (DB, JWT, auth externa, etc.)
│   ├── models/               # Modelos de datos (User, AccessRole)
│   ├── middleware/            # Middleware (autenticación, permisos)
│   ├── generadores/          # Generadores por sección del informe
│   ├── extractores/          # Extractores de datos (Excel, GLPI, MySQL, SharePoint)
│   ├── utils/                # Utilidades (formato, fechas, tablas, etc.)
│   └── ia/                   # Módulos de IA (análisis, generación de párrafos)
│
├── seeders/                   # Seeders para base de datos
│   ├── access_roles.py       # Seeder de roles de acceso
│   └── run_seeders.py        # Script para ejecutar seeders
│
├── tests/                     # Tests del sistema
│   ├── test_seccion*.py      # Tests unitarios por sección
│   └── test_integracion_*.py # Tests de integración
│
├── docs/                      # Documentación e instrucciones
│   ├── AUTHENTICATION_AND_ROLES.md
│   ├── ESTADO_IMPLEMENTACION_*.md
│   ├── ESTADO_INTEGRACION_*.md
│   └── INSTRUCCIONES_*.md
│
└── legacy/                    # Código legacy (migración en progreso)
    ├── ans_config/           # Configuración ANS (en proceso de migración)
    └── sections.py           # Código antiguo de secciones
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

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto (usar `.env.example` como referencia):

```bash
# Base de datos
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=mantto_informe

# JWT
JWT_SECRET=tu-secreto-super-seguro
JWT_ALGORITHM=HS256
JWT_EXPIRES_IN_HOURS=24

# API Externa
EXTERNAL_AUTH_API_URL=http://localhost:4000
EXTERNAL_AUTH_API_TIMEOUT=10

# Aplicación
DEBUG=False
API_HOST=0.0.0.0
API_PORT=3000
CORS_ORIGINS=http://localhost:5001,http://localhost:3000
```

### Configuración en `config.py`

Editar `config.py` para ajustar:

- Información del contrato
- Rutas de directorios
- Configuración de subsistemas
- Parámetros del contrato
- Valores por defecto de variables de entorno

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

```jinja2
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

### Sistema de Autenticación y Roles

El sistema incluye autenticación JWT y control de acceso basado en roles:

- **API de Autenticación**: `src/app.py` (FastAPI)
- **Rutas**: `src/routes/auth_routes.py`
- **Controladores**: `src/controllers/auth_controller.py`
- **Servicios**: `src/services/` (JWT, DB, Auth externa, Mapeo de roles)
- **Middleware**: `src/middleware/` (Autenticación, permisos)
- **Modelos**: `src/models/` (User, AccessRole)

### Seeders

Para poblar la base de datos con roles iniciales:

```bash
python seeders/run_seeders.py
```

### Tests

Ejecutar tests:

```bash
# Tests unitarios
python -m pytest tests/

# Test específico
python tests/test_seccion1.py
```

## Notas

- Los templates Word deben crearse manualmente con el formato deseado
- El contenido fijo debe completarse desde el Anexo Técnico del contrato real
- Para producción, configurar conexiones a fuentes de datos externas (GLPI, MySQL, SharePoint)

## Licencia

Proyecto interno para ETB - Contrato SCJ-1809-2024
