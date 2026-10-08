from django.contrib import admin
from .models import Categoria, Autor, Libro, Ejemplar

class EjemplarInline(admin.TabularInline):
    model = Ejemplar
    extra = 1

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    inlines = [EjemplarInline]
    list_display = ['titulo', 'isbn', 'categoria', 'activo']
    search_fields = ['titulo', 'isbn']

admin.site.register(Categoria)
admin.site.register(Autor)
admin.site.register(Ejemplar)
