from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROL_CHOICES = [
        ('LECTOR', 'Lector'),
        ('BIBLIOTECARIO', 'Bibliotecario'),
        ('ADMIN', 'Administrador'),
    ]
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='LECTOR', verbose_name='Rol')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'

    @property
    def tiene_multas_pendientes(self):
        return self.multas.filter(estado='PENDIENTE').exists()
