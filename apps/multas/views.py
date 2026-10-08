from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Multa, HistorialMulta
from .serializers import MultaSerializer, HistorialMultaSerializer
from .services import registrar_pago_multa
from apps.usuarios.permissions import EsBibliotecario, EsAdmin

class MultaViewSet(viewsets.ModelViewSet):
    queryset = Multa.objects.all()
    serializer_class = MultaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'pagar']:
            return [EsBibliotecario()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def mis_multas(self, request):
        multas = Multa.objects.filter(usuario=request.user).select_related(
            'usuario', 'prestamo', 'prestamo__ejemplar', 'prestamo__ejemplar__libro'
        )
        serializer = self.get_serializer(multas, many=True)
        return Response({'count': len(serializer.data), 'next': None, 'previous': None, 'results': serializer.data})

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        multa = self.get_object()
        condonada = request.data.get('condonada', False)
        try:
            registrar_pago_multa(multa, request.user, condonada)
            return Response({'status': 'Multa procesada'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class HistorialMultaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistorialMulta.objects.all()
    serializer_class = HistorialMultaSerializer
    permission_classes = [EsBibliotecario | EsAdmin]
