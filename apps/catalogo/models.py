from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    nacionalidad = models.CharField(max_length=100, blank=True, verbose_name='Nacionalidad')
    biografia = models.TextField(blank=True, verbose_name='Biografía')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    isbn = models.CharField(max_length=20, unique=True, verbose_name='ISBN')
    titulo = models.CharField(max_length=300, verbose_name='Título')
    sinopsis = models.TextField(blank=True, verbose_name='Sinopsis')
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='libros', verbose_name='Categoría'
    )
    autores = models.ManyToManyField(Autor, related_name='libros', verbose_name='Autores')
    anio_publicacion = models.PositiveIntegerField(null=True, blank=True, verbose_name='Año de publicación')
    portada_url = models.URLField(blank=True, verbose_name='URL de portada')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo} ({self.isbn})'

    @property
    def ejemplares_disponibles(self):
        return self.ejemplares.filter(estado='DISPONIBLE').count()


class Ejemplar(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('PRESTADO', 'Prestado'),
        ('RESERVADO', 'Reservado'),
        ('MANTENIMIENTO', 'En mantenimiento'),
        ('EXTRAVIADO', 'Extraviado'),
    ]
    libro = models.ForeignKey(
        Libro, on_delete=models.CASCADE,
        related_name='ejemplares', verbose_name='Libro'
    )
    codigo_inventario = models.CharField(max_length=50, unique=True, verbose_name='Código de inventario')
    ubicacion_estante = models.CharField(max_length=100, blank=True, verbose_name='Ubicación en estante')
    estado = models.CharField(
        max_length=15, choices=ESTADO_CHOICES, default='DISPONIBLE', verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Ejemplar'
        verbose_name_plural = 'Ejemplares'

    def __str__(self):
        return f'{self.codigo_inventario} - {self.libro.titulo} [{self.get_estado_display()}]'
