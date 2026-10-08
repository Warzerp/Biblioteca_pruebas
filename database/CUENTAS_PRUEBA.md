# Cuentas y escenarios de prueba

Carga automática de la base (una sola línea, desde la raíz del proyecto o desde esta carpeta):

```bat
database\cargar.bat
```

Ese comando:

1. Crea PostgreSQL `LibreriaDesarrolloDB` si no existe (credenciales de `config/settings.py`).
2. Aplica migraciones Django.
3. Inserta catálogo, ejemplares, usuarios, préstamos, reservas y multas.

Si falla la autenticación, el usuario/clave de PostgreSQL en `DATABASES` de `config/settings.py` no coincide con el servidor local. Ajústalos y vuelve a ejecutar el `.bat`.

Contraseña de **todas** las cuentas de prueba: `Biblioteca2026!`

Frontend: `http://localhost:4200`  
API: `http://localhost:8000/api/v1/`  
Admin Django: `http://localhost:8000/admin/` (usuario `admin`)

---

## Personal de biblioteca

| Usuario | Rol | Para qué usarla |
|---|---|---|
| `admin` | ADMIN | CRUD de libros/autores/categorías, panel Angular `/admin`, Django admin. Superusuario. |
| `biblio` | BIBLIOTECARIO | Gestión de ejemplares y préstamos: crear préstamo, devolver, renovar, pagar/condonar multa. No borra libros (eso es ADMIN). |

Qué probar con `admin` / `biblio`:

- `/admin/dashboard` — contadores de libros, ejemplares, préstamos, reservas, multas y usuarios.
- `/admin/libros` — crear, editar y desactivar un libro.
- `/admin/ejemplares` — dar de alta un ejemplar `EJ-TEST-01`.
- `/admin/prestamos` — prestar un ejemplar DISPONIBLE a `maria.limpia` y luego devolverlo.

---

## Lectores (cada uno con un caso distinto)

| Usuario | Qué tiene cargado | Qué probar |
|---|---|---|
| `ana.lector` | 1 préstamo **activo** (`Cien años de soledad`, ejemplar `EJ-CIEN-01`, vence en ~4 días) y 1 reserva **PENDIENTE** (`Alan Turing: The Enigma`). | `/panel/prestamos` (renovar), `/panel/reservas` (cancelar), catálogo (reservar otro título). |
| `carlos.mora` | Préstamo **CON_MORA** (`Rayuela`, `EJ-RAY-01`, límite vencido hace 6 días) y multa **PENDIENTE** de 3000. | `/panel/multas` muestra la deuda. En catálogo, **Reservar debe fallar** (usuario bloqueado). El bibliotecario tampoco puede prestarle otro ejemplar. |
| `maria.limpia` | Sin préstamos ni multas. Una reserva **CANCELADA** de `Cosmos`. | Cuenta “limpia”: puede reservar y recibir un préstamo nuevo. Úsala para el flujo feliz. |
| `pedro.historial` | Préstamo **DEVUELTO** de `Cosmos` + multa **PAGADA** de 1500, y un préstamo **ACTIVO** de `La casa de los espíritus`. | Historial mixto: multa pagada no bloquea; `/panel/prestamos` muestra activo + devuelto. |
| `lucia.reserva` | 2 reservas **PENDIENTES** (`Harry Potter` y `Clean Code`). Sin préstamos. | Lista de reservas múltiples; cancelar una y dejar la otra. `Clean Code` está en MANTENIMIENTO (no hay stock). |
| `juan.extraviado` | Préstamo **EXTRAVIADO** (`Harry Potter`, `EJ-HP-01`). | Estado especial en préstamos; el ejemplar no vuelve a DISPONIBLE. |

---

## Catálogo de prueba (para filtros y stock)

| Título | Categoría | Stock | Notas |
|---|---|---|---|
| Cien años de soledad | Ficción | 1 disponible + 1 prestado | Búsqueda por “soledad” o autor García Márquez |
| Rayuela | Ficción | Prestado (Carlos) | Sin stock |
| Cosmos | Ciencia | 2 disponibles | Filtro categoría Ciencia |
| Alan Turing: The Enigma | Tecnología | Reservado | Reserva de Ana |
| La casa de los espíritus | Ficción | Prestado (Pedro) | — |
| Residencia en la tierra | Historia | Disponible | Filtro Historia |
| Harry Potter y la piedra filosofal | Infantil | 1 disponible + 1 extraviado | Reserva de Lucía |
| Clean Code | Tecnología | Mantenimiento | Sin stock para préstamo |
| El amor en los tiempos del cólera | Ficción | Extraviado | Sin stock |

---

## Rutas rápidas según rol

1. Login lector → Catálogo → Reservar → Mis reservas / Mis préstamos / Mis multas.
2. Login `biblio` → Panel Admin → Préstamos → prestar a `maria.limpia` un ejemplar DISPONIBLE → Devolver (si se pasa la fecha límite, se genera mora automática de 500 por día).
3. Login `admin` → Libros → alta de ISBN nuevo → Ejemplares → inventario.

---

## Diagrama (3FN)

```
Categoria 1──N Libro N──N Autor
                │
                1
                N
             Ejemplar 1──N Prestamo N──1 Usuario
                              │              │
                              N              N
                            Multa         Reserva
```

Libro = metadato. Ejemplar = unidad física. Multa no guarda título: lo obtiene del préstamo → ejemplar → libro.
