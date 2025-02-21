from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from drf_yasg.openapi import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import usuarioPersonalizado, Evento, Reserva, Comentario
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import json


# Registro de usuario
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        tipo = data.get('tipo', 'participante')

        if usuarioPersonalizado.objects.filter(username=username).exists():
            return JsonResponse({'error': 'El usuario ya existe'}, status=400)

        user = usuarioPersonalizado.objects.create(
            username=username,
            password=make_password(password),
            tipo=tipo
        )
        return JsonResponse({'mensaje': 'Usuario registrado correctamente', 'id': user.id})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# Login de usuario
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        else:
            return JsonResponse({'error': 'Credenciales incorrectas'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# API Views para eventos y reservas
class ListarEventosAPIView(APIView):
    def get(self, request):
        eventos = Evento.objects.all()
        eventos_data = [
            {
                'id': evento.id,
                'titulo': evento.titulo,
                'descripcion': evento.descripcion,
                'fecha': evento.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'capacidad': evento.capacidad,
                'organizador': evento.organizador.username
            } for evento in eventos
        ]
        return JsonResponse(eventos_data, safe=False)


class CrearEventoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.tipo != 'organizador':
            return JsonResponse({'error': 'No tienes permisos para crear eventos'}, status=403)

        data = json.loads(request.body)
        evento = Evento.objects.create(
            organizador=request.user,
            titulo=data.get('titulo'),
            descripcion=data.get('descripcion'),
            fecha=data.get('fecha'),
            capacidad=data.get('capacidad'),
            url_imagen=data.get('url_imagen')
        )
        return JsonResponse({'mensaje': 'Evento creado correctamente', 'id': evento.id})


@csrf_exempt
def actualizar_evento(request, evento_id):
    if request.method in ['PUT', 'PATCH']:
        usuario = request.user
        evento = get_object_or_404(Evento, id=evento_id)
        if evento.organizador != usuario:
            return JsonResponse({'error': 'Usuario no autorizado'}, status=401)

        data = json.loads(request.body)
        evento.titulo = data.get('titulo', evento.titulo)
        evento.descripcion = data.get('descripcion', evento.descripcion)
        evento.fecha = data.get('fecha', evento.fecha)
        evento.capacidad = data.get('fecha', evento.capacidad)
        evento.url_imagen = data.get('fecha', evento.url_imagen)
        evento.save()

        return JsonResponse({'mensaje': 'Evento actualizado!'})


@csrf_exempt
def eliminar_evento(request, evento_id):
    if request.method == 'DELETE':
        usuario = request.user
        evento = get_object_or_404(Evento, id=evento_id)
        if evento.organizador != usuario:
            return JsonResponse({'error': 'Usuario no autorizado'}, status=403)
        evento.delete()
        return JsonResponse({'mensaje': 'Evento eliminado'}, status=204)


def listar_reservas(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    reservas = Reserva.objects.filter(usuario=request.user).select_related('evento').values(
        'id', 'evento__titulo', 'estado', 'num_tickets'
    )

    return JsonResponse(list(reservas), safe=False)


class CrearReservaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        evento_id = data.get('evento_id')
        num_tickets = data.get('num_tickets')

        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado'}, status=404)

        reserva = Reserva.objects.create(
            usuario=request.user,
            evento=evento,
            num_tickets=num_tickets
        )
        return JsonResponse({'mensaje': 'Reserva creada correctamente', 'id': reserva.id})


@csrf_exempt
def actualizar_reserva(request, reserva_id):
    if request.method in ['PUT', 'PATCH']:
        usuario = request.user
        reserva = get_object_or_404(Reserva, id=reserva_id)

        if usuario.tipo != 'organizador' and reserva.usuario != usuario:
            return JsonResponse({'error': 'Usuario no autorizado'}, status=403)

        data = json.loads(request.body)
        if usuario.tipo == 'organizador':
            reserva.estado = data.get('estado', reserva.estado)
        reserva.num_tickets = data.get('num_tickets', reserva.num_tickets)
        reserva.save()

        return JsonResponse({'mensaje': 'Reserva actualizada'})


class EliminarReservaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, reserva_id):
        try:
            reserva = Reserva.objects.get(id=reserva_id, usuario=request.user)
        except Reserva.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada o no tienes permiso'}, status=404)

        reserva.delete()
        return JsonResponse({'mensaje': 'Reserva cancelada correctamente'})


# Comentarios
def listar_comentarios(request, evento_id):
    comentarios = Comentario.objects.filter(evento_id=evento_id).select_related('usuario').values(
        'id', 'usuario__username', 'comentario', 'fecha'
    )
    return JsonResponse(list(comentarios), safe=False)


@csrf_exempt
def crear_comentario(request, evento_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        data = json.loads(request.body)
        comentario = Comentario.objects.create(
            usuario=request.user,
            evento_id=evento_id,
            comentario=data['comentario ']
        )
        return JsonResponse({'mensaje': 'Comentario añadido', 'id': comentario.id})


# TOKENS
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = usuarioPersonalizado.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})


# ------------------------------------------------------
# Vistas para plantillas (Etapa 4: Plantillas y Vistas Dinámicas)
# ------------------------------------------------------
from django.contrib.auth.decorators import login_required


def home(request):
    eventos = Evento.objects.all()
    return render(request, 'index.html', {'eventos': eventos})


def event_detail(request, event_id):
    evento = get_object_or_404(Evento, id=event_id)
    comentarios = Comentario.objects.filter(evento=evento).select_related('usuario')
    return render(request, 'event_detail.html', {'evento': evento, 'comentarios': comentarios})


@login_required
def user_panel(request):
    reservas = Reserva.objects.filter(usuario=request.user).select_related('evento')
    return render(request, 'user_panel.html', {'reservas': reservas})


@login_required
def crear_reserva_view(request, event_id):
    evento = get_object_or_404(Evento, id=event_id)
    if request.method == 'POST':
        num_tickets = request.POST.get('num_tickets')
        if num_tickets:
            Reserva.objects.create(
                usuario=request.user,
                evento=evento,
                num_tickets=int(num_tickets)
            )
        return redirect('user_panel')
    return redirect('event_detail', event_id=event_id)


@login_required
def crear_comentario_view(request, event_id):
    evento = get_object_or_404(Evento, id=event_id)
    if request.method == 'POST':
        comentario_text = request.POST.get('comentario')
        if comentario_text:
            Comentario.objects.create(
                usuario=request.user,
                evento=evento,
                comentario=comentario_text
            )
        return redirect('event_detail', event_id=event_id)
    return redirect('event_detail', event_id=event_id)
