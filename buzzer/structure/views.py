from dataclasses import fields
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView
from django.views.generic.edit import ModelFormMixin
from django.db.models import Max
from django.db.models.functions import Substr, Lower

from communs.models import *
from .forms import *
import pprint

extend_de_base = 'communs/base.html'

class ListeRacine(ListView):
	model = Structure
	template_name = 'structure/racine_list.html'
	
	def get_queryset(self):
		typesite = HierarchieStruct.objects.get(indice=1)
		return  Structure.objects.filter(type=typesite)
		
	def get_context_data(self, **kwargs):
		context = super(ListeRacine, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		typesite = HierarchieStruct.objects.get(indice=1)
		context['titre'] = 'Liste des '+typesite.libelle_pluriel
		context['typeelem'] = typesite
		return context

class AjoutElement(CreateView):
	model = Structure
	template_name = 'structure/element_create_form.html'
	fields = ['code','libelle']
	
	def get_success_url(self):
		if self.kwargs['indicehierarchie'] == 1:
			url = "/structure/liste/racine"
		else:
			url = "/structure/modif/element/"+str(self.kwargs['id_racine'])
		return url
		
	def form_valid(self, form):
		self.object = form.save()
		self.object.type = HierarchieStruct.objects.get(indice=self.kwargs['indicehierarchie'])
		if not Structure.objects.all().aggregate(Max('id_element'))['id_element__max']:
			self.object.id_element =  1
		else:
			self.object.id_element =  1 + Structure.objects.all().aggregate(Max('id_element'))['id_element__max'] 
		if self.kwargs['indicehierarchie'] == 1:
			self.object.id_element_racine = 0
		else:
			element_racine = Structure.objects.get(id =int(self.kwargs['id_racine'])) 
			self.object.id_element_racine = element_racine.id_element

		self.object.save()
		return super(ModelFormMixin, self).form_valid(form)
	
	
	def get_context_data(self, **kwargs):
		context = super(AjoutElement, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		typeelem = HierarchieStruct.objects.get(indice=self.kwargs['indicehierarchie'])
		context['titre'] = 'Ajout d\'un '+typeelem.libelle
		if typeelem.indice == 1:
			retour = "/structure/liste/racine"
		else:
			element_racine = Structure.objects.get(id =int(self.kwargs['id_racine'])) 
			retour = "/structure/modif/element/"+str(element_racine.id)
		context['retour'] = retour
		return context


class ModifElement(UpdateView):
	model = Structure
	template_name = 'structure/element_form.html'
	#fields = ['code','libelle']
	form_class =ElementForm
	
	def get_success_url(self):
		if self.object.type.indice == 1:
			url = "/structure/liste/racine"
		else:
			element_racine = Structure.objects.get(id_element=self.object.id_element_racine)
			url = "/structure/modif/element/"+str(element_racine.id)
		return url
		
	def get_context_data(self, **kwargs):
		context = super(ModifElement, self).get_context_data(**kwargs)
		# On cherche à savoir s'il y a un niveau inférieur dans la hiérarchie
		niveausuivant = self.object.type.get_niveausuivant()
		context['niveausuivant'] = niveausuivant 
		
		# Est-ce que le niveau suivant est le dernier ?
		# Si  oui, les données ne sontpas dans la structure mais dans les données spécifiques de l'appli.
		dernierniveau = niveausuivant.is_dernierniveau()
		context['dernierniveau'] = dernierniveau
		#dernierniveau = niveausuivant.get_niveausuivant().is_dernierniveau()
		#context['dernierniveau'] = dernierniveau
		if dernierniveau:
			context['souselements'] = Organisation.objects.filter(structure = self.object)
		else:
			context['souselements'] = Structure.objects.filter(id_element_racine = self.object.id_element)
		context['extend'] = extend_de_base
		if self.object.type.indice == 1:
			retour = "/structure/liste/racine"
		else:
			element_racine = Structure.objects.get(id_element =int(self.object.id_element_racine)) 
			retour = "/structure/modif/element/"+str(element_racine.id)
		context['retour'] = retour
		context['titre'] = 'Modification d\'un  '+self.object.type.libelle
		return context

class SupprElement(DeleteView):
	model = Structure
	template_name = 'structure/element_confirm_delete.html'
	
	def get_success_url(self):
		if self.object.id_element_racine == 0:
			url = '/structure/liste/racine'
		else:
			element_racine = Structure.objects.get(id_element = self.object.id_element_racine)
			url = "/structure/modif/element/"+str(element_racine.id)
		return url
		
	def get_context_data(self, **kwargs):
		context = super(SupprElement, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		impossible = False
		if Structure.objects.filter(id_element_racine = self.object.id_element).count() > 0:
			impossible = True
		context['titre'] = 'Suppression d\'un élément '+self.object.type.libelle
		context['impossible'] = impossible
		if self.object.id_element_racine == 0:
			retour = "/structure/liste/racine"
		else:
			element_racine = Structure.objects.get(id_element =self.object.id_element_racine) 
			retour = "/structure/modif/element/"+str(element_racine.id)
		context['retour'] = retour
		return context

def AjoutUser(request, type_user, element_structure):
	msg = ''
	if request.method == 'POST':
		form = AjoutUserForm(request.POST)
		if form.is_valid():
			identifiant = form.cleaned_data['identifiant'].lower()
			pprint.pprint("======================= "+identifiant) 
			try:
				user = Profilutilisateur.objects.annotate(minuscule=Lower('username')).get(minuscule=identifiant)
				template = "/structure/user/confirm/ajout/"+type_user+"/"+element_structure+"/"+identifiant
				return HttpResponseRedirect(template)
			except:
				msg = "Cet identifiant n\'existe pas"
	else: 
		form = AjoutUserForm()
	element = Structure.objects.get(id_element = int(element_structure))
	extend = extend_de_base
	titre = "Ajout d\'un "+type_user
	template = "structure/ajoute-type-user.html"
	return render(request, template,locals())

def AjoutUserConfirm(request, type_user,element_structure,identifiant):
	element = Structure.objects.get(id_element = int(element_structure))
	msg = ''
	if request.method == 'POST':
		form = AjoutUserConfirmForm(request.POST)
		if form.is_valid():
			try:
				user = Profilutilisateur.objects.annotate(minuscule=Lower('username')).get(minuscule=identifiant.lower())
				if type_user == 'responsable':
					element.responsables.add(user)
				else:
					element.controleurs.add(user)
				template = '/structure/modif/element/'+str(element.id)
				return HttpResponseRedirect(template)
			except:
				msg = "Cet identifiant n\'existe pas"
	else: 
		form = AjoutUserConfirmForm()
	extend = extend_de_base
	titre = "Ajout d\'un "+type_user
	user = Profilutilisateur.objects.annotate(minuscule=Lower('username')).get(minuscule=identifiant)
					
	template = "structure/ajoute-user-confirm.html"
	return render(request, template,locals())

def RetraitUserConfirm(request,type_user,element_structure,identifiant):
	element = Structure.objects.get(id_element = int(element_structure))
	msg = ''
	if request.method == 'POST':
		form = RetraitUserConfirmForm(request.POST)
		if form.is_valid():
			user = Profilutilisateur.objects.annotate(minuscule=Lower('username')).get(minuscule=identifiant.lower())
			if type_user == 'responsable':
				element.responsables.remove(user)
			else:
				element.controleurs.remove(user)
			template = '/structure/modif/element/'+str(element.id)
			return HttpResponseRedirect(template)
	else:
		form = RetraitUserConfirmForm()
	extend = extend_de_base
	titre = "Retrait d\'un "+type_user
	user = Profilutilisateur.objects.annotate(minuscule=Lower('username')).get(minuscule=identifiant)

	template = "structure/retire-user-confirm.html"
	return render(request, template,locals())

class GammeList(ListView):
	'''model = Gamme'''
	template_name = 'structure/gamme_list.html'

	def get_queryset(self):
		moyen = Moyens.objects.get(id=self.kwargs['id_moyen'])
		return Gamme.objects.filter(moyen=moyen).order_by('intitule')

	def get_context_data(self, **kwargs):
		context = super(GammeList, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		context['titre'] = 'Liste des gammes'
		context['moyen'] = Moyens.objects.get(id=self.kwargs['id_moyen'])
		"""context['typeelem'] = typesite"""
		return context

def AjoutGamme(request, id_moyen):
	moyen = Moyens.objects.get(id = id_moyen)
	msg = ''
	if request.method == 'POST':
		form = AjoutGammeForm(request.POST, request.FILES)
		if form.is_valid():
			intitule = form.cleaned_data['intitule'].lower()
			pprint.pprint("======================= "+intitule) 
			fichier = form.cleaned_data['fichier']
			newGamme = Gamme()
			newGamme.intitule = intitule
			newGamme.fichier = fichier
			newGamme.moyen = moyen
			newGamme.save()
			template = "/structure/gamme/"+str(moyen.id)
			return HttpResponseRedirect(template)
	else: 
		form = AjoutGammeForm()
	#element = Structure.objects.get(id_element = int(id_moyen))
	extend = extend_de_base
	titre = "Ajout d\'un "+ moyen.libelle
	template = "structure/ajoute-gamme.html"
	return render(request,template,locals())

class SupprGamme(DeleteView):
	model = Gamme
	template_name = 'structure/gamme_confirm_delete.html'

	def get_success_url(self):
		url = '/structure/gamme/'+str(self.object.moyen.id)
		return url

	def get_context_data(self, **kwargs):
		context = super(SupprGamme, self).get_context_data(**kwargs)
		context['extend'] = extend_de_base
		context['titre'] = 'Suppression d\'une gamme'
		context['retour'] = '/structure/gamme/'+str(self.object.moyen.id)
		return context

class AjoutOrganisation(CreateView):
	model = Organisation
	template_name = 'structure/ajout-organisation.html'
	form_class = AjoutOrganisationForm

	def get_context_data(self, **kwargs):
		context = super(AjoutOrganisation, self).get_context_data(**kwargs)
		context['souselements'] = Organisation.objects.filter(structure = self.object)
		context['extend'] = extend_de_base
		context['titre'] = 'Ajouter une organisation'
		return context

	def form_valid(self, form):
		self.object = form.save() 
		self.object.id = self.kwargs['id_struct']
		self.object.save()
		return super(ModelFormMixin, self).form_valid(form)
	
	def get_success_url(self):
		url = "/structure/modif/element/"+str(self.kwargs['id_struct'])
		return url
