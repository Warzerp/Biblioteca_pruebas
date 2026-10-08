from django.conf import settings
from django.db import models
from apps.catalogo.models import Libro, Ejemplar


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ASIGNADA', 'Asignada'),
        ('CANCELADA', 'Cancelada'),
        ('EXPIRADA', 'Expirada'),
        ('COMPLETADA', 'Completada'),
    ]
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='reservas', verbose_name='Usuario'
    )
    libro = models.ForeignKey(
        Libro, on_delete=models.CASCADE,
        related_name='reservas', verbose_name='Libro'
    )
    fecha_reserva = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reserva')
    fecha_expiracion = models.DateTimeField(verbose_name='Fecha de expiración')
    estado = models.CharField(
        max_length=12, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha_reserva']

    def __str__(self):
        return f'Reserva #{self.pk} - {self.usuario.username} - {self.libro.titulo}'


class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('DEVUELTO', 'Devuelto'),
        ('CON_MORA', 'Con mora'),
        ('EXTRAVIADO', 'Extraviado'),
    ]
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='prestamos', verbose_name='Usuario'
    )
    ejemplar = models.ForeignKey(
        Ejemplar, on_delete=models.CASCADE,
        related_name='prestamos', verbose_name='Ejemplar'
    )
    fecha_prestamo = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de préstamo')
    fecha_limite_devolucion = models.DateTimeField(verbose_name='Fecha límite de devolución')
    fecha_devolucion_real = models.DateTimeField(
        null=True, blank=True, verbose_name='Fecha de devolución real'
    )
    estado = models.CharField(
        max_length=12, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name='Estado'
    )
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering = ['-fecha_prestamo']

    def __str__(self):
        return f'Préstamo #{self.pk} - {self.usuario.username} - {self.ejemplar.libro.titulo}'


class HistorialPrestamo(models.Model):
    ACCION_CHOICES = [
        ('CREACION', 'Creación'),
        ('EXTENSION', 'Extensión'),
        ('DEVOLUCION', 'Devolución'),
    ]
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='historial_prestamos', verbose_name='Usuario'
    )
    prestamo = models.ForeignKey(
        Prestamo, on_delete=models.CASCADE,
        related_name='historial', verbose_name='Préstamo'
    )
    accion = models.CharField(max_length=12, choices=ACCION_CHOICES, verbose_name='Acción')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
    detalle = models.TextField(blank=True, verbose_name='Detalle')

    class Meta:
        verbose_name = 'Historial de préstamo'
        verbose_name_plural = 'Historial de préstamos'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.get_accion_display()} - Préstamo #{self.prestamo.pk}'
