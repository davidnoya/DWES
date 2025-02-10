from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json
from .models import usuarioPersonalizado, Evento, Reserva, Comentario

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UsuarioSerializer, EventoSerializer, ReservaSerializer, ComentarioSerializer
from rest_framework.permissions import BasePermission

# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usuario = usuarioPersonalizado.objects.create_user(
            username=data['username'],
            password=data['password'],
            tipo=data.get('tipo', 'participante'),
        )
        return JsonResponse({'mensaje': 'Registro completado', 'id': usuario.id})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usuario = authenticate(username=data['username'], password=data['password'])
        if usuario:
            login(request, usuario)
            return JsonResponse({'mensaje': 'Login completado'})
        return JsonResponse({'error': 'Datos incorrectos'}, status=401)


def listar_eventos(request):
    eventos = Evento.objects.select_related('organizador').all()
    titulo = request.GET.get('titulo')
    fecha= request.GET.get('fecha')

    if titulo:
        eventos = eventos.filter(titulo__icontains=titulo)
    if fecha:
        eventos = eventos.filter(fecha_hora__date=fecha)

    paginator = Paginator(eventos, 5)
    page = request.GET.get('page', 1)
    eventos_paginados= paginator.get_page(page)

    data = [
        {
            'id': ev.id,
            'titulo': ev.titulo,
            'descripcion': ev.descripcion,
            'fecha': ev.fecha.isoformat(),
            'capacidad': ev.capacidad,
            'organizador': ev.organizador.username
        }
        for ev in eventos_paginados
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_evento(request):
    if request.method == 'POST':
        usuario = request.user
        if not usuario.is_authenticated or usuario.tipo != 'organizador':
            return JsonResponse({'error': 'No autorizado'}, status=401)
        data = json.loads(request.body)
        evento = Evento.objects.create(
            titulo=data['titulo'],
            descripcion=data['descripcion'],
            fecha=data['fecha'],
            capacidad=data['capacidad'],
            url_imagen=data.get('url_imagen', ''),
            organizador=usuario
        )
        return JsonResponse({'mensaje': 'Evento creado', 'id': evento.id})

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


@csrf_exempt
def crear_reserva(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        data = json.loads(request.body)
        evento = Evento.objects.get(id=data['evento_id'])
        reserva = Reserva.objects.create(
            usuario=request.user,
            evento=evento,
            num_tickets=data['num_tickets']
        )
        return JsonResponse({'mensaje': 'Reserva creada', 'id': reserva.id})


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


@csrf_exempt
def cancelar_reserva(request, reserva_id):
    if request.method == 'DELETE':
        usuario = request.user
        reserva = get_object_or_404(Reserva, id=reserva_id)

        if reserva.usuario != usuario:
            return JsonResponse({'error': 'Usuario no autorizado'}, status=403)

        reserva.delete()
        return JsonResponse({'mensaje': 'Reserva cancelada'}, status=204)


# ------------------- COMENTARIOS -------------------
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

#TOKENS

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = usuarioPersonalizado.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})

#APIVIEW

class ListarEventosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        eventos = Evento.objects.all()
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)

class EsOrganizador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'organizador'

class CrearEventoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EsOrganizador]

    def post(self, request):
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizador=request.user)
            return Response({'mensaje': 'Evento creado', 'evento': serializer.data})
        return Response(serializer.errors, status=400)