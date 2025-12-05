# 🔐 Documentación: Sistema de Autenticación y Control de Usuarios y Roles

## 📋 Índice

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Modelos de Datos](#modelos-de-datos)
4. [Autenticación](#autenticación)
5. [Sistema de Roles](#sistema-de-roles)
6. [Control de Acceso](#control-de-acceso)
7. [Frontend - Implementación](#frontend---implementación)
8. [Backend - Implementación](#backend---implementación)
9. [Endpoints API](#endpoints-api)
10. [Seguridad](#seguridad)
11. [Usuarios de Prueba](#usuarios-de-prueba)

---

## 📊 Resumen Ejecutivo

El sistema implementa el frontend de autenticación basado en **JWT (JSON Web Tokens)** con un modelo de roles definido en mongodb:

- **Roles de Acceso**: Definen los permisos de acceso a módulos específicos del sistema (superadmin, admin_módulo, readonly_módulo)

### Tecnologías Utilizadas

| Componente | Tecnología |
|------------|-----------|
| **Autenticación** | JWT (jsonwebtoken) |
| **Hash de Contraseñas** | bcryptjs (10 rounds) |
| **Frontend Auth** | React Context API |
| **Almacenamiento** | localStorage (user), token  (cockies http_only ) |
| **ODM** |  python |
| **Base de Datos** | Mongo (roles)

---

## 🏗️ Arquitectura del Sistema

### Flujo de Autenticación

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       │ 1. POST /api/auth/login (password hash)
       ▼
┌─────────────────────┐
│  authController.py  │
│  - llama a api de verificacion,     │
│  - Verifica usuario, y con el rol devuelto homologa el rol │
│  - Genera JWT       │
└──────┬──────────────┘
       │
       │ 2. Retorna token + user
       ▼
┌─────────────────────┐
│  AuthContext.ts
│  - Guarda en        │
│    cockies     │
│  - Actualiza estado  │
└──────┬──────────────┘
       │
       │ 3. Token en headers
       ▼
┌─────────────────────┐
│ authMiddleware.js   │
│  - Verifica JWT     │
│  - Carga usuario    │
│  - Agrega req.user  │
└─────────────────────┘
```

### Estructura de Archivos

```
backend/
├── src/
│   ├── service/
│   │   └── authController.js          # Lógica de consulta externa de existencia de usuario,
│   ├── middleware/
│   │   ├── authMiddleware.js          # Verificación JWT
│   │   └── permissions.js             # Helpers de permisos
│   ├── models/
│   │   └── AccessRole.js              # Modelo de rol de acceso
│   └── routes/
│       └── authRoutes.js               # Rutas de autenticación
└── seeders/
    ├── 00-access-roles.js             # Seed de roles de acceso

frontend/
├── src/
│   ├── contexts/
│   │   └── AuthContext.tsx            # Context de autenticación
│   ├── pages/
│   │   └── LoginPage.tsx              # Página de login
│   ├── services/
│   │   └── authApi.ts                 # API client de autenticación
│   └── utils/
│       └── permissions.ts             # Utilidades de permisos
```

---

## 📊 Modelos de Datos


**Campos Clave:**
- `password`: Almacenado con hash bcrypt (10 rounds)
- `functional_role_id`: Relación con modulo/permiso
- `access_role_id`: Relación con permisos de acceso


**Modulos Predefinidos:**

se definen modulos del informe al cual solo los usuarios asignados pueden acceder 
1. Información General del Contrato
2. Informe de Mesa de servicio
3. Informes de medición de niveles de servicio ANS
4. Informe de Bienes y servicios
5. Informe de laboratorio
6. Informe de Visitas Ejecutadas
7. Informe de Siniestros 
8. Ejecución presupuestal
9. Matriz de riesgos
10. Informe mensual de gestión SGSST
11. Valores públicos
12. Conclusiones
13. Anexos
14. Control de Revisiones y Cambios

## 🔐 Autenticación

### Proceso de Login

1. **Usuario envía credenciales** (`email` + `password` encriptada)
2. **Backend :**
  - hace peticion en api externa de login (devuelve jwt)
  - verifica el rol devuelto el mongo el rol de aplicacion 
  - devuelve rol y token jwt

3. **Frontend guarda:**
   - Token en `cockie http_only 'token'`
   - User en `localStorage.setItem('user', JSON.stringify(user))`
4. **Todas las peticiones incluyen:**
   ```
   Authorization: header <token>
   ```

### Configuración JWT

```javascript
// Variables de entorno (.env)
JWT_SECRET=tu-secreto-super-seguro-cambialo-en-produccion
JWT_EXPIRES_IN=24h  // Token expira en 24 horas
```

### Hash de Contraseñas

- **Algoritmo**: bcrypt
- **Rounds**: 10
- **Ejemplo**:
  ```javascript
  const hashedPassword = await bcrypt.hash(password, 10);
  const isValid = await bcrypt.compare(password, hashedPassword);
  ```

---

## 👥 Sistema de Roles

### Concepto  de Roles

#### 2. **Rol de Acceso** (`access_role_id`)
- Define los **permisos de acceso** a módulos del sistema
- Ejemplos: `admin`, `readonly`, `superadmin`
- **Propósito**: Control de acceso a funcionalidades
- **Sí afecta permisos de acceso**

### Niveles de Permiso

| Nivel | Descripción | Acciones Permitidas |
|-------|-------------|---------------------|
| `superadmin` | Super Administrador | Acceso total a todos los módulos (lectura + escritura) |
| `admin` | Administrador de Módulo | Lectura + Escritura en su módulo asignado |
| `readonly` | Solo Lectura | Solo lectura en su módulo asignado |

Cada permiso puede aplicarse a los modulos es decir pueden haber usuarios con acceso a ciertos modulos con diferentes niveles de permiso 


## 🛡️ Control de Acceso

### Middleware de Autenticación

**Archivo**: `backend/src/middleware/authMiddleware.js`

```python
// Verifica JWT token en cada petición
def authMiddleware() {
  // 1. Extrae token de header:  <token>
  // 2. Verifica token con JWT_SECRET
  // 3. busca en api externa 
  // 4. Agrega req.user con información del usuario
  // 5. Continúa al siguiente middleware
}
```

**Uso en rutas:**
```python
router.get('/informe ', authMiddleware, authController.getProfile);
```

### Middleware de Permisos

**Archivo**: `backend/src/middleware/authMiddleware.py`

#### 1. `requireAccessRole(...allowedAccessRoles)`
Verifica que el usuario tenga uno de los roles de acceso permitidos.

```python
// Ejemplo: Solo admin o readonly 
router.get('/projects', 
  authMiddleware, 
  requireAccessRole('admin_fabrica_software', 'readonly_fabrica_software'),
  projectController.getAll
);
```

#### 2. `requireWritePermission(module)`
Verifica que el usuario tenga permisos de escritura en el módulo.

```python
router.post('/projects', 
  authMiddleware, 
  requireWritePermission(''),
  projectController.create
);
```

#### 3. `requireRole(...allowedRoles)`
Verifica que el usuario tenga uno de los roles funcionales permitidos.

```python
router.get('/reports', 
  authMiddleware, 
  requireRole(''),
  reportController.getAll
);
```

### Helpers de Permisos

**Archivo**: `backend/src/middleware/authMiddleware.js`

```javascript
// Verifica si puede leer un módulo
canRead(userAccessRole, module) {
  if (userAccessRole === 'superadmin') return true;
  return userAccessRole === `admin_${module}` || 
         userAccessRole === `readonly_${module}`;
}

// Verifica si puede escribir en un módulo
canWrite(userAccessRole, module) {
  if (userAccessRole === 'superadmin') return true;
  return userAccessRole === `admin_${module}`;
}
```

---

## 🎨 Frontend - Implementación

### AuthContext

**Archivo**: `frontend/src/contexts/AuthContext.tsx`

**Funcionalidad:**
- Maneja el estado global de autenticación
- Persiste token y usuario cookies y local storage
- Proporciona funciones: `login`, `logout`

**Estado:**
```typescript
{
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
```

**Uso:**
```typescript
import { useAuth } from '../contexts/AuthContext';

const { user, login, logout, isAuthenticated } = useAuth();
```

### LoginPage

**Archivo**: `frontend/src/pages/LoginPage.tsx`

**Características:**
- Formulario de login con validación
- Manejo de errores
- Integración con `AuthContext`
- Redirección automática después del login

### authApi Service

**Archivo**: `frontend/src/services/authApi.ts`

**Métodos:**
- `login(credentials)` - Iniciar sesión
- `verifyToken()` - Verificar si el token es válido

### Utilidades de Permisos

**Archivo**: `frontend/src/utils/permissions.ts`

**Funciones:**
```typescript
// Verifica si es superadmin
isSuperAdmin(accessRole: string): boolean

// Verifica si puede leer un módulo
canRead(accessRole: string, module: Module): boolean

// Verifica si puede escribir en un módulo
canWrite(accessRole: string, module: Module): boolean

// Obtiene el nombre legible del rol
getAccessRoleLabel(accessRole: string): string

// Obtiene el módulo de un access_role
getModuleFromAccessRole(accessRole: string): Module | null
```

**Uso en componentes:**
```typescript
import { canWrite, canRead } from '../utils/permissions';

const { user } = useAuth();

if (canWrite(user.access_role, 'fabrica_software')) {
  // Mostrar botón de crear proyecto
}
```

### Interceptor de Axios

**Archivo**: `frontend/src/services/api.ts`

**Funcionalidad:**
- Agrega automáticamente el token JWT a todas las peticiones
- Maneja errores 401 (no autorizado) y redirige al login

```typescript
// Interceptor de request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor de response
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token inválido o expirado
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

---

## ⚙️ Backend - Implementación

### authController

**Archivo**: `backend/src/controllers/authController.py`

**Métodos:**


#### 2. `login(req, res)`
Inicia sesión con email y contraseña.

**Request:**
```json
{
  "email": "juan@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": { /* mismo formato que register */ }
  }
}
```

**Errores:**
- `400`: Email o contraseña faltantes
- `401`: Credenciales inválidas o usuario inactivo

## 🌐 Endpoints API

### Base URL
```
http://localhost:3000/api/auth
```

### Endpoints

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|

| `POST` | `/login` | Iniciar sesión | ❌ Público |
| `GET` | `/verify` | Verificar token | ✅ Requerida |

### Ejemplo de Uso

```bash
# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin.fabrica@verytel.com",
    "password": "admin1234"
  }'



---

## 🔒 Seguridad

### Medidas Implementadas

1. **Hash de Contraseñas**
   - bcrypt con 10 rounds
   - Las contraseñas nunca se almacenan en texto plano

2. **JWT Tokens**
   - Firma con secreto (`JWT_SECRET`)
   - Expiración configurable (default: 24h)
   - Payload incluye solo información necesaria

3. **Validación de Usuario Activo**
   - Solo usuarios con `is_active = true` pueden iniciar sesión
   - El middleware verifica el estado en cada petición

4. **Headers de Autorización**
   - Formato estándar: `Authorization: Bearer <token>`
   - Validación estricta del formato

5. **Manejo de Errores**
   - Mensajes genéricos para evitar información sensible
   - Logs de errores en servidor (no en respuesta)

### Recomendaciones para Producción

1. **Variables de Entorno**
   ```env
   JWT_SECRET=<secreto-fuerte-generado-aleatoriamente>
   JWT_EXPIRES_IN=24h
   ```

2. **HTTPS**
   - Usar HTTPS en producción para proteger tokens en tránsito

3. **Rate Limiting**
   - Implementar límites de intentos de login
   - Prevenir ataques de fuerza bruta

4. **Refresh Tokens**
   - Considerar implementar refresh tokens para mayor seguridad

5. **Auditoría**
   - Registrar intentos de login fallidos
   - Registrar cambios de contraseña

---



### Ejecutar Seeds

```bash
cd backend
npm run seed
```

Esto ejecutará:
1. `00-functional-roles.js` - Crea roles funcionales
2. `00-access-roles.js` - Crea roles de acceso

---

## 📝 Resumen de Archivos Clave

### Backend

| Archivo | Descripción |
|---------|-------------|
| `src/controllers/authController.js` | Lógica de autenticación (login) |
| `src/middleware/authMiddleware.js` | Verificación JWT y middlewares de permisos |
| `src/models/User.js` | Modelo de usuario |
| `src/models/FunctionalRole.js` | Modelo de rol funcional |
| `src/models/AccessRole.js` | Modelo de rol de acceso |
| `src/routes/authRoutes.js` | Rutas de autenticación |
| `seeders/00-functional-roles.js` | Seed de roles funcionales |
| `seeders/00-access-roles.js` | Seed de roles de acceso |
| `seeders/03-users.js` | Seed de usuarios |

### Frontend

| Archivo | Descripción |
|---------|-------------|
| `src/contexts/AuthContext.tsx` | Context de autenticación global |
| `src/pages/LoginPage.tsx` | Página de login |
| `src/services/authApi.ts` | API client de autenticación |
| `src/services/api.ts` | Configuración de Axios con interceptors |
| `src/utils/permissions.ts` | Utilidades de permisos |

---

## 🔄 Flujo Completo de Autenticación

### 1. Usuario Inicia Sesión

```
Usuario → LoginPage → AuthContext.login() → authApi.login()
  ↓
Backend: authController.login()
  ↓
Valida credenciales con servicio externo → Genera JWT → Retorna token + (user role)
  ↓
AuthContext guarda en localStorage y cookies → Actualiza estado
  ↓
Redirige a /dashboard
```

### 2. Usuario Hace Petición Autenticada

```
Componente → authApi.getProfile() → api.get('/auth/profile')
  ↓
Interceptor agrega: Authorization: Bearer <token>
  ↓
Backend: authMiddleware
  ↓
Verifica JWT → Carga usuario → Agrega req.user
  ↓
authController.getProfile() → Retorna datos
```

### 3. Usuario Cierra Sesión

```
Usuario → Navbar.logout() → AuthContext.logout()
  ↓
Limpia localStorage, cockies → Limpia estado 
  ↓
Redirige a /login
```

---

## Envio DE PETICION A SERVICIO EXTERNO 
/auth/login    -- POST
 
{
    "username": "andres.vallejo@yopmail.com",
    "password": "Pruebas123$"
}

## ✅ Checklist de Implementación

- [x] Modelo de usuarios con roles duales
- [x] Hash de contraseñas con bcrypt
- [x] Autenticación JWT
- [x] Middleware de autenticación
- [x] Middleware de permisos
- [x] Context de autenticación en frontend
- [x] Página de login
- [x] Interceptor de Axios para tokens
- [x] Utilidades de permisos
- [x] Seeds de roles y usuarios
- [x] Endpoints de perfil y cambio de contraseña
- [x] Validación de usuarios activos
- [x] Manejo de errores de autenticación

---

