
from django import forms
from django.forms.widgets import RadioSelect ,CheckboxSelectMultiple
from django.forms.widgets import Widget, Select, MultiWidget
from django.forms import ModelChoiceField

from communs.models import *

equipes = (
	('Jour','Jour'),
	('Bleue','Bleue'),
	('Verte','Verte'),
	('Nuit','Nuit'),
	('Vsd','Vsd'),
)
class RechercheForm(forms.Form):
	critere = forms.CharField(
		label='Identifiant/Nom/Prénom',
		max_length=30,
		help_text = '',
		required = False,
		widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

class ProfilutilisateurForm(forms.ModelForm):
	username = forms.CharField(label='Identifiant',max_length=30,widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	first_name = forms.CharField(label='Prénom',max_length=30)
	last_name = forms.CharField(label='Nom',max_length=30)
	site = forms.ModelChoiceField(label='Site', queryset=Structure.objects.filter(id_element_racine=0).order_by('libelle'), required=False)
	email = forms.EmailField(label='Adresse Email')
	telinterne = forms.CharField(label=u'N° tel. interne',required=False)
	telexterne = forms.CharField(label=u'N° tel mobile',required=False)
	is_staff = forms.BooleanField(label='Administrateur',required=False,help_text='')
	equipe = forms.ChoiceField(choices=equipes)

	class Meta:
		model = Profilutilisateur
		fields = ['username','first_name','last_name','site','email','telinterne','telexterne','is_staff','equipe']

class UserSupprGroupeConfirmForm(forms.ModelForm):
	username = forms.CharField(required=False,widget=forms.HiddenInput(attrs={}))
	class Meta:
		model = Profilutilisateur
		fields = ['username']	