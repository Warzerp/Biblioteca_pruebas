from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, AutorViewSet, LibroViewSet, EjemplarViewSet

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('autores', AutorViewSet)
router.register('libros', LibroViewSet)
router.register('ejemplares', EjemplarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
