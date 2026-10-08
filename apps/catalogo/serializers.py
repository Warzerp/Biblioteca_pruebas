from rest_framework import serializers
from .models import Categoria, Autor, Libro, Ejemplar


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'


class EjemplarSerializer(serializers.ModelSerializer):
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)

    class Meta:
        model = Ejemplar
        fields = [
            'id', 'libro', 'libro_titulo', 'codigo_inventario',
            'ubicacion_estante', 'estado',
        ]


class LibroSerializer(serializers.ModelSerializer):
    autores = AutorSerializer(many=True, read_only=True)
    autores_ids = serializers.PrimaryKeyRelatedField(
        queryset=Autor.objects.all(), many=True, write_only=True,
        source='autores', required=False,
    )
    ejemplares_disponibles = serializers.IntegerField(read_only=True)
    categoria_detalle = CategoriaSerializer(source='categoria', read_only=True)

    class Meta:
        model = Libro
        fields = [
            'id', 'isbn', 'titulo', 'sinopsis', 'categoria', 'categoria_detalle',
            'autores', 'autores_ids', 'anio_publicacion', 'portada_url',
            'activo', 'creado_en', 'ejemplares_disponibles',
        ]
