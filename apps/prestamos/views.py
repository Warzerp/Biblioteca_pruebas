from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Reserva, Prestamo, HistorialPrestamo
from .serializers import ReservaSerializer, PrestamoSerializer, HistorialPrestamoSerializer
from .services import (
    calcular_fecha_limite, calcular_fecha_expiracion_reserva,
    usuario_bloqueado, calcular_mora,
)
from apps.usuarios.permissions import EsBibliotecario, EsAdmin
from apps.multas.models import Multa, HistorialMulta


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related('usuario', 'libro').all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if usuario_bloqueado(self.request.user):
            raise ValidationError({'detail': 'No puedes reservar: tienes multas pendientes.'})
        serializer.save(
            usuario=self.request.user,
            fecha_expiracion=calcular_fecha_expiracion_reserva(),
        )

    @action(detail=False, methods=['get'])
    def mis_reservas(self, request):
        reservas = Reserva.objects.filter(usuario=request.user).select_related('libro', 'usuario')
        serializer = self.get_serializer(reservas, many=True)
        return Response({'count': len(serializer.data), 'next': None, 'previous': None, 'results': serializer.data})

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.usuario != request.user and request.user.rol not in ['BIBLIOTECARIO', 'ADMIN']:
            return Response(status=status.HTTP_403_FORBIDDEN)
        reserva.estado = 'CANCELADA'
        reserva.save()
        return Response({'status': 'Reserva cancelada'})


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.select_related('usuario', 'ejemplar', 'ejemplar__libro').all()
    serializer_class = PrestamoSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'devolucion']:
            return [EsBibliotecario()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        usuario = serializer.validated_data['usuario']
        if usuario_bloqueado(usuario):
            raise ValidationError({'detail': 'El usuario tiene multas pendientes.'})

        ejemplar = serializer.validated_data['ejemplar']
        if ejemplar.estado != 'DISPONIBLE':
            raise ValidationError({'detail': 'El ejemplar no está disponible.'})

        ejemplar.estado = 'PRESTADO'
        ejemplar.save()

        prestamo = serializer.save(fecha_limite_devolucion=calcular_fecha_limite())
        HistorialPrestamo.objects.create(usuario=usuario, prestamo=prestamo, accion='CREACION')

    @action(detail=False, methods=['get'])
    def mis_prestamos(self, request):
        prestamos = Prestamo.objects.filter(usuario=request.user).select_related(
            'usuario', 'ejemplar', 'ejemplar__libro'
        )
        serializer = self.get_serializer(prestamos, many=True)
        return Response({'count': len(serializer.data), 'next': None, 'previous': None, 'results': serializer.data})

    @action(detail=True, methods=['post'])
    def devolucion(self, request, pk=None):
        prestamo = self.get_object()
        if prestamo.estado == 'DEVUELTO':
            return Response({'error': 'Ya devuelto'}, status=400)

        ahora = timezone.now()
        mora = calcular_mora(prestamo.fecha_limite_devolucion, ahora)
        prestamo.estado = 'CON_MORA' if mora > 0 else 'DEVUELTO'
        prestamo.fecha_devolucion_real = ahora
        prestamo.observaciones = request.data.get('observaciones', prestamo.observaciones)
        prestamo.save()

        ejemplar = prestamo.ejemplar
        ejemplar.estado = 'DISPONIBLE'
        ejemplar.save()

        HistorialPrestamo.objects.create(
            usuario=request.user, prestamo=prestamo, accion='DEVOLUCION'
        )

        if mora > 0:
            multa = Multa.objects.create(
                usuario=prestamo.usuario,
                prestamo=prestamo,
                monto=mora,
                motivo=f'Devolución tardía ({mora} de mora)',
                estado='PENDIENTE',
            )
            HistorialMulta.objects.create(
                usuario=prestamo.usuario, multa=multa, accion='GENERADA',
                detalle='Generada automáticamente en la devolución',
            )

        return Response({'status': 'Devuelto exitosamente', 'mora': str(mora)})

    @action(detail=True, methods=['post'])
    def renovar(self, request, pk=None):
        prestamo = self.get_object()
        es_staff = request.user.rol in ['BIBLIOTECARIO', 'ADMIN']
        if prestamo.usuario != request.user and not es_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if prestamo.estado not in ['ACTIVO', 'CON_MORA']:
            return Response({'error': 'Solo se pueden renovar préstamos activos.'}, status=400)
        prestamo.fecha_limite_devolucion = calcular_fecha_limite()
        prestamo.estado = 'ACTIVO'
        prestamo.save()
        HistorialPrestamo.objects.create(
            usuario=request.user, prestamo=prestamo, accion='EXTENSION'
        )
        return Response({'status': 'Renovado exitosamente'})

class HistorialPrestamoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistorialPrestamo.objects.all()
    serializer_class = HistorialPrestamoSerializer
    permission_classes = [EsBibliotecario | EsAdmin]
