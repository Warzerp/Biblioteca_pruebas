from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MultaViewSet, HistorialMultaViewSet

router = DefaultRouter()
router.register('multas', MultaViewSet)
router.register('historial-multas', HistorialMultaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
