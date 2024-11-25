from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Tjuegos
from .models import Tcomentarios
from django.shortcuts import get_object_or_404
# Create your views here.

def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>");

def devolver_juegos(request):
	lista = Tjuegos.objects.all()
	respuesta = [{'id': j.id, 'nombre': j.nombre, 'tematica': j.tematica, 'fecha_publicacion': j.fecha_publicacion} for j in lista]
	return JsonResponse(respuesta, safe=False)

def devolver_juego_por_id(request, id_solicitado):
	juego = get_object_or_404(Tjuegos, id=id_solicitado)
	respuesta = {
		'id': juego.id,
		'nombre': juego.nombre,
		'tematica': juego.tematica,
		'fecha_publicacion': juego.fecha_publicacion,
		'comentarios': [{'id': j.id, 'comentario': j.comentario} for j in juego.comentarios.all()]
	}
	return JsonResponse(respuesta)
