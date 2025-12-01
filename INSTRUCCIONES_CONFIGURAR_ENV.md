# INSTRUCCIONES: CONFIGURAR ARCHIVO .env

## 📋 PASOS PARA CONFIGURAR

### 1. Crear el archivo .env

**Opción A: Usar el script (Recomendado)**
```bash
python crear_env.py
```

**Opción B: Copiar manualmente**
```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2. Editar el archivo .env

Abre el archivo `.env` en tu editor de texto y reemplaza los valores de ejemplo con tus credenciales reales.

---

## 🔑 CONFIGURACIÓN DE OPENAI

### Obtener API Key de OpenAI

1. Ir a https://platform.openai.com/api-keys
2. Iniciar sesión o crear cuenta
3. Click en "Create new secret key"
4. Copiar la key (solo se muestra una vez)
5. Pegar en `.env`:
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```

### Modelo de OpenAI (Opcional)

Por defecto usa `gpt-4o-mini` (más económico). Puedes cambiar a:
- `gpt-4o-mini` - Más económico, rápido (recomendado)
- `gpt-4o` - Más potente, más caro
- `gpt-4-turbo` - Balance
- `gpt-3.5-turbo` - Alternativa económica

---

## 🔐 CONFIGURACIÓN DE SHAREPOINT

### Opción 1: Usuario y Contraseña (Básico)

**Configurar:**
```
SHAREPOINT_SITE_URL=https://empresa.sharepoint.com/sites/ContratoSCJ
SHAREPOINT_USERNAME=usuario@empresa.com
SHAREPOINT_PASSWORD=tu-contraseña
```

**Nota:** Si tu organización usa autenticación de dos factores (2FA), este método puede no funcionar. Usa App Registration en ese caso.

### Opción 2: App Registration (Recomendado - Más Seguro)

#### Paso 1: Registrar Aplicación en Azure AD

1. Ir a https://portal.azure.com
2. Azure Active Directory > App registrations
3. New registration
4. Nombre: "Informe Mantenimiento ETB" (o el que prefieras)
5. Supported account types: "Accounts in this organizational directory only"
6. Redirect URI: Dejar vacío
7. Click "Register"
8. **Anotar el Application (client) ID**

#### Paso 2: Crear Client Secret

1. En la aplicación creada > Certificates & secrets
2. New client secret
3. Description: "Secret para Informe Mantenimiento"
4. Expires: Elegir duración (ej: 24 meses)
5. Click "Add"
6. **Copiar el VALUE del secret** (solo se muestra una vez)

#### Paso 3: Dar Permisos a SharePoint

1. En la aplicación > API permissions
2. Add a permission
3. SharePoint > Application permissions
4. Seleccionar:
   - `Sites.Read.All` (para leer archivos)
   - O `Sites.ReadWrite.All` (si necesitas escribir)
5. Click "Add permissions"
6. **Grant admin consent** (botón azul)

#### Paso 4: Configurar en .env

```
SHAREPOINT_SITE_URL=https://empresa.sharepoint.com/sites/ContratoSCJ
SHAREPOINT_CLIENT_ID=tu-client-id-aqui
SHAREPOINT_CLIENT_SECRET=tu-client-secret-aqui
```

**Dejar vacíos:**
```
SHAREPOINT_USERNAME=
SHAREPOINT_PASSWORD=
```

---

## 📝 EJEMPLO DE ARCHIVO .env COMPLETO

```env
# OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini

# SharePoint (con App Registration)
SHAREPOINT_SITE_URL=https://etb.sharepoint.com/sites/ContratoSCJ
SHAREPOINT_CLIENT_ID=12345678-1234-1234-1234-123456789abc
SHAREPOINT_CLIENT_SECRET=abc~1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ
SHAREPOINT_USERNAME=
SHAREPOINT_PASSWORD=
```

---

## ✅ VERIFICAR CONFIGURACIÓN

### Probar OpenAI

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key configurada: {bool(api_key)}")
```

### Probar SharePoint

```python
from src.extractores.sharepoint_extractor import get_sharepoint_extractor

extractor = get_sharepoint_extractor()
print(f"SharePoint configurado: {extractor.site_url is not None}")
```

---

## 🔒 SEGURIDAD

### ⚠️ IMPORTANTE

1. **NO subir .env a Git** - Ya está en `.gitignore`
2. **NO compartir el archivo .env** - Contiene credenciales sensibles
3. **Usar App Registration** - Más seguro que usuario/contraseña
4. **Rotar credenciales** - Cambiar periódicamente
5. **Revisar permisos** - Solo dar permisos necesarios

### Variables de Entorno Alternativas

Si prefieres no usar archivo `.env`, puedes configurar variables de entorno del sistema:

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-proj-..."
$env:SHAREPOINT_SITE_URL="https://..."
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-proj-..."
export SHAREPOINT_SITE_URL="https://..."
```

---

## 🚨 TROUBLESHOOTING

### Error: "OPENAI_API_KEY no configurada"

**Solución:**
- Verificar que el archivo `.env` existe
- Verificar que la variable está escrita correctamente (sin espacios)
- Verificar que estás usando `python-dotenv` para cargar el archivo

### Error: "SharePoint no configurado"

**Solución:**
- Verificar que `SHAREPOINT_SITE_URL` está configurada
- Verificar que tienes `SHAREPOINT_USERNAME` y `SHAREPOINT_PASSWORD` O `SHAREPOINT_CLIENT_ID` y `SHAREPOINT_CLIENT_SECRET`
- Verificar que la URL es correcta

### Error: "No se puede autenticar con SharePoint"

**Solución:**
- Verificar credenciales
- Si usas 2FA, usar App Registration
- Verificar permisos de la aplicación en Azure AD
- Verificar que se dio "Grant admin consent"

---

## 📚 REFERENCIAS

- OpenAI API Keys: https://platform.openai.com/api-keys
- Azure AD App Registration: https://portal.azure.com
- SharePoint REST API: https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service

---

**¡Listo! Una vez configurado el archivo .env, el sistema podrá usar LLM y SharePoint automáticamente.** 🚀

