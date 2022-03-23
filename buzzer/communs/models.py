from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models import Q

import pprint
import uuid
import pprint

SYNC_JEU_PRET = 100
SYNC_JEU_RESET_BUZZER = 200
SYNC_JEU_RESET_BUZZER = 300
SYNC_JEU_RESET_EN_COURS = 400

AFF_JEU_LISTE_BUZZER = 100
AFF_JEU_RESULTAT = 200

class Jeu(models.Model):
	nom = models.TextField()
	cle = models.TextField(null=True)
	synchro = models.IntegerField(default=SYNC_JEU_PRET)
	affichage = models.IntegerField(default=AFF_JEU_LISTE_BUZZER)
	date_creation = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if self.cle == None:
			self.cle = str(uuid.uuid1())
		super().save(*args, **kwargs)  

	def __str__(self):
		return self.nom

SYNC_BUZZER_PRET = 100
SYNC_BUZZER_reset_BUZZER = 200

ETAT_BUZZER_PRET = 100
ETAT_BUZZER_ENFONCE = 200
		
class Buzzer(models.Model):
	jeu = models.ForeignKey(Jeu, on_delete=models.CASCADE, null=True)
	nom = models.TextField()
	date = models.DateTimeField(null=True)
	synchro = models.IntegerField(default=SYNC_BUZZER_PRET)
	etat_buzzer = models.IntegerField(default=ETAT_BUZZER_PRET)
	
	def __str__(self):
		return self.nom




def liste_secteurs_enfants(secteur, liste):
	les_enfants = secteur.enfants()
	for enfant in les_enfants:
		if enfant.type.indice == INDICE_SECTEUR:
			liste.append(enfant)
		else:
			liste_secteurs_enfants(enfant, liste)
	return liste


class HierarchieStruct(models.Model):
	indice =models.IntegerField()
	libelle = models.TextField(max_length=30)
	libelle_pluriel = models.TextField(max_length=35)
	
	def get_niveausuivant(self):
		# On cherche à savoir s'il y a un niveau inférieur dans la hiérarchie
		try:
			niveausuivant = HierarchieStruct.objects.get(indice=1+self.indice)
		except:
			niveausuivant = False
		return niveausuivant
			
	def is_dernierniveau(self):
		try:
			niveausuivant = HierarchieStruct.objects.get(indice=1+self.indice)
			dernierniveau = False
		except:
			dernierniveau = True
		return dernierniveau
	
	
	def __str__(self):
		return self.libelle
				
class Profilutilisateur(User):
	site = models.ForeignKey('Structure', on_delete=models.SET_NULL, null=True)
	equipe = models.TextField(max_length=15,null=True) # Ajout de la notion d'équipe
	telinterne = models.TextField(max_length=6,null=True)
	telexterne = models.TextField(max_length=10,null=True)
	nbvisites = models.IntegerField(default=0)
	datevisite = models.DateTimeField(auto_now=True)

	def secteurs(self):
		resultat = []
		struct = Structure.objects.filter(Q(responsables=self) | Q(controleurs=self))
		for elem in struct:
			if elem.type.indice < INDICE_SECTEUR:	# Si niveau site, projet ou type de ctrl
				les_secteurs_enfants = []
				liste_secteurs_enfants(elem, les_secteurs_enfants)
				for secteur_enfant in les_secteurs_enfants:
					resultat.append(secteur_enfant)
			elif elem.type.indice > INDICE_SECTEUR:	# si niveau moyen
				parent = elem.parent()
				while not parent.type.indice == INDICE_SECTEUR:
					parent = parent.parent()
				if not parent in resultat:
					resultat.append(parent)
			else:
				if not elem in resultat:
					resultat.append(elem)
		return sorted(resultat, key=lambda x:x.libelle)	

	def inc_nbvisites(self):
		self.nbvisites += 1
		self.save()
		return
        
	def get_secteurs_enfants(self):
		les_secteurs = []
		for secteur in self.responsable.all():
			#pprint.pprint(str(secteur))
			les_secteurs = les_secteurs + secteur.get_secteurs()
		#pprint.pprint(str(les_secteurs))
		return les_secteurs
	
	def __str__(self):
		return self.last_name+" "+self.first_name 

class Structure(models.Model):
	id_element = models.IntegerField(null=True)
	id_element_racine = models.IntegerField(null=True)
	type = models.ForeignKey(HierarchieStruct,null=True,on_delete=models.CASCADE)
	code = models.TextField("Code ",max_length=5)
	libelle = models.TextField("Libellé ",max_length=50)
	responsables = models.ManyToManyField(Profilutilisateur,verbose_name='Responsable',related_name='responsable')
	controleurs = models.ManyToManyField(Profilutilisateur,verbose_name='Controleur',related_name='controleur')

	def liste_elems_enfants(self, niveau):
		resultat = []
		if self.type.indice < niveau:	
			les_enfants = self.enfants()
			for enfant  in les_enfants:
				if enfant.type.indice == niveau:
					resultat.append(enfant)
				else:
					resultat += enfant.liste_elems_enfants(niveau)	
		elif self.type.indice > niveau:	
			parent = self.parent()
			while not parent.type.indice == niveau:
				parent = parent.parent()
			if not parent in resultat:
				resultat.append(parent)
		else:
			if not self in resultat:
				resultat.append(self)
		return sorted(resultat, key=lambda x:x.libelle)	


	def get_niveau(self, indice):
		elem =self
		niveau = self.type.indice
		if niveau > indice:
			while not niveau == indice:
				id_element = elem.id_element_racine
				elem = Structure.objects.get(id_element = id_element)
				niveau = elem.type.indice
				id_element = elem.id_element_racine
		else:
			elem = self
		return elem
	
	def parent(self):
		elems = Structure.objects.get(id_element= self.id_element_racine)
		return elems

	def enfants(self):
		elems = Structure.objects.filter(id_element_racine = self.id_element)
		return elems
			
	def localisation(self):
		local = self.code
		id_elem = self.id_element_racine
		while not id_elem == 0:
			elem = Structure.objects.get(id_element = id_elem)
			local = elem.code+'/'+local
			id_elem = elem.id_element_racine
		return local
				
	def get_secteurs(self):
		secteurs = []
		fin = False
		while not fin:
			les_enfants = self.enfants()
			#pprint.pprint(str(les_enfants))
			for enfant in les_enfants:
				#pprint.pprint('enfant = '+str(enfant)+' Niveau = '+str(enfant.type.indice))
				if enfant.type.indice == 4:
					#pprint.pprint('dernier niveau = '+str(enfant))
					secteurs.append(enfant)
				else:
					#pprint.pprint('Pas dernier niveau :'+str(enfant))
					secteurs = enfant.get_secteurs()
			fin = True
		return secteurs
			
					
		
	
	def __str__(self):
		return self.libelle	
		
class Organisation(models.Model):
	structure = models.ForeignKey(Structure,on_delete=models.CASCADE,null=True)
	tdc = models.FloatField(null=True)
	nbOperateur = models.IntegerField(null=True)


def liste_secteurs_enfants(secteur, liste):
	les_enfants = secteur.enfants()
	for enfant in les_enfants:
		if enfant.type.indice == INDICE_SECTEUR:
			liste.append(enfant)
		else:
			liste_secteurs_enfants(enfant, liste)
	return liste






class Moyens(models.Model):
	structure_id = models.ForeignKey(Structure, on_delete=models.CASCADE, null=True)
	numero = models.TextField(max_length=20)
	libelle = models.TextField(max_length=80)
	actif =models.BooleanField(default=False)
	nb_ctrls = models.IntegerField('Nb contrôle / tournée',default=2)
	datecreation = models.DateTimeField(auto_now_add=True)
	datemodif =models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.libelle

def get_chemin(instance, filename):
	return 'gammes/'+instance.moyen.numero+'/'+filename

class Gamme(models.Model):
	moyen = models.ForeignKey(Moyens, on_delete=models.CASCADE)
	intitule = models.TextField(max_length=50, null=True)
	fichier = models.FileField(upload_to=get_chemin, max_length=100)

	def __str__(self):
		return self.intitule





