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
    evento = serializers.StringRelatedField()  # título evento
    usuario = serializers.StringRelatedField()  # nombre del usuario

    class Meta:
        model = Reserva
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = Comentario
        fields = '__all__'