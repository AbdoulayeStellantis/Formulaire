
from django import forms
from communs.models import *


class AjoutUserForm(forms.Form):
	identifiant = forms.CharField(
		label='Identifiant',
		widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

class AjoutUserConfirmForm(forms.Form):
	identifiant = forms.CharField(
		required=False,
		label='Identifiant',
		widget=forms.HiddenInput(attrs={}))

class RetraitUserConfirmForm(forms.Form):
	identifiant = forms.CharField(
		required=False,
		label='Identifiant',
		widget=forms.HiddenInput(attrs={}))

class ElementForm(forms.ModelForm):
	class Meta:
		model = Structure
		fields = ['code','libelle']
		
class AjoutGammeForm(forms.ModelForm):
	intitule = forms.CharField(label = 'intitulé')
	class Meta:
		model = Gamme
		fields = ['intitule','fichier']

class AjoutOrganisationForm(forms.ModelForm):
	class Meta:
		model = Organisation
		fields = ['nbOperateur', 'tdc']