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