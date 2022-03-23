from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import ModelFormMixin

import json

from communs.models import *
from pilote.forms import *

extend_de_base = 'communs/base.html'

class PiloteAccueil(CreateView):
	model = Jeu
	template_name = 'communs/formulaire.html'
	form_class = PiloteAccueilForm
	
	def get_success_url(self):
		return '/communs/buzzers-liste/'+str(self.object.cle)

	def get_context_data(self, **kwargs):
		context = super(PiloteAccueil, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		context['titre'] = 'Ouverture d\'un nouveau jeu'
		context['retour'] = '/pilote'
		context['btn_submit'] = 'Commencer'
		return context

