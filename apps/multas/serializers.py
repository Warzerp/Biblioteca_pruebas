from rest_framework import serializers
from .models import Multa, HistorialMulta


class MultaSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    libro_titulo = serializers.CharField(source='prestamo.ejemplar.libro.titulo', read_only=True)

    class Meta:
        model = Multa
        fields = [
            'id', 'usuario', 'usuario_username', 'prestamo', 'libro_titulo',
            'monto', 'motivo', 'estado', 'fecha_generacion', 'fecha_pago',
        ]
        read_only_fields = ['fecha_generacion', 'fecha_pago', 'estado']

class HistorialMultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialMulta
        fields = '__all__'
        read_only_fields = ['timestamp']
