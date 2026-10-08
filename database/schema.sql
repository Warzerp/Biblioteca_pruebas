-- =============================================================================
-- Biblioteca Digital — esquema de dominio (PostgreSQL)
-- Tablas alineadas a los modelos Django (nombres reales de migrate).
--
-- Instalación automática (recomendado):
--   database\cargar.bat
--
-- Ese comando crea la BD, aplica migraciones Django y carga datos de prueba.
-- Este archivo documenta 1FN / 2FN / 3FN y las relaciones.
-- =============================================================================

-- usuarios_customuser: autenticación + rol de negocio (no se mezcla con préstamos).
-- catalogo_*: metadato bibliográfico separado del ejemplar físico.
-- prestamos_*: reservas y préstamos dependen de usuario + libro/ejemplar.
-- multas_*: multa depende del préstamo (no se duplican datos del libro).

CREATE TABLE IF NOT EXISTS catalogo_categoria (
    id              BIGSERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL UNIQUE,
    descripcion     TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS catalogo_autor (
    id              BIGSERIAL PRIMARY KEY,
    nombre          VARCHAR(200) NOT NULL,
    nacionalidad    VARCHAR(100) NOT NULL DEFAULT '',
    biografia       TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS catalogo_libro (
    id                  BIGSERIAL PRIMARY KEY,
    isbn                VARCHAR(20) NOT NULL UNIQUE,
    titulo              VARCHAR(300) NOT NULL,
    sinopsis            TEXT NOT NULL DEFAULT '',
    categoria_id        BIGINT NULL REFERENCES catalogo_categoria(id) ON DELETE SET NULL,
    anio_publicacion    INTEGER NULL,
    portada_url         VARCHAR(200) NOT NULL DEFAULT '',
    activo              BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS catalogo_libro_autores (
    id          BIGSERIAL PRIMARY KEY,
    libro_id    BIGINT NOT NULL REFERENCES catalogo_libro(id) ON DELETE CASCADE,
    autor_id    BIGINT NOT NULL REFERENCES catalogo_autor(id) ON DELETE CASCADE,
    UNIQUE (libro_id, autor_id)
);

CREATE TABLE IF NOT EXISTS catalogo_ejemplar (
    id                  BIGSERIAL PRIMARY KEY,
    libro_id            BIGINT NOT NULL REFERENCES catalogo_libro(id) ON DELETE CASCADE,
    codigo_inventario   VARCHAR(50) NOT NULL UNIQUE,
    ubicacion_estante   VARCHAR(100) NOT NULL DEFAULT '',
    estado              VARCHAR(15) NOT NULL DEFAULT 'DISPONIBLE'
);

CREATE TABLE IF NOT EXISTS prestamos_reserva (
    id                  BIGSERIAL PRIMARY KEY,
    usuario_id          BIGINT NOT NULL REFERENCES usuarios_customuser(id) ON DELETE CASCADE,
    libro_id            BIGINT NOT NULL REFERENCES catalogo_libro(id) ON DELETE CASCADE,
    fecha_reserva       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_expiracion    TIMESTAMPTZ NOT NULL,
    estado              VARCHAR(12) NOT NULL DEFAULT 'PENDIENTE'
);

CREATE TABLE IF NOT EXISTS prestamos_prestamo (
    id                          BIGSERIAL PRIMARY KEY,
    usuario_id                  BIGINT NOT NULL REFERENCES usuarios_customuser(id) ON DELETE CASCADE,
    ejemplar_id                 BIGINT NOT NULL REFERENCES catalogo_ejemplar(id) ON DELETE CASCADE,
    fecha_prestamo              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_limite_devolucion     TIMESTAMPTZ NOT NULL,
    fecha_devolucion_real       TIMESTAMPTZ NULL,
    estado                      VARCHAR(12) NOT NULL DEFAULT 'ACTIVO',
    observaciones               TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS prestamos_historialprestamo (
    id              BIGSERIAL PRIMARY KEY,
    usuario_id      BIGINT NOT NULL REFERENCES usuarios_customuser(id) ON DELETE CASCADE,
    prestamo_id     BIGINT NOT NULL REFERENCES prestamos_prestamo(id) ON DELETE CASCADE,
    accion          VARCHAR(12) NOT NULL,
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    detalle         TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS multas_multa (
    id                  BIGSERIAL PRIMARY KEY,
    usuario_id          BIGINT NOT NULL REFERENCES usuarios_customuser(id) ON DELETE CASCADE,
    prestamo_id         BIGINT NOT NULL REFERENCES prestamos_prestamo(id) ON DELETE CASCADE,
    monto               NUMERIC(10, 2) NOT NULL,
    motivo              VARCHAR(255) NOT NULL,
    estado              VARCHAR(10) NOT NULL DEFAULT 'PENDIENTE',
    fecha_generacion    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_pago          TIMESTAMPTZ NULL
);

CREATE TABLE IF NOT EXISTS multas_historialmulta (
    id              BIGSERIAL PRIMARY KEY,
    usuario_id      BIGINT NOT NULL REFERENCES usuarios_customuser(id) ON DELETE CASCADE,
    multa_id        BIGINT NOT NULL REFERENCES multas_multa(id) ON DELETE CASCADE,
    accion          VARCHAR(10) NOT NULL,
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    detalle         TEXT NOT NULL DEFAULT ''
);

-- Cardinalidades:
-- Categoria 1:N Libro
-- Autor N:M Libro
-- Libro 1:N Ejemplar
-- Usuario 1:N Reserva, Prestamo, Multa
-- Prestamo 1:N Multa / HistorialPrestamo
-- Multa 1:N HistorialMulta
