from rest_framework import serializers
from .models import Reserva, Prestamo, HistorialPrestamo


class ReservaSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id', 'usuario', 'usuario_username', 'libro', 'libro_titulo',
            'fecha_reserva', 'fecha_expiracion', 'estado',
        ]
        read_only_fields = ['usuario', 'fecha_reserva', 'fecha_expiracion', 'estado']


class PrestamoSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    ejemplar_codigo = serializers.CharField(source='ejemplar.codigo_inventario', read_only=True)
    libro_titulo = serializers.CharField(source='ejemplar.libro.titulo', read_only=True)

    class Meta:
        model = Prestamo
        fields = [
            'id', 'usuario', 'usuario_username', 'ejemplar', 'ejemplar_codigo',
            'libro_titulo', 'fecha_prestamo', 'fecha_limite_devolucion',
            'fecha_devolucion_real', 'estado', 'observaciones',
        ]
        read_only_fields = [
            'fecha_prestamo', 'fecha_devolucion_real', 'estado', 'fecha_limite_devolucion',
        ]


class HistorialPrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPrestamo
        fields = '__all__'
        read_only_fields = ['timestamp']
