from django.shortcuts import render
from .forms import *

extend_de_base = 'communs/base.html'

def get_departement(request):
	if request.method == 'POST':
		form = GetDeptForm(request.POST)
		if form.is_valid():
			dept = form.cleaned_data['dept']
			template = '/saisie/rg/'+dept
		return HtpResponseRedirect(template)
	else:
		form = GetDeptForm()
	template = 'formulaires/get_departement.html'
	extend = extend_de_base
	return render(request, template, locals())
	

