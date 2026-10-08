from django.utils import timezone
from .models import Multa, HistorialMulta


def registrar_pago_multa(multa, usuario_quien_paga, condonada=False):
    """
    Marca una multa como PAGADA o CONDONADA y crea el registro en historial.
    """
    if multa.estado != 'PENDIENTE':
        raise ValueError('Solo se pueden pagar multas en estado PENDIENTE.')

    accion = 'CONDONADA' if condonada else 'PAGADA'
    detalle = f'Procesado por: {usuario_quien_paga.username}'

    multa.estado = accion
    multa.fecha_pago = timezone.now()
    multa.save()

    HistorialMulta.objects.create(
        usuario=multa.usuario,
        multa=multa,
        accion=accion,
        detalle=detalle,
    )
    return multa
