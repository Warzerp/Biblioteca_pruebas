"""Carga catálogo, usuarios, préstamos, reservas y multas de demostración."""
import os
import sys
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.db import transaction  # noqa: E402
from django.utils import timezone  # noqa: E402

from apps.catalogo.models import Autor, Categoria, Ejemplar, Libro  # noqa: E402
from apps.multas.models import HistorialMulta, Multa  # noqa: E402
from apps.prestamos.models import HistorialPrestamo, Prestamo, Reserva  # noqa: E402

User = get_user_model()
PASSWORD = 'Biblioteca2026!'
RESET = '--reset' in sys.argv


def user(username, **kwargs):
    defaults = {
        'email': f'{username}@biblioteca.test',
        'rol': 'LECTOR',
        'is_staff': False,
        'is_superuser': False,
        'is_active': True,
    }
    defaults.update(kwargs)
    obj, created = User.objects.get_or_create(username=username, defaults=defaults)
    obj.set_password(PASSWORD)
    for key, value in defaults.items():
        setattr(obj, key, value)
    obj.save()
    return obj


@transaction.atomic
def run():
    if RESET:
        HistorialMulta.objects.all().delete()
        Multa.objects.all().delete()
        HistorialPrestamo.objects.all().delete()
        Prestamo.objects.all().delete()
        Reserva.objects.all().delete()
        Ejemplar.objects.all().delete()
        Libro.objects.all().delete()
        Autor.objects.all().delete()
        Categoria.objects.all().delete()
        User.objects.filter(email__endswith='@biblioteca.test').delete()

    now = timezone.now()

    ficcion = Categoria.objects.create(nombre='Ficción', descripcion='Novela y narrativa')
    ciencia = Categoria.objects.create(nombre='Ciencia', descripcion='Divulgación científica')
    historia = Categoria.objects.create(nombre='Historia', descripcion='Historia general')
    infantil = Categoria.objects.create(nombre='Infantil', descripcion='Literatura infantil')
    tecnologia = Categoria.objects.create(nombre='Tecnología', descripcion='Informática y sistemas')

    autores = {
        'garcia': Autor.objects.create(nombre='Gabriel García Márquez', nacionalidad='Colombia'),
        'cortazar': Autor.objects.create(nombre='Julio Cortázar', nacionalidad='Argentina'),
        'sagan': Autor.objects.create(nombre='Carl Sagan', nacionalidad='Estados Unidos'),
        'turing': Autor.objects.create(nombre='Andrew Hodges', nacionalidad='Reino Unido'),
        'allende': Autor.objects.create(nombre='Isabel Allende', nacionalidad='Chile'),
        'neruda': Autor.objects.create(nombre='Pablo Neruda', nacionalidad='Chile'),
        'rowling': Autor.objects.create(nombre='J. K. Rowling', nacionalidad='Reino Unido'),
        'martin': Autor.objects.create(nombre='Robert C. Martin', nacionalidad='Estados Unidos'),
    }

    def libro(isbn, titulo, categoria, autor_keys, anio, sinopsis, portada=''):
        item = Libro.objects.create(
            isbn=isbn, titulo=titulo, categoria=categoria,
            anio_publicacion=anio, sinopsis=sinopsis, portada_url=portada, activo=True,
        )
        for key in autor_keys:
            item.autores.add(autores[key])
        return item

    cien = libro('9780307474728', 'Cien años de soledad', ficcion, ['garcia'], 1967,
                 'Saga de la familia Buendía en Macondo.')
    rayuela = libro('9788437604572', 'Rayuela', ficcion, ['cortazar'], 1963,
                    'Novela antinovelística de hopscotch parisino.')
    cosmos = libro('9780345539434', 'Cosmos', ciencia, ['sagan'], 1980,
                   'Recorrido por el universo y la ciencia.')
    turing = libro('9780691164724', 'Alan Turing: The Enigma', tecnologia, ['turing'], 1983,
                   'Biografía del matemático Alan Turing.')
    casa = libro('9781501117015', 'La casa de los espíritus', ficcion, ['allende'], 1982,
                 'Saga familiar chilena con realismo mágico.')
    resid = libro('9788437604947', 'Residencia en la tierra', historia, ['neruda'], 1935,
                  'Poesía de Neruda en su etapa de madurez.')
    harry = libro('9788478884452', 'Harry Potter y la piedra filosofal', infantil, ['rowling'], 1997,
                  'Primer año de Harry en Hogwarts.')
    clean = libro('9780132350884', 'Clean Code', tecnologia, ['martin'], 2008,
                  'Principios para escribir código mantenible.')
    soledad2 = libro('9788497592208', 'El amor en los tiempos del cólera', ficcion, ['garcia'], 1985,
                     'Historia de amor a lo largo de décadas.')

    ejemplares = {}
    stock = [
        (cien, 'EJ-CIEN-01', 'A-1', 'PRESTADO'),
        (cien, 'EJ-CIEN-02', 'A-1', 'DISPONIBLE'),
        (rayuela, 'EJ-RAY-01', 'A-2', 'PRESTADO'),
        (cosmos, 'EJ-COS-01', 'B-1', 'PRESTADO'),
        (cosmos, 'EJ-COS-02', 'B-1', 'DISPONIBLE'),
        (turing, 'EJ-TUR-01', 'C-1', 'RESERVADO'),
        (casa, 'EJ-CASA-01', 'A-3', 'PRESTADO'),
        (resid, 'EJ-RES-01', 'D-1', 'DISPONIBLE'),
        (harry, 'EJ-HP-01', 'E-1', 'PRESTADO'),
        (harry, 'EJ-HP-02', 'E-1', 'DISPONIBLE'),
        (clean, 'EJ-CC-01', 'C-2', 'MANTENIMIENTO'),
        (soledad2, 'EJ-COL-01', 'A-4', 'EXTRAVIADO'),
    ]
    for libro_obj, codigo, estante, estado in stock:
        ejemplares[codigo] = Ejemplar.objects.create(
            libro=libro_obj, codigo_inventario=codigo,
            ubicacion_estante=estante, estado=estado,
        )

    admin = user(
        'admin', first_name='Ana', last_name='Admin', rol='ADMIN',
        is_staff=True, is_superuser=True, telefono='+56911111111',
    )
    biblio = user(
        'biblio', first_name='Bruno', last_name='Bibliotecario', rol='BIBLIOTECARIO',
        is_staff=True, telefono='+56922222222',
    )
    ana = user('ana.lector', first_name='Ana', last_name='Lector', telefono='+56933333333')
    carlos = user('carlos.mora', first_name='Carlos', last_name='Mora', telefono='+56944444444')
    maria = user('maria.limpia', first_name='María', last_name='Limpia', telefono='+56955555555')
    pedro = user('pedro.historial', first_name='Pedro', last_name='Historial', telefono='+56966666666')
    lucia = user('lucia.reserva', first_name='Lucía', last_name='Reserva', telefono='+56977777777')
    juan = user('juan.extraviado', first_name='Juan', last_name='Extraviado', telefono='+56988888888')

    def prestamo(usuario, codigo, fecha, limite, estado='ACTIVO', devolucion=None, obs=''):
        p = Prestamo.objects.create(
            usuario=usuario,
            ejemplar=ejemplares[codigo],
            fecha_limite_devolucion=limite,
            estado=estado,
            observaciones=obs,
            fecha_devolucion_real=devolucion,
        )
        Prestamo.objects.filter(pk=p.pk).update(fecha_prestamo=fecha)
        p.refresh_from_db()
        HistorialPrestamo.objects.create(usuario=usuario, prestamo=p, accion='CREACION')
        if estado in ['DEVUELTO', 'CON_MORA'] and devolucion:
            HistorialPrestamo.objects.create(usuario=biblio, prestamo=p, accion='DEVOLUCION', detalle='Carga inicial')
        return p

    p_ana = prestamo(ana, 'EJ-CIEN-01', now - timedelta(days=3), now + timedelta(days=4))
    p_carlos = prestamo(
        carlos, 'EJ-RAY-01', now - timedelta(days=20), now - timedelta(days=6), estado='CON_MORA',
        obs='Atraso de 6 días',
    )
    p_pedro_old = prestamo(
        pedro, 'EJ-COS-01', now - timedelta(days=40), now - timedelta(days=33),
        estado='DEVUELTO', devolucion=now - timedelta(days=30),
    )
    # Cosmos EJ-COS-01 quedó PRESTADO en el catálogo de stock; el préstamo de Pedro ya se devolvió.
    ejemplares['EJ-COS-01'].estado = 'DISPONIBLE'
    ejemplares['EJ-COS-01'].save()
    p_pedro_activo = prestamo(pedro, 'EJ-CASA-01', now - timedelta(days=2), now + timedelta(days=5))
    p_juan = prestamo(
        juan, 'EJ-HP-01', now - timedelta(days=12), now - timedelta(days=5),
        estado='EXTRAVIADO', obs='No localizado en inventario',
    )
    ejemplares['EJ-HP-01'].estado = 'EXTRAVIADO'
    ejemplares['EJ-HP-01'].save()

    Reserva.objects.create(
        usuario=ana, libro=turing, fecha_expiracion=now + timedelta(days=2), estado='PENDIENTE',
    )
    Reserva.objects.create(
        usuario=lucia, libro=harry, fecha_expiracion=now + timedelta(days=1), estado='PENDIENTE',
    )
    Reserva.objects.create(
        usuario=lucia, libro=clean, fecha_expiracion=now + timedelta(hours=10), estado='PENDIENTE',
    )
    Reserva.objects.create(
        usuario=pedro, libro=cien, fecha_expiracion=now - timedelta(days=1), estado='EXPIRADA',
    )
    Reserva.objects.create(
        usuario=maria, libro=cosmos, fecha_expiracion=now + timedelta(days=2), estado='CANCELADA',
    )

    multa_carlos = Multa.objects.create(
        usuario=carlos, prestamo=p_carlos, monto=Decimal('3000.00'),
        motivo='Atraso de 6 días (tarifa 500/día)', estado='PENDIENTE',
    )
    HistorialMulta.objects.create(usuario=carlos, multa=multa_carlos, accion='GENERADA', detalle='Seed')

    multa_pedro = Multa.objects.create(
        usuario=pedro, prestamo=p_pedro_old, monto=Decimal('1500.00'),
        motivo='Atraso histórico ya pagado', estado='PAGADA', fecha_pago=now - timedelta(days=28),
    )
    HistorialMulta.objects.create(usuario=pedro, multa=multa_pedro, accion='GENERADA')
    HistorialMulta.objects.create(
        usuario=biblio, multa=multa_pedro, accion='PAGADA', detalle='Pagada en caja',
    )

    print('Seed completado.')
    print(f'Contraseña de todas las cuentas de prueba: {PASSWORD}')
    print('Detalle: database/CUENTAS_PRUEBA.md')
    _ = (admin, biblio, maria, p_ana, p_pedro_activo, p_juan)


if __name__ == '__main__':
    run()
