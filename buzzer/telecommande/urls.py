from django.contrib import admin
from django.urls import path

from communs.views import *
urlpatterns = [
	path('<str:cle_jeu>', BuzzerListe.as_view(), {}, 'telecommande'),
]
