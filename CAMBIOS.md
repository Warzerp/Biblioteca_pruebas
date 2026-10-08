#  Registro de Correcciones y Mejoras
## Proyecto: Biblioteca Digital y Sistema de Préstamos

> **Fecha de implementación:** Octubre 2026  
> **Estado anterior:** Prototipo monolítico Django con plantillas HTML básicas  
> **Estado actual:** Arquitectura desacoplada completa — Django REST API + Angular 17 SPA

---

##  Correcciones Críticas

### 1. Seguridad: Contraseña en texto plano → Hashing seguro

| | Antes | Después |
|---|---|---|
| **Archivo** | [`pagina_principal/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/pagina_principal/models.py) | [`apps/usuarios/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/usuarios/models.py) |
| **Código** | `password = models.CharField(max_length=120)` | Hereda `AbstractUser` → `set_password()` con PBKDF2 |
| **Riesgo** | � Crítico — datos comprometidos ante cualquier filtración de BD | ✅ Contraseñas hasheadas con sal |

**Problema**: El modelo `Usuario` original guardaba la contraseña como `CharField` en texto plano, sin ningún cifrado. Esto es una vulnerabilidad crítica de seguridad.

**Solución**: Se reemplazó por un `CustomUser` que extiende `AbstractUser` de Django, obteniendo automáticamente hashing seguro con PBKDF2-SHA256 y manejo de permisos del sistema.

---

### 2. CORS: Protocolo incorrecto (HTTPS → HTTP)

| | Antes | Después |
|---|---|---|
| **Archivo** | [`config/settings.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/config/settings.py) | [`config/settings.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/config/settings.py) |
| **Valor** | `"https://localhost:4200"` | `"http://localhost:4200"`, `"http://127.0.0.1:4200"` |
| **Efecto** | ❌ Angular CLI no se podía comunicar con el backend (todas las peticiones bloqueadas) | ✅ Comunicación frontend-backend operativa |

**Problema**: Angular CLI (`ng serve`) corre por defecto en HTTP, pero `CORS_ALLOWED_ORIGINS` apuntaba a HTTPS. Esto bloqueaba 100% de las peticiones del frontend.

---

### 3. Eliminación de `pagina_principal` como app de rendering

| | Antes | Después |
|---|---|---|
| **Rol** | App Django que renderizaba HTML con `render()` | Eliminada del ciclo activo de vistas |
| **Problema** | Mezcla de responsabilidades; Django no puede ser simultáneamente servidor de plantillas y API REST limpia | Toda la lógica de vistas migra a Angular; Django solo devuelve JSON |

Las vistas `principal()`, `catalogo()`, `reservar()` y `sesion()` en `pagina_principal/views.py` retornaban HTML directamente — incompatible con la arquitectura SPA Angular planificada.

---

### 4. Modelo de datos incompleto → Normalización completa (FN3)

El modelo original tenía únicamente la tabla `Usuario`. Se implementó el esquema completo normalizado según el diseño del archivo `DB/Base de Datos.xlsx`:

| Tabla | Estado anterior | Implementada en |
|---|---|---|
| `CustomUser` | Parcial (sin roles, contraseña insegura) | [`apps/usuarios/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/usuarios/models.py) |
| `Categoria` | ❌ No existía | [`apps/catalogo/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/catalogo/models.py) |
| `Autor` | ❌ No existía | [`apps/catalogo/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/catalogo/models.py) |
| `Libro` | ❌ No existía | [`apps/catalogo/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/catalogo/models.py) |
| `Ejemplar` | ❌ No existía | [`apps/catalogo/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/catalogo/models.py) |
| `Reserva` | ❌ No existía | [`apps/prestamos/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/prestamos/models.py) |
| `Prestamo` | ❌ No existía | [`apps/prestamos/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/prestamos/models.py) |
| `HistorialPrestamo` | ❌ No existía | [`apps/prestamos/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/prestamos/models.py) |
| `Multa` | ❌ No existía | [`apps/multas/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/multas/models.py) |
| `HistorialMulta` | ❌ No existía | [`apps/multas/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/multas/models.py) |

---

##  Mejoras Estructurales

### 5. Modularización del backend: Monolito → Apps por dominio

**Antes**: Una sola app `pagina_principal` con todo mezclado.

**Después**: Cuatro apps especializadas con separación de responsabilidades clara:

```
apps/
├── usuarios/     → Autenticación, roles, perfiles
├── catalogo/     → Libros, autores, categorías, ejemplares
├── prestamos/    → Reservas, préstamos, historial de préstamos
└── multas/       → Multas, historial de multas, servicios de cálculo
```

Cada app tiene su propio ciclo completo:
- `models.py` → Entidades de base de datos
- `serializers.py` → Transformación JSON ↔ Python
- `views.py` → Lógica de respuesta HTTP
- `urls.py` → Enrutamiento propio
- `admin.py` → Panel administrativo Django
- `apps.py` → Configuración de la app

---

### 6. Autenticación: Sin sistema → JWT con SimpleJWT

**Antes**: La vista `sesion()` usaba `UsuarioForm` y `form.save()` sin autenticación real ni tokens.

**Después**: Sistema JWT completo implementado:

| Endpoint | Función |
|---|---|
| `POST /api/v1/auth/login/` | Obtiene par `access`/`refresh` tokens |
| `POST /api/v1/auth/refresh/` | Refresca el access token expirado |
| `POST /api/v1/auth/registro/` | Crea usuario nuevo (rol LECTOR) |
| `GET /api/v1/auth/perfil/` | Devuelve datos del usuario autenticado |

Configuración añadida en [`config/settings.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/config/settings.py):
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

---

### 7. Sistema de permisos granular por rol

Se creó [`apps/usuarios/permissions.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/usuarios/permissions.py) con permisos DRF personalizados:

| Permiso | Aplicado en |
|---|---|
| `EsBibliotecario` | Endpoints de gestión de préstamos y ejemplares |
| `EsAdmin` | Operaciones de borrado de registros |
| `EsPropietarioOAdmin` | Cancelación de reservas (solo tu propia reserva o un admin) |

---

### 8. Lógica de negocio separada en servicios (`services.py`)

Se extrajeron las reglas de negocio a módulos de servicio dedicados:

**[`apps/prestamos/services.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/prestamos/services.py)**:
- `calcular_fecha_limite(dias)` — fecha límite de devolución
- `calcular_fecha_expiracion_reserva(dias)` — expiración de reservas (48h)
- `calcular_mora(fecha_limite, fecha_real)` — tarifa por días de retraso
- `usuario_bloqueado(usuario)` — valida si tiene multas pendientes antes de prestar

**[`apps/multas/services.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/multas/services.py)**:
- `registrar_pago_multa(multa, usuario, condonada)` — procesa pago o condonación y crea entrada en historial

---

### 9. Paginación y filtros en la API REST

`config/settings.py` configura paginación global:
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

Los ViewSets de catálogo soportan filtrado por `?search=titulo`, `?categoria=id`, `?disponible=true`.

---

### 10. Localización correcta

| Configuración | Antes | Después |
|---|---|---|
| `LANGUAGE_CODE` | `'en-us'` | `'es'` |
| `TIME_ZONE` | `'UTC'` | `'America/Santiago'` |
| `USE_TZ` | `True` | `True` (correcto, para aware datetimes) |

---

##  Nuevas Funcionalidades Implementadas

### 11. Frontend Angular 17+ completo desde cero

No existía ningún proyecto Angular. Se creó en [`frontend/`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/) la aplicación completa:

#### Módulo `core/` — Infraestructura base
| Archivo | Función |
|---|---|
| [`auth.service.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/core/services/auth.service.ts) | Manejo de sesión con Signals (`_usuario`, `isLoggedIn`, `esAdmin`) |
| [`auth.interceptor.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/core/interceptors/auth.interceptor.ts) | Inyecta automáticamente `Authorization: Bearer <token>` en cada request |
| [`error.interceptor.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/core/interceptors/error.interceptor.ts) | Redirige a `/login` en 401, a `/` en 403 |
| [`auth.guard.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/core/guards/auth.guard.ts) | Protege rutas privadas (`/panel/*`) |
| [`role.guard.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/core/guards/role.guard.ts) | Protege rutas de admin (`/admin/*`) según rol del usuario |

#### Módulo `shared/` — Componentes reutilizables
| Componente | Descripción |
|---|---|
| [`navbar`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/shared/components/navbar/navbar.component.ts) | Barra de navegación reactiva (muestra links según login/rol) |
| [`footer`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/shared/components/footer/footer.component.ts) | Pie de página con datos de contacto |
| [`book-card`](file:///c:/Users/USUARIO/Desktop\DOAP%20-%20copia/frontend/src/app/shared/components/book-card/book-card.component.ts) | Tarjeta de libro con portada, disponibilidad y botón de reserva |
| [`alert-modal`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/shared/components/alert-modal/alert-modal.component.ts) | Modal de confirmación genérico |

#### Módulo `features/` — Funcionalidades de negocio

| Feature | Páginas | Servicio |
|---|---|---|
| `auth` | Login, Registro | [`auth.service.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/core/services/auth.service.ts) |
| `catalogo` | Lista con filtros, Detalle de libro | [`catalogo.service.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/features/catalogo/services/catalogo.service.ts) |
| `reservas` | Mis Reservas (lector) | [`reserva.service.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/features/reservas/services/reserva.service.ts) |
| `prestamos` | Mis Préstamos (lector), Gestión (admin) | [`prestamo.service.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/features/prestamos/services/prestamo.service.ts) |
| `multas` | Mis Multas (lector) | [`multa.service.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/features/multas/services/multa.service.ts) |
| `admin` | Dashboard, CRUD Libros, CRUD Ejemplares | [`admin.service.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/features/admin/services/admin.service.ts) |

#### Modelos TypeScript (`models/`) — Tipado estricto

Seis interfaces alineadas al 100% con los serializers del backend:
- [`usuario.model.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/models/usuario.model.ts) — `Usuario`, `LoginRequest`, `LoginResponse`, `RegistroRequest`
- [`libro.model.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/models/libro.model.ts) — `Libro`, `Autor`, `Categoria`, `PaginatedResponse<T>`
- [`ejemplar.model.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/models/ejemplar.model.ts) — `Ejemplar`, `EstadoEjemplar`
- [`reserva.model.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/models/reserva.model.ts) — `Reserva`, `EstadoReserva`
- [`prestamo.model.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/models/prestamo.model.ts) — `Prestamo`, `EstadoPrestamo`
- [`multa.model.ts`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/frontend/src/app/models/multa.model.ts) — `Multa`, `EstadoMulta`

---

### 12. Registro de auditoría (Historial)

Se implementaron tablas de auditoría completas con trazabilidad de acciones:

- **`HistorialPrestamo`**: registra cada `CREACION`, `EXTENSION` o `DEVOLUCION` de un préstamo con timestamp y detalle.
- **`HistorialMulta`**: registra cuando una multa fue `GENERADA`, `PAGADA` o `CONDONADA`, incluyendo quién la procesó.

---

### 13. Distinción Libro / Ejemplar (Patrón Físico vs. Metadato)

**Antes**: No existía distinción — no había ni `Libro` ni `Ejemplar` implementados.

**Después**: Separación clara implementada en [`apps/catalogo/models.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/apps/catalogo/models.py):

- `Libro` → Datos bibliográficos compartidos (ISBN, título, sinopsis, autores M:N, categoría)
- `Ejemplar` → Unidad física individual con `codigo_inventario` único y `estado` propio
- Property calculada `libro.ejemplares_disponibles` para stock en tiempo real sin queries adicionales

---

### 14. Media files y configuración de producción

Se añadieron en [`config/settings.py`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/config/settings.py):
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
Y se creó la carpeta [`media/.gitkeep`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/media/.gitkeep) para que git rastree el directorio de subida de portadas.

---

### 15. requirements.txt

Se creó [`requirements.txt`](file:///c:/Users/USUARIO/Desktop/DOAP%20-%20copia/requirements.txt) en la raíz con las dependencias exactas del proyecto:

```
Django>=5.0
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
django-cors-headers>=4.3
psycopg2-binary>=2.9
```

---

##  Resumen de Archivos por Categoría

### Backend (Django REST Framework)
| Categoría | Archivos nuevos | Archivos modificados |
|---|---|---|
| Configuración | — | `config/settings.py`, `config/urls.py` |
| App `usuarios` | 6 archivos | — |
| App `catalogo` | 6 archivos | — |
| App `prestamos` | 7 archivos | — |
| App `multas` | 7 archivos | — |
| Infraestructura | `requirements.txt`, `media/.gitkeep` | — |
| **Total backend** | **28 archivos nuevos** | **2 modificados** |

### Frontend (Angular 17+)
| Categoría | Archivos nuevos |
|---|---|
| Configuración raíz | `package.json`, `tsconfig.json`, `angular.json` |
| Bootstrap | `src/index.html`, `src/main.ts`, `src/styles.css` |
| App raíz | `app.component.ts`, `app.config.ts`, `app.routes.ts` |
| Core | 5 archivos (guards, interceptors, service) |
| Shared | 5 archivos (components, pipe) |
| Models | 6 archivos (interfaces TypeScript) |
| Features | 19 archivos (components + services) |
| **Total frontend** | **42 archivos nuevos** |

---

##  Pasos para Poner en Marcha

### Backend Django
```bash
# 1. Activar el entorno virtual
.\.venv\Scripts\activate

# 2. Instalar nuevas dependencias
pip install djangorestframework-simplejwt

# 3. Crear y aplicar migraciones del nuevo esquema
python manage.py makemigrations usuarios catalogo prestamos multas
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Iniciar el servidor
python manage.py runserver
```

### Frontend Angular
```bash
# Desde la carpeta frontend/
cd frontend

# 1. Instalar dependencias Node.js
npm install

# 2. Iniciar el servidor de desarrollo
npm start
# → Disponible en http://localhost:4200
```

> [!IMPORTANT]
> El backend debe estar corriendo en `http://localhost:8000` antes de iniciar el frontend.

> [!NOTE]
> Si `npm install` da error por falta de Node.js/Angular CLI, descarga Node.js LTS desde https://nodejs.org e instala Angular CLI con `npm install -g @angular/cli`.


### 16. Mejoras Estéticas de la Interfaz
Se reescribió styles.css utilizando una paleta de colores moderna inspirada en Tailwind CSS (Slate, Sky). Se mejoró la tipografía, el espaciado, y se añadieron sombras sutiles (box-shadow) para un aspecto más profesional. Se eliminaron todos los emojis decorativos para mantener un tono formal en toda la aplicación.
