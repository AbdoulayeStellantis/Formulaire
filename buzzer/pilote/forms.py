from django import forms

from communs.models import *


class PiloteAccueilForm(forms.ModelForm):
	nom=forms.CharField(label="Nom du nouveau jeu", widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	
	class Meta:
		model = Jeu
		fields = ['nom']

