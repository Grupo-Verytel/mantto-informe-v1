# GUÍA: LECTURA DE ANEXOS DESDE SHAREPOINT

## 🎯 OBJETIVO

Leer archivos de anexos directamente desde SharePoint para generar observaciones dinámicas con LLM, sin necesidad de descargar manualmente los archivos.

---

## ✅ IMPLEMENTACIÓN COMPLETADA

El sistema ahora soporta:
- ✅ Lectura de archivos desde SharePoint
- ✅ Descarga automática temporal
- ✅ Procesamiento con LLM
- ✅ Limpieza automática de archivos temporales

---

## 🔧 CONFIGURACIÓN

### Opción 1: Variables de Entorno (Recomendado)

```bash
# Windows PowerShell
$env:SHAREPOINT_SITE_URL="https://empresa.sharepoint.com/sites/Sitio"
$env:SHAREPOINT_USERNAME="usuario@empresa.com"
$env:SHAREPOINT_PASSWORD="contraseña"

# Linux/Mac
export SHAREPOINT_SITE_URL="https://empresa.sharepoint.com/sites/Sitio"
export SHAREPOINT_USERNAME="usuario@empresa.com"
export SHAREPOINT_PASSWORD="contraseña"
```

### Opción 2: Archivo .env

Crear archivo `.env` en la raíz del proyecto:
```
SHAREPOINT_SITE_URL=https://empresa.sharepoint.com/sites/Sitio
SHAREPOINT_USERNAME=usuario@empresa.com
SHAREPOINT_PASSWORD=contraseña
```

### Opción 3: Configuración en config.py

Agregar a `config.py`:
```python
# Configuración SharePoint
SHAREPOINT_SITE_URL = "https://empresa.sharepoint.com/sites/Sitio"
SHAREPOINT_USERNAME = "usuario@empresa.com"
SHAREPOINT_PASSWORD = "contraseña"
```

---

## 📊 FORMATOS DE RUTAS EN JSON

### Formato 1: URL Completa de SharePoint

```json
{
  "anexo": "https://empresa.sharepoint.com/sites/Sitio/Documentos/01SEP - 30SEP/OBLIGACIONES GENERALES/archivo.pdf"
}
```

### Formato 2: Ruta Relativa de SharePoint

```json
{
  "anexo": "/sites/Sitio/Documentos/01SEP - 30SEP/OBLIGACIONES GENERALES/archivo.pdf"
}
```

**Nota:** Si usas ruta relativa, debe comenzar con `/` y el sistema agregará automáticamente la URL base del sitio.

### Formato 3: Ruta Local (Fallback)

```json
{
  "anexo": "01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ archivo.pdf"
}
```

El sistema intentará primero SharePoint, luego buscará localmente.

---

## 🔍 CÓMO FUNCIONA

### Flujo de Procesamiento

```
1. Cargar obligación desde JSON
   ↓
2. Verificar si "anexo" es URL de SharePoint
   ├─ Sí → Descargar desde SharePoint
   └─ No → Buscar localmente
   ↓
3. Extraer texto del archivo (PDF/DOCX/TXT)
   ↓
4. Enviar a LLM para generar observación
   ↓
5. Limpiar archivo temporal (si se descargó)
```

### Detección Automática

El sistema detecta automáticamente si una ruta es de SharePoint verificando:
- Si comienza con `http://` o `https://`
- Si el dominio contiene `sharepoint.com`, `sharepointonline.com`, etc.

---

## 💻 USO

### Ejemplo de JSON con URL de SharePoint

**Archivo:** `data/fuentes/obligaciones_9_2025.json`

```json
{
  "obligaciones_generales": [
    {
      "item": 1,
      "obligacion": "Acatar la Constitución, la Ley...",
      "periodicidad": "Permanente",
      "cumplio": "Cumplió",
      "observaciones": "",
      "anexo": "https://empresa.sharepoint.com/sites/ContratoSCJ/Documentos/01SEP - 30SEP/01 OBLIGACIONES GENERALES/Oficio Obli SEPTIEMBRE 2025.pdf",
      "regenerar_observacion": true
    }
  ]
}
```

### Generar Sección 1

```python
from src.generadores.seccion_1_info_general import GeneradorSeccion1
from pathlib import Path

# El sistema detectará automáticamente URLs de SharePoint
gen = GeneradorSeccion1(anio=2025, mes=9, usar_llm_observaciones=True)
gen.cargar_datos()  # Descarga y procesa archivos desde SharePoint
gen.guardar(Path("output/seccion_1.docx"))
```

---

## 🔐 AUTENTICACIÓN

### Método 1: Usuario/Contraseña (Básico)

```python
# Configurar variables de entorno
export SHAREPOINT_USERNAME="usuario@empresa.com"
export SHAREPOINT_PASSWORD="contraseña"
```

**Nota:** Este método puede requerir autenticación de dos factores (2FA). Si tu organización usa 2FA, considera usar App Registration.

### Método 2: App Registration (Recomendado)

1. **Registrar aplicación en Azure AD:**
   - Ir a https://portal.azure.com
   - Azure Active Directory > App registrations > New registration
   - Crear nueva aplicación
   - Anotar Application (client) ID

2. **Crear Client Secret:**
   - En la aplicación > Certificates & secrets
   - New client secret
   - Anotar el valor del secret

3. **Dar permisos a SharePoint:**
   - API permissions > Add a permission
   - SharePoint > Application permissions
   - Seleccionar: `Sites.Read.All` o `Sites.ReadWrite.All`
   - Grant admin consent

4. **Configurar variables:**
   ```bash
   export SHAREPOINT_CLIENT_ID="tu-client-id"
   export SHAREPOINT_CLIENT_SECRET="tu-client-secret"
   ```

---

## 📝 EJEMPLO COMPLETO

### 1. Configurar Credenciales

```bash
# Windows PowerShell
$env:SHAREPOINT_SITE_URL="https://etb.sharepoint.com/sites/ContratoSCJ"
$env:SHAREPOINT_USERNAME="usuario@etb.com.co"
$env:SHAREPOINT_PASSWORD="contraseña"
$env:OPENAI_API_KEY="tu-api-key-openai"
```

### 2. Crear JSON de Obligaciones

**Archivo:** `data/fuentes/obligaciones_9_2025.json`

```json
{
  "obligaciones_generales": [
    {
      "item": 1,
      "obligacion": "Acatar la Constitución, la Ley, las normas legales...",
      "periodicidad": "Permanente",
      "cumplio": "Cumplió",
      "observaciones": "",
      "anexo": "https://etb.sharepoint.com/sites/ContratoSCJ/Documentos/01SEP - 30SEP/01 OBLIGACIONES GENERALES/Oficio Obli SEPTIEMBRE 2025.pdf",
      "regenerar_observacion": true
    },
    {
      "item": 2,
      "obligacion": "Cumplir con lo previsto en las disposiciones...",
      "periodicidad": "Permanente",
      "cumplio": "Cumplió",
      "observaciones": "",
      "anexo": "/sites/ContratoSCJ/Documentos/01SEP - 30SEP/01 OBLIGACIONES GENERALES/INFORME MENSUAL SEPTIEMBRE 2025.pdf",
      "regenerar_observacion": true
    }
  ]
}
```

### 3. Ejecutar Generación

```python
from src.generadores.seccion_1_info_general import GeneradorSeccion1
from pathlib import Path

gen = GeneradorSeccion1(anio=2025, mes=9)
gen.cargar_datos()  # Descarga desde SharePoint y genera observaciones
gen.guardar(Path("output/seccion_1.docx"))
```

---

## 🚨 TROUBLESHOOTING

### Error: "No se pudo descargar archivo desde SharePoint"

**Posibles causas:**
1. Credenciales incorrectas
2. URL incorrecta
3. Sin permisos para acceder al archivo
4. Archivo no existe en esa ubicación

**Solución:**
- Verificar credenciales
- Verificar URL del archivo en SharePoint
- Verificar permisos de la cuenta
- Usar URL completa en lugar de ruta relativa

### Error: "Error al inicializar SharePoint"

**Posibles causas:**
1. `Office365-REST-Python-Client` no instalado
2. Credenciales faltantes
3. URL del sitio incorrecta

**Solución:**
```bash
pip install Office365-REST-Python-Client
```

### Error: Autenticación falla con 2FA

**Solución:**
- Usar App Registration en lugar de usuario/contraseña
- O usar token de acceso manual

### Archivo se descarga pero no se lee

**Posibles causas:**
1. Formato no soportado
2. Archivo corrupto
3. Permisos de lectura

**Solución:**
- Verificar que el formato sea PDF, DOCX o TXT
- Verificar que el archivo no esté corrupto
- Verificar permisos

---

## 🔄 ALTERNATIVAS

### Si SharePoint no está disponible

El sistema tiene fallback automático:
1. Intenta SharePoint
2. Si falla, busca localmente
3. Si no encuentra, usa observación genérica

### Usar archivos locales

Simplemente usa rutas locales en el JSON:
```json
{
  "anexo": "data/anexos/archivo.pdf"
}
```

---

## ✅ VENTAJAS

1. **Sin descargas manuales**: Los archivos se descargan automáticamente
2. **Siempre actualizado**: Lee directamente desde SharePoint
3. **Flexible**: Soporta URLs completas y rutas relativas
4. **Robusto**: Fallback automático si SharePoint falla
5. **Seguro**: Limpia archivos temporales después de procesar

---

## 📚 REFERENCIAS

- Office365-REST-Python-Client: https://github.com/vgrem/Office365-REST-Python-Client
- SharePoint REST API: https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service

---

**¡Listo! El sistema ahora puede leer archivos directamente desde SharePoint.** 🚀

