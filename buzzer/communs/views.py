from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView

import json
import pprint
from communs.models import *

extend_de_base = 'communs/base.html'

class BuzzerListe(TemplateView):
	template_name = 'communs/buzzers_liste.html'
	
	def get_context_data(self, **kwargs):
		context = super(BuzzerListe, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		jeu = Jeu.objects.get(cle=self.kwargs['cle_jeu'])
		context['titre'] = str(jeu)
		context['jeu'] = jeu
		if not 'affichage' in self.request.session:
			self.request.session['affichage'] = jeu.affichage
		return context

class Qr(TemplateView):
	template_name = 'communs/qr.html'

	def get_context_data(self, **kwargs):
		context = super(Qr, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		jeu = Jeu.objects.get(cle=self.kwargs['cle_jeu'])
		if self.kwargs['qrtype'] == 'candidat':
			context['titre'] = 'Qr Code du buzzer à : '+str(jeu)
			context['complement_url'] = '/candidat/'+jeu.cle
		elif self.kwargs['qrtype'] == 'telecommande':
			context['titre'] = 'Qr Code de la télécommande de : '+str(jeu)
			context['complement_url'] = '/telecommande/'+jeu.cle
		
		context['qrtype'] = self.kwargs['qrtype']
		context['jeu'] = jeu
		return context

def ListeBuzzersJson(request, id_jeu):
	jeu = Jeu.objects.get(id=id_jeu)
	les_buzzers = Buzzer.objects.filter(jeu=jeu)
	reponse = []
	for buzzer in les_buzzers:
		reponse.append({
			'id_buzzer':buzzer.id,
			'nom_buzzer':buzzer.nom,
		})

	return HttpResponse(json.dumps(reponse),content_type='application/json')

def synchro(request, id_jeu, action):
	jeu = Jeu.objects.get(id=id_jeu)
	# Pour déterminer si la liste des buzzers affichée doit être ou non effacée
	reset_affichage = False	# Par défaut, il ne faut pas effacer la liste des buzzers
	if not request.session['affichage'] == jeu.affichage:
		pprint.pprint('==========')
		reset_affichage = True
		request.session['affichage'] = jeu.affichage		
		
	
	# Démarrage d'une nouvelle question
	if action == 'startbuzzers':
		jeu.affichage = AFF_JEU_RESULTAT
		jeu.save()
		jeu.buzzer_set.all().update(
			synchro=SYNC_JEU_RESET_BUZZER,
			etat_buzzer = ETAT_BUZZER_PRET,
			date=None
		)
		reponse = {
			'action':action,
			'reset_affichage': True
		}
	
	
	# Pour revoyer la liste des buzzers à afficher
	elif action == 'liste_buzzers':
		
		if jeu.affichage == AFF_JEU_LISTE_BUZZER:
			buzzers = jeu.buzzer_set.all().order_by('nom')
			titre_liste = 'Liste de tous les buzzers'
		elif jeu.affichage == AFF_JEU_RESULTAT:
			buzzers = jeu.buzzer_set.filter(date__isnull=False).order_by('date')
			titre_liste = 'Résultat'
		
		les_buzzers = []
		for buzzer in buzzers:
			les_buzzers.append({
				'id_buzzer': buzzer.id,
				'nom_buzzer': buzzer.nom,
			})
		reponse = {
			'action':action,
			'reset_affichage': reset_affichage,
			'titre_liste':titre_liste,
			'les_buzzers': les_buzzers,
		}
	elif action == 'affichetouslesbuzzers':
		jeu.affichage = AFF_JEU_LISTE_BUZZER
		jeu.save()
		reponse = {
			'action':action,
			'reset_affichage': True
		}
	
	elif action == 'get_synchro':
		reponse = {
			'action':action,
		}
	return HttpResponse(json.dumps(reponse),content_type='application/json')
	
	
