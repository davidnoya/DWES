from django.contrib import admin
from .models import usuarioPersonalizado, Evento, Reserva, Comentario


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo')
    list_filter = ('tipo',)

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'capacidad', 'organizador')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('fecha', 'organizador')

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'num_tickets', 'estado')
    list_filter = ('estado',)

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha')
    search_fields = ('comentario',)

admin.site.register(usuarioPersonalizado, UsuarioAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Comentario, ComentarioAdmin)
