#*-coding:Utf-8 -*
#!/usr/bin/python3.2
"""Fichier contenanr les classes de clefs publiques et privées"""


import pickle
from matrice import *
from galois import *
from random import *
from goppa import *


#Un ensemble de fonctions pour manipuler des strings et des fichiers

def string2bin(s):
	"""Convertit un string en une chaine de binaires"""

	return ''.join('%s'%('0'*(8-len(bin(ord(c))[2:])))+bin(ord(c))[2:] for c in s)

def bin2string(chaine,couper):
	"""Convertit une chaine de binaire en un string"""

	message = ''
	while chaine != '':
		octet = chaine[:8:]
		if octet == '00000000' and couper:
			break
		message += chr(int('0b'+octet,2))
		chaine = chaine[8::]
	return message

def string2blocbin(string,k):
	"""Convertit un string en bloc de binaire"""

	chaine = string2bin(string)
	liste = []
	while chaine !='':
		morceau = chaine[:k:]
		chaine = chaine[k::]
		vecteur =  []
		for i in morceau:
			vecteur.append(elt(int(i),2))
		vecteur = vecteur + [0 for i in range(k - len(vecteur))]
		liste.append(matrice(k,1,vecteur))
	return liste

def file2blocbin(fichier,k):
	"""Convertit un fichier texte en une liste de vecteurs d'elements de Z/2Z via Galois"""

	with open(fichier,"rb") as f:
		string = f.read()
	return string2blocbin(string,k)

def blocbin2string(liste,couper):
	"""Convertit une liste de vecteurs en string"""

	chaine = ''
	for vecteur in liste:
		for i in vecteur.tableau :
			chaine += str(i)
	string = bin2string(chaine,couper)
	return string

def blocbin2file(fichier,liste,couper):
	"""Convertit une liste de vecteur en un fichier texte"""

	string = blocbin2string(liste,couper)
	with open(fichier,"wb") as f:
		f.write(string)


#Un ensemble de classes de clef reunissant les fonctions importantes du programme

#Obsolete mais on la garde au cas ou.
class clef(object):
	"""Classe de clef dans le cyrptosysteme de Mc Eliece
	Construit de objets sauvegardables dans des fichiers via pickle"""

	def save(self,fichier):
		"""Methode pour sauvegarder la clef dans fichier, ou fichier est un string"""

		with open(fichier, 'wb') as f:
			mon_pickler = pickle.Pickler(f)
			mon_pickler.dump(self)

	def load(self,fichier):
		"""Methode pour charger la clef dans un fichier"""

		with open(fichier,'rb') as f:
			mon_depickler = pickle.Unpickler(f)
			recupere = mon_depickler.load()
		return recupere

class clef_publique(clef):
	"""Classe de clef publique du cryptosysteme de Mc Eliece
	Permet le chiffrage"""

	def __init__(self,Gprime=0,correction=0):
		"""Methode d'initialisation de la clef publique
		Gprime doit etre de taille n,k"""
		self.Gprime = Gprime
		self.correction=correction

	def save(self,fichier):
		"""Methode de sauvegarde d'une clef publique"""

		string = ''
		string += str(self.correction) + "1234567890"
		string += str(self.Gprime.nbligne) + "1234567890"
		string += str(self.Gprime.nbcolonne) + "1234567890"
		string += blocbin2string([self.Gprime],False)
		with open(fichier,'wb') as f:
			f.write(string)

	def load(self,fichier):
		"""Methode de chargement d'une clef publique"""

		with open(fichier,'rb') as f:
			string = f.read()
		liste = string.split("1234567890")
		correction = int(liste[0])
		n = int(liste[1])
		k = int(liste[2])
		Gprime = matrice(n,k,string2blocbin(liste[3],k*n)[0].tableau)
		return clef_publique(Gprime,correction)

	def chiffrer(self,f_source,f_cible):
		"""Methode pour chiffrer le message
		Reste a savoir comment on se forme le message : liste de vecteurs"""
		
		message = file2blocbin(f_source,self.Gprime.nbcolonne)
		resultat = []
		for vecteur in message:
			erreur = [0 for i in range(self.Gprime.nbligne)]
			for i in range(self.correction):
				erreur[randint(0,self.Gprime.nbligne-1)]=elt(1,2)
			erreur = matrice(self.Gprime.nbligne,1,erreur)
			resultat.append((self.Gprime * vecteur) + erreur)
		blocbin2file(f_cible,resultat,False)

	def new(self,privkey):
		"""Methode pour creer une clef publique a partir d'une clef publique"""

		return clef_publique(privkey.P * (privkey.G* privkey.Q),privkey.correction)
		

class clef_privee(clef):
	"""Classe de clef privee du cryptosysteme de Mc Eliece
	Permet le dechiffrage et la generation du code"""

	def __init__(self,G=0,P=0,D=0,Q=0,Qinv=0,g=0,support=0,L_fi=0,mod = 0,correction=0):
		"""Methode d'initialisation de la clef privee
		G de taille n,k
		P permutation de taille n,n
		Q inversible de taille k,k"""
		self.G=G
		self.P = P
		self.D = D
		self.Q = Q
		self.Qinv=Qinv
		self.g = g
		self.support = support
		self.L_fi = L_fi
		self.mod = mod
		self.correction = correction

	def save(self,fichier):
		"""Methode de sauvegarde d'une clef privee"""

		string = ''
		string += blocbin2string([self.G],False)+ "1234567890" #0
		string += blocbin2string([self.P],False)+ "1234567890"
		string += blocbin2string([self.D],False)+ "1234567890"
		string += blocbin2string([self.Q],False)+ "1234567890"
		string += blocbin2string([self.Qinv],False)+ "1234567890"
		string += str(self.g.liste)+ "1234567890" #5
		string += str(self.support)+ "1234567890"
		#L_fi on le recalculera parce que c'est galere a stocker...
		string += str(self.mod) + "1234567890"
		string += str(self.correction)+ "1234567890"
		string += str(self.G.nbligne)+ "1234567890" 
		string += str(self.G.nbcolonne)+ "1234567890" #10
		with open(fichier,'wb') as f:
			f.write(string)

	def load(self,fichier):
		"""Methode de chargement d'une clef privee"""

		with open(fichier,'rb') as f:
			string = f.read()
		liste = string.split("1234567890")

		n = int(liste[9])
		k = int(liste[10])
		correction = int(liste[8])
		mod = int(liste[7])

		#Methode bizarre pour les listes, on enleve la tete, on retourne, on enleve la tete (queue initiale) et on remet dans le bon sens
		#Ensuite on split car le string initial est '[1,2,3]'
		gp =(((liste[5][1::])[::-1])[1::])[::-1].split(',')
		g = []
		for i in gp:
			g.append(elt(int(i),mod))
		g = polynome(g)

		support = []
		supportp = (((liste[6][1::])[::-1])[1::])[::-1].split(',')
		for i in supportp:
			support.append(elt(int(i),mod))

		G = matrice(n,k,string2blocbin(liste[0],k*n)[0].tableau)
		P = matrice(n,n,string2blocbin(liste[1],n*n)[0].tableau)
		D = matrice(k,n,string2blocbin(liste[2],k*n)[0].tableau)
		Q = matrice(k,k,string2blocbin(liste[3],k*k)[0].tableau)
		Qinv = matrice(k,k,string2blocbin(liste[4],k*k)[0].tableau)

		L_fi = fi(g,support,mod)

		return clef_privee(G,P,D,Q,Qinv,g,support,L_fi,mod,correction)

	def new(self,mod,correction):
		"""Methode pour generer une clef privee aleatoire"""

		n = 2**(d(mod,0))

		#Generation de g
		g = P_irreductible(2*correction+1,mod)
		print '-Polynome genere'

		#Generation du support aleatoire
		liste = range(n)
		support = []
		for i in range(n)[::-1]:
			support.append(elt(liste.pop(randint(0,i)),mod))
		L_fi = fi(g,support,mod)
		print '-Support genere'

		#Generation de la matrice de parite et de ses dependances
		H = parite(g,support,mod)
		print "-H generee"
		G = generatrice(H)
		print "-G generee"
		D = decodage(G)
		print '-D generee'

		#Generation des matrices de melange
		P = permutation(n)
		print "-P generee"
		Q = inversible(G.nbcolonne)
		print '-Q generee'
		Qinv = Q.inverse()
		print "-Q inverse calculee"

		return clef_privee(G,P,D,Q,Qinv,g,support,L_fi,mod,correction)

	def dechiffrer(self,f_source,f_cible):
		"""Methode pour dechiffrer un fichier code avec la bonne clef"""

		print "-Conversion du fichier en bloc de bits"
		liste = file2blocbin(f_source,self.G.nbligne)

		print "-Inversion des matrices de la clef privee"
		Per = self.P.transpose()
		Qinv = self.Qinv
		
		#On calcule Per * mot comme le dit Mc Eliece
		#On corrige les fautes
		#Puis on fait Qinv fois le reste pour retrouver le mot de Fn d'origine
		#Enfin on passe le tout a la matrice de decodage pour retrouver le mot de Fk
		print "-Decodage des blocs de bits"
		resultat = []
		for mot in liste:
			mot = Per * mot
			mot = corrige(self.g,mot,self.support,self.L_fi,self.mod)
			mot = self.D * mot
			mot  = Qinv * mot
			resultat.append(mot)


		print "-Inscription du message dans le fichier source"
		blocbin2file(f_cible,resultat,True)


class clef_correcteur(clef):
	"""Une classe de clef qui ne sert qu'a corriger des erreurs"""

	def __init__(self,G=0,D=0,g=0,support=0,L_fi=0,mod=0,correction=0):
		self.G = G
		self.D = D
		self.g = g
		self.support = support
		self.L_fi = L_fi
		self.correction = correction
		self.mod = mod
		
	def new(self,mod,correction):
		"""Methode pour generer une clef privee aleatoire"""

		n = 2**(d(mod,0))

		#Generation de g
		g = P_irreductible(2*correction+1,mod)
		print '-Polynome genere'

		#Generation du support aleatoire
		liste = range(n)
		support = []
		for i in range(n)[::-1]:
			support.append(elt(liste.pop(randint(0,i)),mod))
		L_fi = fi(g,support,mod)
		print '-Support genere'

		#Generation de la matrice de parite et de ses dependances
		H = parite(g,support,mod)
		print "-H generee"
		G = generatrice(H)
		print "-G generee"
		D = decodage(G)
		print '-D generee'

		return clef_correcteur(G,D,g,support,L_fi,mod,correction)

	def save(self,fichier):
		"""Methode de sauvegarde d'une clef goppa, l'indicage est le meme que pour la clef privee"""

		string = ''
		string += blocbin2string([self.G],False)+ "1234567890" #0
		string += blocbin2string([self.D],False)+ "1234567890"
		string += str(self.g.liste)+ "1234567890" 
		string += str(self.support)+ "1234567890"
		#L_fi on le recalculera parce que c'est galere a stocker...
		string += str(self.mod) + "1234567890"
		string += str(self.correction)+ "1234567890" #5
		string += str(self.G.nbligne)+ "1234567890" 
		string += str(self.G.nbcolonne)+ "1234567890"
		with open(fichier,'wb') as f:
			f.write(string)

	def load(self,fichier):
		"""Methode de chargement d'une clef goppa, l'indicage est le meme que pour la clef privee"""

		with open(fichier,'rb') as f:
			string = f.read()
		liste = string.split("1234567890")

		n = int(liste[6])
		k = int(liste[7])
		correction = int(liste[5])
		mod = int(liste[4])

		#Methode bizarre pour les listes, on enleve la tete, on retourne, on enleve la tete (queue initiale) et on remet dans le bon sens
		#Ensuite on split car le string initial est '[1,2,3]'
		gp =(((liste[2][1::])[::-1])[1::])[::-1].split(',')
		g = []
		for i in gp:
			g.append(elt(int(i),mod))
		g = polynome(g)

		support = []
		supportp = (((liste[3][1::])[::-1])[1::])[::-1].split(',')
		for i in supportp:
			support.append(elt(int(i),mod))

		G = matrice(n,k,string2blocbin(liste[0],k*n)[0].tableau)
		D = matrice(k,n,string2blocbin(liste[1],k*n)[0].tableau)

		L_fi = fi(g,support,mod)

		return clef_correcteur(G,D,g,support,L_fi,mod,correction)

	def chiffrer(self,f_source,f_cible):
		"""Methode pour chiffrer le message
		Reste a savoir comment on se forme le message : liste de vecteurs"""
		
		message = file2blocbin(f_source,self.G.nbcolonne)
		resultat = []
		for vecteur in message:
			resultat.append(self.G * vecteur)
		blocbin2file(f_cible,resultat,False)

	def dechiffrer(self,f_source,f_cible):
		"""Methode pour dechiffrer un fichier code avec la bonne clef"""

		print "-Conversion du fichier en bloc de bits"
		liste = file2blocbin(f_source,self.G.nbligne)
		
		#On corrige les fautes
		#Enfin on passe le tout a la matrice de decodage pour retrouver le mot de Fk
		print "-Decodage des blocs de bits"
		resultat = []
		for mot in liste:
			mot = corrige(self.g,mot,self.support,self.L_fi,self.mod)
			mot = self.D * mot
			resultat.append(mot)
		
		print "-Inscription du message dans le fichier source"
		blocbin2file(f_cible,resultat,True)