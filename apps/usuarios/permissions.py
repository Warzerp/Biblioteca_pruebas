from rest_framework.permissions import BasePermission

class EsBibliotecario(BasePermission):
    """Permite acceso solo a usuarios con rol BIBLIOTECARIO o ADMIN."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
                    request.user.rol in ['BIBLIOTECARIO', 'ADMIN'])

class EsAdmin(BasePermission):
    """Permite acceso solo a usuarios con rol ADMIN."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
                    request.user.rol == 'ADMIN')

class EsPropietarioOAdmin(BasePermission):
    """Permite acceso al propietario del recurso o a un Admin."""
    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user or request.user.rol in ['BIBLIOTECARIO', 'ADMIN']
