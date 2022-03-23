from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
	path('<str:cle_jeu>', views.BuzzerAccueil, {}, 'buzzer_accueil'),
	path('page-buzzer/<int:id_buzzer>', views.PageBuzzer.as_view(), {}, 'page_buzzer'),
	path('synchro/<int:id_buzzer>/<str:action>', views.synchro, {}, 'synchro_buzzer'),
]
