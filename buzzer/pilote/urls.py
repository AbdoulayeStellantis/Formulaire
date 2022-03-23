from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
	path('', views.PiloteAccueil.as_view(), {}, 'pilote_accueil'),
]
