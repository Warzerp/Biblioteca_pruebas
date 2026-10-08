from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet, PrestamoViewSet, HistorialPrestamoViewSet

router = DefaultRouter()
router.register('reservas', ReservaViewSet)
router.register('prestamos', PrestamoViewSet)
router.register('historial-prestamos', HistorialPrestamoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
