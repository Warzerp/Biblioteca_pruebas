from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nickname", "correo", "telefono", "password", "activo")
    search_fields = ("nombre", "nickname", "correo")
    list_filter = ("activo",)
    
