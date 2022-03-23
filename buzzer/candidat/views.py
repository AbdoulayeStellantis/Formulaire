from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

import json

from communs.models import *
from candidat.forms import *

extend_de_base = 'communs/base.html'

def BuzzerAccueil(request, cle_jeu):
	jeu = Jeu.objects.get(cle=cle_jeu)
	if request.method == 'POST':
		form = BuzzerAccueilForm(request.POST)
		if form.is_valid():
			new_buzzer = Buzzer()
			new_buzzer.nom = form.cleaned_data['nom']
			new_buzzer.jeu = jeu
			new_buzzer.save()
			
			template = '/candidat/page-buzzer/'+str(new_buzzer.id)
			return HttpResponseRedirect(template)

	else:
		form = BuzzerAccueilForm()
	template = 'communs/formulaire.html'
	extend = extend_de_base
	titre = 'Inscription à une nouvelle partie'
	retour = '/candidat/'+cle_jeu
	btn_submit = 'Entrer'
	return render(request, template, locals())


class PageBuzzer(TemplateView):
	template_name = 'candidat/page_buzzer.html'

	def get_context_data(self, **kwargs):
		context = super(PageBuzzer, self).get_context_data(**kwargs)
		buzzer = Buzzer.objects.get(id=self.kwargs['id_buzzer'])
		context['buzzer'] = buzzer
		context['extend'] = extend_de_base
		context['titre'] = buzzer.jeu.nom + ' / ' + buzzer.nom
		return context

def synchro(request, id_buzzer, action):
	buzzer = Buzzer.objects.get(id=id_buzzer)
	if action == 'get_synchro':
		action_a_faire = ''
		if buzzer.synchro == SYNC_JEU_RESET_BUZZER:
			action_a_faire = 'reset_buzzer'
		reponse = {
			'action':action,
			'synchro':action_a_faire,
		}
	elif action == 'set_buzzer_enfonce':
		buzzer.etat_buzzer = ETAT_BUZZER_ENFONCE
		buzzer.date = timezone.datetime.now()
		buzzer.save()
		reponse = {
			'action':action,
		}
	elif action == 'set_buzzer_pret':
		buzzer.synchro = SYNC_BUZZER_PRET
		buzzer.etat_buzzer = ETAT_BUZZER_PRET
		buzzer.date = None
		buzzer.save()
		reponse = {
			'action':action,
		}
	return HttpResponse(json.dumps(reponse),content_type='application/json')
	
	

		