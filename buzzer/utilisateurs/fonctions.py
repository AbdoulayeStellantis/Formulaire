
from .models import *
from django.utils import timezone
import datetime

def nb_users_par_groupe():
	uneminute = datetime.timedelta(minutes=1)
	daterecherche = timezone.now() - uneminute
	reponse = []
	for groupe in Group.objects.all():
		reponse.append({
			'nom':groupe.name,
			'nb':Profilutilisateur.objects.filter(groups__name=groupe.name,datevisite__gt=daterecherche).count()
		})
	return reponse
