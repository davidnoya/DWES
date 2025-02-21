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
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpoints de autenticación y API
    path('usuario/register/', views.register),
    path('usuario/login/', views.login_view),
    path('usuario/token/', obtain_auth_token),

    path('eventos/actualizar/<int:evento_id>/', views.actualizar_evento),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento),

    path('reservas/', views.listar_reservas),
    path('reservas/actualizar/<int:reserva_id>/', views.actualizar_reserva),

    path('comentarios/<int:evento_id>/', views.listar_comentarios),
    path('comentarios/<int:evento_id>/crear/', views.crear_comentario),

    path('eventosAPI/', views.ListarEventosAPIView.as_view()),
    path('eventosAPI/crear/', views.CrearEventoAPIView.as_view()),
    path('reservasAPI/crear/', views.CrearReservaAPIView.as_view()),
    path('reservasAPI/cancelar/<int:reserva_id>/', views.EliminarReservaAPIView.as_view()),

    # Rutas para las plantillas dinámicas (Etapa 4)
    path('', views.home, name='home'),
    path('evento/<int:event_id>/', views.event_detail, name='event_detail'),
    path('panel/', views.user_panel, name='user_panel'),
    path('evento/<int:event_id>/reservar/', views.crear_reserva_view, name='crear_reserva_view'),
    path('evento/<int:event_id>/comentario/', views.crear_comentario_view, name='crear_comentario_view'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
