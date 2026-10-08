from django.conf import settings
from django.db import models
from apps.prestamos.models import Prestamo


class Multa(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada'),
        ('CONDONADA', 'Condonada'),
    ]
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='multas', verbose_name='Usuario'
    )
    prestamo = models.ForeignKey(
        Prestamo, on_delete=models.CASCADE,
        related_name='multas', verbose_name='Préstamo'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')
    motivo = models.CharField(max_length=255, verbose_name='Motivo')
    estado = models.CharField(
        max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name='Estado'
    )
    fecha_generacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de generación')
    fecha_pago = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de pago')

    class Meta:
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'
        ordering = ['-fecha_generacion']

    def __str__(self):
        return f'Multa #{self.pk} - {self.usuario.username} - ${self.monto}'


class HistorialMulta(models.Model):
    ACCION_CHOICES = [
        ('GENERADA', 'Generada'),
        ('PAGADA', 'Pagada'),
        ('CONDONADA', 'Condonada'),
    ]
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='historial_multas', verbose_name='Usuario'
    )
    multa = models.ForeignKey(
        Multa, on_delete=models.CASCADE,
        related_name='historial', verbose_name='Multa'
    )
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES, verbose_name='Acción')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
    detalle = models.TextField(blank=True, verbose_name='Detalle')

    class Meta:
        verbose_name = 'Historial de multa'
        verbose_name_plural = 'Historial de multas'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.get_accion_display()} - Multa #{self.multa.pk}'
