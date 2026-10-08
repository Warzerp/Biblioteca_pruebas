from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Categoria, Autor, Libro, Ejemplar
from .serializers import CategoriaSerializer, AutorSerializer, LibroSerializer, EjemplarSerializer
from apps.usuarios.permissions import EsAdmin, EsBibliotecario


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [EsAdmin()]
        return [IsAuthenticatedOrReadOnly()]


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [EsAdmin()]
        return [IsAuthenticatedOrReadOnly()]


class LibroViewSet(viewsets.ModelViewSet):
    serializer_class = LibroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'isbn', 'autores__nombre']

    def get_queryset(self):
        qs = Libro.objects.filter(activo=True).select_related('categoria').prefetch_related('autores', 'ejemplares')
        categoria = self.request.query_params.get('categoria')
        disponible = self.request.query_params.get('disponible')
        if categoria:
            qs = qs.filter(categoria_id=categoria)
        if disponible == 'true':
            qs = qs.filter(ejemplares__estado='DISPONIBLE').distinct()
        return qs

    def get_permissions(self):
        if self.action == 'destroy':
            return [EsAdmin()]
        if self.action in ['create', 'update', 'partial_update']:
            return [EsBibliotecario()]
        return [IsAuthenticatedOrReadOnly()]

    def perform_destroy(self, instance):
        instance.activo = False
        instance.save()


class EjemplarViewSet(viewsets.ModelViewSet):
    queryset = Ejemplar.objects.select_related('libro').all()
    serializer_class = EjemplarSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['codigo_inventario', 'libro__titulo']

    def get_permissions(self):
        return [EsBibliotecario()]
