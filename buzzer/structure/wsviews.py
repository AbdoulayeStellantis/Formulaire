from django import http
from .models import *
from django.db.models.functions import Substr, Lower

import json

def Sites(request):
	reponse = []
	sites = Structure.objects.filter(type = 'site')
	for site in sites:
		reponse.append({
			'id': site.id_element,
			'code':site.code,			
			'libelle':site.libelle
		})	
	return http.HttpResponse(json.dumps(reponse),content_type='application/json')

def Batiments(request,site):
	reponse = []
	batiments = Structure.objects.filter(id_element_racine = site)
	for batiment in batiments:
		reponse.append({
			'id': batiment.id_element,
			'code':batiment.code,			
			'libelle':batiment.libelle
		})	
	return http.HttpResponse(json.dumps(reponse),content_type='application/json')

def Lignes(request,batiment):
	reponse = []
	lignes = Structure.objects.filter(id_element_racine = batiment)
	for ligne in lignes:
		reponse.append({
			'id': ligne.id_element,
			'code':ligne.code,			
			'libelle':ligne.libelle
		})	
	return http.HttpResponse(json.dumps(reponse),content_type='application/json')
