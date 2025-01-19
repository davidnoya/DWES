from django.db import models
from django.contrib.auth.models import AbstractUser

class usuarioPersonalizado(AbstractUser):
    TIPO_USUARIO = [
        ('organizador', 'Organizador'),
        ('participante', 'Participante'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='participante')

class Evento(models.Model):
    organizador = models.ForeignKey(usuarioPersonalizado, on_delete=models.CASCADE, related_name='eventos')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    capacidad = models.PositiveIntegerField()
    url_imagen = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    participante = models.ForeignKey(usuarioPersonalizado, on_delete=models.CASCADE, related_name='reservas')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='reservas')
    num_tickets = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f'Reserva de {self.participante.username} para {self.evento.titulo}'