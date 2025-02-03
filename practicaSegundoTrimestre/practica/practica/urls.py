"""
URL configuration for practica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eventos import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('usuario/register/', views.register),
    path('usuario/login/', views.login_view),

    path('eventos/', views.listar_eventos),
    path('eventos/crear/', views.crear_evento),
    path('eventos/actualizar/<int:evento_id>/', views.actualizar_evento),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento),

    path('reservas/', views.listar_reservas),
    path('reservas/crear/', views.crear_reserva),
    path('reservas/actualizar/<int:reserva_id>/', views.actualizar_reserva),
    path('reservas/cancelar/<int:reserva_id>/', views.cancelar_reserva),

    path('comentarios/<int:evento_id>/', views.listar_comentarios),
    path('comentarios/<int:evento_id>/crear/', views.crear_comentario)

]
