from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("enviarHorario/", views.enviarHorario, name="enviarHorario")
]