from django.conf import settings


def utilisateurs_processeur(request):
	request.session.set_expiry(0)
	return {}
