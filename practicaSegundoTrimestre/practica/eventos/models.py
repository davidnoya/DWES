from django.db import models
from django.contrib.auth.models import AbstractUser

class usuarioPersonalizado(AbstractUser):
    TIPO_USUARIO = [
        ('organizador', 'Organizador'),
        ('participante', 'Participante'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='participante')