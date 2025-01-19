from django.contrib import admin
from .models import usuarioPersonalizado, Evento, Reserva, Comentario

@admin.register(usuarioPersonalizado)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo')
    list_filter = ('tipo',)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'capacidad', 'organizador')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('fecha', 'organizador')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'num_tickets', 'estado')
    list_filter = ('estado',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha')
    search_fields = ('comentario',)