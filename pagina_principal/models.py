from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=120)
    nickname = models.CharField(max_length=120)
    correo = models.EmailField()
    telefono = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

