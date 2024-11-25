from django.shortcuts import render
from django.http import HttpResponse
from .models import tJuegos
# Create your views here.

def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>");

def devolver_juegos(request):
	lista = tJuegos.objects.all()
	respuesta = [{'id': j.id, 'nombre': j.nombre, 'tematica': j.tematica, 'fecha_publicacion': j.fecha_publicacion for j in lista]
	return JsonResponse(respuesta, safe=False)
