# GUÍA: GENERACIÓN DINÁMICA DE OBSERVACIONES CON LLM

## 🎯 OBJETIVO

Generar observaciones de cumplimiento de forma dinámica basándose en el contenido real de los archivos de anexos, usando LLM (Large Language Model) para extraer y resumir información relevante.

---

## 📋 FUNCIONAMIENTO

### Flujo de Generación

```
1. Cargar obligaciones desde JSON
   ↓
2. Para cada obligación:
   ├─ Leer ruta del anexo
   ├─ Extraer texto del archivo (PDF/DOCX/TXT)
   ├─ Enviar a LLM con contexto de la obligación
   └─ Generar observación profesional
   ↓
3. Incluir observaciones en el contexto del template
   ↓
4. Template Word renderiza las observaciones
```

---

## 🔧 CONFIGURACIÓN

### 1. Instalar Dependencias

```bash
pip install openai PyPDF2
```

O actualizar `requirements.txt` (ya está actualizado):
```bash
pip install -r requirements.txt
```

### 2. Configurar API Key de OpenAI

**Opción A: Variable de Entorno (Recomendado)**

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="tu-api-key-aqui"

# Windows CMD
set OPENAI_API_KEY=tu-api-key-aqui

# Linux/Mac
export OPENAI_API_KEY="tu-api-key-aqui"
```

**Opción B: Archivo .env**

Crear archivo `.env` en la raíz del proyecto:
```
OPENAI_API_KEY=tu-api-key-aqui
```

**Opción C: Configuración en Código (No Recomendado)**

Modificar `src/ia/extractor_observaciones.py` directamente (solo para pruebas).

### 3. Obtener API Key de OpenAI

1. Ir a https://platform.openai.com/api-keys
2. Crear cuenta o iniciar sesión
3. Crear nueva API key
4. Copiar la key y configurarla según opción A o B

---

## 📊 ESTRUCTURA DE DATOS

### Archivo JSON de Obligaciones

**Ubicación:** `data/fuentes/obligaciones_{mes}_{anio}.json`

**Estructura:**
```json
{
  "obligaciones_generales": [
    {
      "item": 1,
      "obligacion": "Acatar la Constitución, la Ley...",
      "periodicidad": "Permanente",
      "cumplio": "Cumplió",
      "observaciones": "",  // Se generará automáticamente
      "anexo": "01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 1/ archivo.pdf",
      "regenerar_observacion": true  // Forzar regeneración
    }
  ],
  "obligaciones_especificas": [],
  "obligaciones_ambientales": [],
  "obligaciones_anexos": []
}
```

### Campos Importantes

- **`anexo`**: Ruta relativa al archivo de anexo (PDF, DOCX, TXT)
- **`regenerar_observacion`**: Si es `true`, siempre regenera la observación (ignora `observaciones` existente)
- **`observaciones`**: Si está vacío y `regenerar_observacion` es `true`, se genera automáticamente

---

## 🗂️ ESTRUCTURA DE ARCHIVOS DE ANEXOS

### Ubicación de Anexos

El sistema busca archivos en estas ubicaciones (en orden):

1. `output/{anio}/{mes}/` - Donde se generan los informes
2. `data/anexos/` - Carpeta dedicada a anexos
3. `data/fuentes/` - Fuentes de datos
4. Ruta absoluta (si se proporciona ruta completa)

### Formato de Rutas

Las rutas en el JSON pueden ser:

**Formato 1: Ruta relativa completa**
```
"01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 1/ archivo.pdf"
```

**Formato 2: Solo nombre de archivo**
```
"archivo.pdf"
```
(El sistema buscará en todas las ubicaciones posibles)

---

## 💻 USO

### Uso Básico

```python
from src.generadores.seccion_1_info_general import GeneradorSeccion1
from pathlib import Path

# Generar con LLM habilitado (default)
gen = GeneradorSeccion1(anio=2025, mes=9, usar_llm_observaciones=True)
gen.cargar_datos()  # Aquí se generan las observaciones
gen.guardar(Path("output/seccion_1.docx"))
```

### Deshabilitar LLM (usar observaciones estáticas)

```python
# Si no tienes API key o quieres usar observaciones predefinidas
gen = GeneradorSeccion1(anio=2025, mes=9, usar_llm_observaciones=False)
gen.cargar_datos()
gen.guardar(Path("output/seccion_1.docx"))
```

### Uso Directo del Extractor

```python
from src.ia.extractor_observaciones import get_extractor_observaciones

extractor = get_extractor_observaciones()

obligacion = {
    "item": 1,
    "obligacion": "Acatar la Constitución...",
    "periodicidad": "Permanente",
    "cumplio": "Cumplió",
    "anexo": "ruta/al/archivo.pdf"
}

# Procesar y generar observación
obligacion_procesada = extractor.procesar_obligacion(obligacion)
print(obligacion_procesada["observaciones"])
```

---

## 🔍 CÓMO FUNCIONA LA EXTRACCIÓN

### 1. Lectura de Archivos

El sistema soporta:
- **PDF**: Usa `PyPDF2` para extraer texto
- **DOCX**: Usa `python-docx` para extraer texto
- **TXT**: Lee directamente

### 2. Generación con LLM

**Prompt enviado al LLM:**
```
Eres un asistente que genera observaciones de cumplimiento contractual...

CONTEXTO:
- Obligación: [texto de la obligación]
- Periodicidad: [permanente/mensual/etc]
- Estado: [Cumplió/No Cumplió]

CONTENIDO DEL ANEXO:
[texto extraído del archivo - máximo 4000 caracteres]

INSTRUCCIONES:
Genera una observación profesional y concisa...
```

**Parámetros del LLM:**
- Modelo: `gpt-4o-mini` (configurable)
- Max tokens: 300
- Temperature: 0.3 (baja para respuestas más determinísticas)

### 3. Fallback

Si el LLM no está disponible o falla:
- Usa observaciones genéricas basadas en palabras clave de la obligación
- Mantiene el formato profesional
- Incluye información básica de cumplimiento

---

## ⚙️ CONFIGURACIÓN AVANZADA

### Cambiar Modelo de LLM

```python
from src.ia.extractor_observaciones import ExtractorObservaciones

extractor = ExtractorObservaciones(
    api_key="tu-api-key",
    model="gpt-4"  # Modelo más potente (más caro)
)
```

### Modelos Disponibles

- `gpt-4o-mini` - Más económico, rápido (recomendado)
- `gpt-4o` - Más potente, más caro
- `gpt-4-turbo` - Balance entre costo y calidad
- `gpt-3.5-turbo` - Alternativa económica

### Personalizar Prompt

Editar método `generar_observacion_llm()` en `src/ia/extractor_observaciones.py`:

```python
prompt = f"""Tu prompt personalizado aquí...
{texto_anexo}
"""
```

---

## 📝 EJEMPLO COMPLETO

### 1. Crear Archivo JSON de Obligaciones

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
      "anexo": "01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 1/ Oficio Obli SEPTIEMBRE 2025.pdf",
      "regenerar_observacion": true
    }
  ]
}
```

### 2. Colocar Archivo de Anexo

Colocar el archivo PDF en:
```
data/anexos/01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ OBLIGACIÓN 1/ Oficio Obli SEPTIEMBRE 2025.pdf
```

O en cualquier ubicación que el sistema pueda encontrar.

### 3. Configurar API Key

```bash
export OPENAI_API_KEY="sk-..."
```

### 4. Generar Sección 1

```python
from src.generadores.seccion_1_info_general import GeneradorSeccion1
from pathlib import Path

gen = GeneradorSeccion1(anio=2025, mes=9)
gen.cargar_datos()  # Genera observaciones automáticamente
gen.guardar(Path("output/seccion_1.docx"))
```

---

## 🚨 MANEJO DE ERRORES

### Error: API Key no configurada

**Síntoma:**
```
[WARNING] openai no está disponible. Las observaciones se generarán de forma estática.
```

**Solución:**
- Configurar `OPENAI_API_KEY` como variable de entorno
- O pasar `usar_llm_observaciones=False` al generador

### Error: Archivo de anexo no encontrado

**Síntoma:**
```
[WARNING] No se encontró archivo de anexo: ruta/del/archivo.pdf
```

**Solución:**
- Verificar que la ruta en el JSON sea correcta
- Colocar el archivo en una de las ubicaciones de búsqueda
- O usar ruta absoluta en el JSON

### Error: No se puede leer el archivo

**Síntoma:**
```
[WARNING] Error al leer PDF ruta/archivo.pdf: ...
```

**Solución:**
- Verificar que el archivo no esté corrupto
- Verificar permisos de lectura
- Verificar que el formato sea soportado (PDF, DOCX, TXT)

### Error: LLM no responde

**Síntoma:**
```
[WARNING] Error al generar observación con LLM: ...
```

**Solución:**
- Verificar conexión a internet
- Verificar que la API key sea válida
- Verificar límites de uso de la API
- El sistema usará fallback automáticamente

---

## 💰 COSTOS

### Estimación de Costos (OpenAI)

**Modelo gpt-4o-mini:**
- Input: ~$0.15 por 1M tokens
- Output: ~$0.60 por 1M tokens

**Ejemplo:**
- 1 obligación con anexo de 2000 caracteres ≈ 500 tokens input
- Observación generada ≈ 100 tokens output
- Costo por obligación: ~$0.0001 (muy bajo)

**Para un mes típico:**
- 20 obligaciones × $0.0001 = **$0.002 por mes**

### Optimizaciones

1. **Cache de observaciones**: Guardar observaciones generadas para reutilizar
2. **Límite de texto**: Limitar texto del anexo a 4000 caracteres
3. **Modelo económico**: Usar `gpt-4o-mini` en lugar de `gpt-4`
4. **Batch processing**: Procesar múltiples obligaciones en una llamada

---

## 🔒 SEGURIDAD Y PRIVACIDAD

### Datos Enviados a OpenAI

- Texto extraído de anexos (máximo 4000 caracteres)
- Texto de la obligación
- Estado de cumplimiento

### Recomendaciones

1. **No enviar información sensible** sin revisar
2. **Revisar anexos** antes de procesarlos
3. **Usar modelos locales** si la información es muy sensible
4. **Configurar retención de datos** en OpenAI (si aplica)

### Alternativas

Si no quieres usar OpenAI:
- **Modelos locales**: Ollama, LM Studio
- **APIs alternativas**: Anthropic Claude, Google Gemini
- **Sistema híbrido**: LLM solo para casos complejos, templates para casos simples

---

## ✅ VENTAJAS DEL SISTEMA

1. **Observaciones dinámicas**: Basadas en contenido real de anexos
2. **Ahorro de tiempo**: No escribir observaciones manualmente
3. **Consistencia**: Formato profesional uniforme
4. **Escalabilidad**: Procesa múltiples obligaciones automáticamente
5. **Fallback robusto**: Funciona aunque el LLM falle

---

## 📚 REFERENCIAS

- OpenAI API: https://platform.openai.com/docs
- PyPDF2: https://pypdf2.readthedocs.io/
- python-docx: https://python-docx.readthedocs.io/

---

**¡Listo! El sistema generará observaciones dinámicas automáticamente basándose en el contenido real de los anexos.**

