from django import forms
from communs.models import *

class GetDeptForm(forms.Form):
	dept = forms.ModelChoiceField(queryset=Structure.objects.filter(id_element_racine=0))