from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect

import json

from communs.models import *

extend_de_base = 'communs/base.html'

class TelecommandeAccueil(TemplateView):
	template_name = 'telecommande/telecommande.html'
	
	def get_context_data(self, **kwargs):
		context = super(TelecommandeAccueil, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		jeu = Jeu.objects.get(cle=self.kwargs['cle_jeu'])
		context['jeu'] = jeu
		context['titre'] = 'telecommande de ' + jeu.nom
		return context
		
