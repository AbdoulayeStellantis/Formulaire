from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.db.models.functions import Substr, Lower
from django.utils import timezone
from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import datetime

from .models import *
from .forms import *

extend_de_base = 'communs/base.html'
prefix_pass = 'midas'

def Liste(request):
	extend = extend_de_base
	titre = u'Liste des utilisateurs'
	if request.method == 'POST':
		form = RechercheForm(request.POST)
		if form.is_valid():
			critere = str(form.cleaned_data['critere']).lower()
			touslesutilisateurs = Profilutilisateur.objects.filter(
				Q(username__icontains=critere) |
				Q(last_name__icontains=critere) | 
				Q(first_name__icontains=critere) 
			).order_by('first_name','last_name')
	else:
		form = RechercheForm()
		touslesutilisateurs = Profilutilisateur.objects.all().order_by('first_name','last_name')
	pagination = Paginator(touslesutilisateurs ,15)
	page = request.GET.get('page',1)
	try:
		lesutilisateurs = pagination.page(page)
	except PageNotAnInteger:
		lesutilisateurs = pagination.page(1)
	except EmptyPage:
		lesutilisateurs = pagination.page(pagination.num_pages)
	situation = 'Page N° '+str(page)+' / '+str(pagination.num_pages)
	template_name = 'utilisateurs/profilutilisateur_list.html'
	return render(request, template_name, locals())

class oldListe(TemplateView):
	template_name = 'utilisateurs/profilutilisateur_list.html'
	#model = Profilutilisateur
	#queryset =  Profilutilisateur.objects.all().order_by('first_name','last_name')

	def get_context_data(self, **kwargs):
		context = super(Liste, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		liste_utilisateurs =  Profilutilisateur.objects.all().order_by('first_name','last_name')
		pagination = Paginator(liste_utilisateurs,10)
		page = self.request.GET.get('page',1)
		try:
			lesutilisateurs = pagination.page(page)
		except PageNotAnInteger:
			lesutilisateurs = pagination.page(1)
		except EmptyPage:
			lesutilisateurs = pagination.page(pagination.num_pages)
		context['situation'] = 'Page N° '+str(page)+' / '+str(pagination.num_pages)
		context['lesutilisateurs'] = lesutilisateurs

		return context

class Ajout(CreateView):
	template_name = 'utilisateurs/profilutilisateur_list.html'
	model = Profilutilisateur
	form_class = ProfilutilisateurForm
	success_url = '/utilisateurs/liste'
	
	def form_valid(self, form):
		self.object = form.save()
		object = self.object
		object.set_password(prefix_pass+self.object.username.lower())
		object.save()
		#login(self.request, object)
		#self.request.session.set_expiry(0)
		return super(ModelFormMixin, self).form_valid(form)
	
	def get_context_data(self, **kwargs):
		context = super(Ajout, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		context['titre'] = 'Création d\'un utilisateur'
		return context

class Modif(UpdateView):
	template_name = 'utilisateurs/profilutilisateur_form.html'
	model = Profilutilisateur
	form_class = ProfilutilisateurForm
	success_url = '/utilisateurs/liste'
	
	def get_context_data(self, **kwargs):
		context = super(Modif, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		context['titre'] = 'Modification d\'un utilisateur'
		return context

class Suppr(DeleteView):
	template_name = 'utilisateurs/profilutilisateur_confirm_delete.html'
	model = Profilutilisateur
	success_url = '/utilisateurs/liste'
	
	def get_context_data(self, **kwargs):
		context = super(Suppr, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		context['titre'] = 'Suppression d\'un utilisateur'
		return context

class GroupeListe(ListView):
	template_name = "utilisateurs/groupe_list.html"
	def get_queryset(self):
		queryset = User.objects.filter(groups__name = self.kwargs['groupe']).order_by('first_name','last_name')
		return queryset

	def get_context_data(self, **kwargs):
		context = super(GroupeListe, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		context['titre'] = 'Liste des '+self.kwargs['groupe']
		context['groupe'] = self.kwargs['groupe']
		return context

class UserSupprGroupe(UpdateView):
	model = Profilutilisateur
	template_name = 'utilisateurs/user_group_confirm_delete.html'
	form_class = UserSupprGroupeConfirmForm

	def get_success_url(self):
		return '/utilisateurs/groupe/liste/'+self.kwargs['groupe']
	
	def form_valid(self, form):
		grp = Group.objects.get(name=self.kwargs['groupe'])
		self.object.groups.remove(grp)
		self.object.save()
		return super(ModelFormMixin, self).form_valid(form)
		
	def get_context_data(self, **kwargs):
		context = super(UserSupprGroupe, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		context['groupe'] = self.kwargs['groupe']
		context['titre'] = 'Retrait d\'un utilisateur d\'un groupe'
		return context

def ResetMdp(request,username):
	user = Profilutilisateur.objects.annotate(minuscule=Lower('username')).get(minuscule=username.lower())
	user.set_password(prefix_pass+username.lower())
	user.save()
	mdp = 'midas'+username.lower()
	extend = extend_de_base
	template = "utilisateurs/reset_mdp_done.html"
	return render(request,template,locals())

class UtilisateursConnectes(TemplateView):
	template_name = 'utilisateurs/utilisateurs_connectes.html'
	
	def get_context_data(self, **kwargs):
		context = super(UtilisateursConnectes, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base 
		context['titre'] = 'Liste des personnes connectées'
		uneminute = datetime.timedelta(minutes=1)
		daterecherche = timezone.now() - uneminute
		lesgroupes = []
		for groupe in Group.objects.all().order_by('name'):
			lesutilisateurs = Profilutilisateur.objects.filter(groups__name=groupe.name,datevisite__gt=daterecherche).order_by('first_name','last_name')
			lesgroupes.append({
				'nom':groupe.name,
				'nb':lesutilisateurs.count(),
				'lesutilisateurs': lesutilisateurs,
			})
		context['lesgroupes'] = lesgroupes
		return context
		
		
		
		