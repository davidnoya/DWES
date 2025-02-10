from rest_framework import serializers
from .models import usuarioPersonalizado, Evento, Reserva, Comentario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = usuarioPersonalizado
        fields = ['id', 'username', 'tipo']

class EventoSerializer(serializers.ModelSerializer):
    organizador = serializers.StringRelatedField()  #nombre organizador

    class Meta:
        model = Evento
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    evento_id = serializers.PrimaryKeyRelatedField(queryset=Evento.objects.all(), source='evento')

    class Meta:
        model = Reserva
        fields = ['evento_id', 'num_tickets']

class ComentarioSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = Comentario
        fields = '__all__'