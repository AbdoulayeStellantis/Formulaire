from django import forms

from communs.models import *


class telecommandeAccueilForm(forms.ModelForm):
	nom=forms.CharField(label="Telecommande", widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	

