from django import forms

from communs.models import *


class BuzzerAccueilForm(forms.ModelForm):
	nom=forms.CharField(label="Nom de votre buzzer", widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	
	class Meta:
		model = Buzzer
		fields = ['nom']

