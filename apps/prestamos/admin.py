from django.contrib import admin
from .models import Reserva, Prestamo, HistorialPrestamo

admin.site.register(Reserva)
admin.site.register(Prestamo)
admin.site.register(HistorialPrestamo)
