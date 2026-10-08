from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


TARIFA_MORA_DIARIA = Decimal('500.00')  # En pesos o la moneda local
DIAS_PRESTAMO_DEFAULT = 7
DIAS_EXPIRACION_RESERVA = 2


def calcular_fecha_limite(dias=DIAS_PRESTAMO_DEFAULT):
    """Retorna la fecha límite de devolución a partir de ahora."""
    return timezone.now() + timedelta(days=dias)


def calcular_fecha_expiracion_reserva(dias=DIAS_EXPIRACION_RESERVA):
    """Retorna la fecha de expiración de una reserva a partir de ahora."""
    return timezone.now() + timedelta(days=dias)


def calcular_mora(fecha_limite, fecha_devolucion_real):
    """
    Calcula el monto de mora dado que el libro fue devuelto tarde.
    Retorna Decimal 0.00 si no hay mora.
    """
    if fecha_devolucion_real <= fecha_limite:
        return Decimal('0.00')
    dias_retraso = (fecha_devolucion_real.date() - fecha_limite.date()).days
    return TARIFA_MORA_DIARIA * dias_retraso


def usuario_bloqueado(usuario):
    """Retorna True si el usuario tiene multas pendientes."""
    return usuario.multas.filter(estado='PENDIENTE').exists()
