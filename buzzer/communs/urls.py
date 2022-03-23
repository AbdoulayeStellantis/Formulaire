from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
	path('buzzers-liste/<str:cle_jeu>', views.BuzzerListe.as_view(), {}, 'buzzer_liste'),
	path('qr/<str:qrtype>/<str:cle_jeu>', views.Qr.as_view(), {}, 'qr'),

	path('liste-buzzers-json/<int:id_jeu>', views.ListeBuzzersJson, {}, 'liste_buzzers_json'),
	path('synchro/<int:id_jeu>/<str:action>', views.synchro, {}, 'synchro_telecommande'),
]
