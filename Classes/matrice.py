#*-coding:Utf-8 -*
#!/usr/bin/python3.2
"""Fichier Python contenant la classe matrice et les methodes associees """

from galois import *
from random import *
from arith import *
import numpy as np

class matrice(arith):
	"""Classe definissant l'element matrice en Python"""

	def __init__(self,nbligne,nbcolonne,tableau):
		"""Definition de la matrice avec gestion du cas erreur de taille"""
		try:
			if len(tableau) != nbligne * nbcolonne :
				raise IndexError("Erreur de taille de la matrice durant l'initialisation")
			self.nbligne=nbligne
			self.nbcolonne=nbcolonne
			self.tableau=tableau[::]
		except IndexError as ex:
			print(ex)
			print [nbligne,nbcolonne,tableau]
		except AttributeError as ex:
			print(ex)
			print [nbligne,nbcolonne,tableau]

	def __repr__(self):
		"""Representation de la matrice sous forme normalisee a l'appel de print"""
		try:
			rep = str(self.tableau[:self.nbcolonne])
			for i in xrange(1,self.nbligne):
				rep+="\n" + str(self.tableau[i*self.nbcolonne:self.nbcolonne * (i+1)])
			return rep
		except AttributeError:
			return "[]"

	def __str__(self):
		"""Definit la conversion d'une matrice en chaine de carateres """
		return self.__repr__()

	def __add__(self, autre):
		"""Methode d'addition de 2 matrices"""
		try:
			if self.nbcolonne != autre . nbcolonne:
				raise TypeError("Erreur dans la taille des matrices")
			tab = []
			for i in xrange(len(self.tableau)):
				tab.append(self.tableau[i] + autre.tableau[i])
			return matrice(self.nbligne,self.nbcolonne,tab)
		except TypeError as ex :
			print ex
		except AttributeError:
			print("On n'ajoute que des matrices entre elles")

	def __mul__(self,autre):
		"""Methode de multiplication par un scalaire et par une matrice"""
		try:
			if self.nbcolonne != autre.nbligne:
				raise TypeError("Probleme dans la taille des matrices a multiplier : "+str(self.nbcolonne) + " " + str(autre.nbligne))
			tab = []
			for i in xrange(self.nbligne * autre.nbcolonne):
				s=0
				x=i%autre.nbcolonne
				y=i/autre.nbcolonne
				for j in xrange(self.nbcolonne):
					s+=self.tableau[y*self.nbcolonne + j] * autre.tableau[x + j * autre.nbcolonne]
				tab.append(s)
			return matrice(self.nbligne,autre.nbcolonne,tab)
		except AttributeError:
			tab = []
			for i in self.tableau:
				tab.append(autre * i)
			return matrice(self.nbligne,self.nbcolonne,tab)
		except TypeError as ex:
			print ex

	def __pow__(self,indice):
		"""Methode pour les puissances de matrice"""
		try:
			if self.nbligne != self.nbcolonne:
				raise TypeError("Hop, hop, hop matrices carrées s'il te plait")
			if type(indice)!=type(0):
				raise TypeError("On ne fait que des indices entiers")
			if indice==1:
				return self
			else:
				N=self ** (indice//2)
				if indice%2 == 0:
					return N*N
				else:
					return self*N*N
		except TypeError as ex:
			print ex
		except AttributeError:
			print("Dans pow, erreur d'attribut")

	def transpose(self):
		"""Methode pour passer a la transposee"""
		try:
			new_tableau = []
			for i in xrange(self.nbcolonne):
				new_tableau += self.tableau[i::self.nbcolonne]
			return matrice(self.nbcolonne,self.nbligne,new_tableau)
		except AttributeError:
			print("Erreur d'attributs")

	def copie(self):
		"""Methode de copie de matrice"""
		try:
			new_tableau=[]
			for i in self.tableau:
				new_tableau.append(i+0)
			return matrice(self.nbligne,self.nbcolonne,new_tableau)
		except AttributeError:
			print("Probleme d'attribut")

	def echange(self,ligne1,ligne2):
		"""Methode d'echange de ligne dans une matrice"""
		try:
			resultat = self.tableau[::]
			if ligne1<1 or ligne1>self.nbligne or ligne2<1 or ligne2 > self.nbligne:
				raise IndexError("Probleme dans le choix des lignes a echanger "+str(ligne1) + " " + str(ligne2) +"  "+ str(self.nbligne))
			aux=resultat[self.nbcolonne * (ligne1 - 1):self.nbcolonne * (ligne1):]
			resultat[self.nbcolonne * (ligne1-1):self.nbcolonne * (ligne1):]=resultat[self.nbcolonne * (ligne2-1):self.nbcolonne * (ligne2):]
			resultat[self.nbcolonne * (ligne2-1):self.nbcolonne * (ligne2):]=aux
			return matrice(self.nbligne,self.nbcolonne,resultat)
		except AttributeError:
			print("Probleme d'attribut")
		except IndexError as ex:
			print ex
			return self

	def echange_colonnes(self,colonne1,colonne2):
		"""Methode d'echange de colonnes"""
		return self.transpose().echange(colonne1,colonne2).transpose()

	def mult_ligne(self,ligne,scalaire):
		"""Methode de multiplication d'une ligne par un scalaire"""
		try:
			if ligne<1 or ligne>self.nbligne:
				raise IndexError("Probleme dans le choix de la ligne")
			resultat = self.tableau[::]
			resultat[self.nbcolonne * (ligne-1):self.nbcolonne * (ligne):]=[scalaire*i for i in resultat[self.nbcolonne * (ligne-1):self.nbcolonne * (ligne):]]
			return matrice(self.nbligne,self.nbcolonne,resultat)
		except AttributeError:
			print("Probleme d'attribut")
		except IndexError as ex:
			print ex
			print("durant mult_ligne")
			return self

	def cblineaire(self,ligne1,ligne2,scalaire=1):
		"""Methode de cb lineraire qui retourne a la ligne 1 : ligne1+scalaire*ligne2"""
		try:

			resultat = self.tableau[::]
			if ligne1<1 or ligne1>self.nbligne or ligne2<1 or ligne2 > self.nbligne:
				raise IndexError("Probleme dans le choix des lignes a echanger")
			resultat[self.nbcolonne * (ligne1-1):self.nbcolonne * (ligne1):]=[resultat[(ligne1-1)*self.nbcolonne+i] + scalaire*resultat[(ligne2-1)*self.nbcolonne+i] for i in xrange(self.nbcolonne)]
			return matrice(self.nbligne,self.nbcolonne,resultat)
		except AttributeError:
			print("Probleme d'attribut")
		except IndexError as ex:
			print ex
			print("durant cblineaire avec les lignes {0}, {1} et le scalaire{2}".format(ligne1,ligne2,scalaire))
			return self

	def gauss(self,complet):
		"""Methode de pivot de Gauss :utile pour le rang et le calcul de l'inverse
		complet est un booleen qui dit si on doit faire les meme choses pour l identite"""
		inversibilite=True
		n=self.nbligne

		#Une copie est necessaire pour ne pas overwritten self
		M=self.copie()	

		#initialisation d'une matrice identite
		identite= [0 for i in range(n**2)]
		identite[::n+1]=[1 for i in range(n)]
		identite = matrice(n,n,identite)

		#Liste des permutations de [lignes,colonnes] faites par Gauss	
		permut = []

		#boucle de descente, i représente le numero de la diagonale recherchee de la ligne 1(0) a n(n-1)
		for i in xrange(n):				
			j=i

			#Recherche d'une ligne dont le coefficient i soit non nul
			while j<n and M.tableau[n*j+i]==0:
				j+=1

			if M.nbligne!=M.nbcolonne:
				inversibilite=False
				break
			
			#Si j==n alors aucun coefficient n'est non nul donc self pas inversible
			if j==n:
				inversibilite=False	 	
				ligne,colonne=i,i

				#C'est pas inversible mais on continue de chercher une valeur non nulle pour trouver le rang
				while colonne<n and M.tableau[n*ligne + colonne]==0 :
					colonne += (ligne+1)//(n)
					ligne=(ligne+1-i)%(n-i) +i
				if colonne==n:
					break
				else :
					M=M.echange(i+1,ligne+1)
					M=M.echange_colonnes(i+1,colonne+1)
					j=i
					permut.append([i,ligne,colonne])
			else:
				permut.append([i,j,i])
				#Si i!=j, alors on doit echanger les lignes i+1 et j+1
				if i!=j:					
					M=M.echange(i+1,j+1)
					#On fait de meme sur la matrice identite
					if complet :
						identite=identite.echange(i+1,j+1)

			#Si le coefficient diagonnal !=1 on le rend egal a un par multiplication par son inverse		
			if M.tableau[i*n+i]!=1:		
				scalaire=1/M.tableau[i*n+i]
				M=M.mult_ligne(i+1,scalaire)
				if complet:
					identite=identite.mult_ligne(i+1,scalaire)

			#Propagation : pour toutes les lignes sous la ligne i on rend les coefficients i nuls
			for j in xrange(i+1,n):	
				scalaire=-M.tableau[j*n+i]
				M=M.cblineaire(j+1,i+1,scalaire)
				if complet:
					identite=identite.cblineaire(1+j,i+1,scalaire)			

		#si notre matrice est toujours inversible on remonte ! Pire que faire de la randonnée !
		if inversibilite and complet:	

			#I designe toujours la ligne consideree, la meme chose en symetrique
			for  i in xrange(n-1,-1,-1):		
				j=i
				while j>=0 and M.tableau[n*j+i]==0:
					j-=1
				if j==-1:
					inversibilite=False
					break
				if i!=j:
					M=M.echange(i+1,j+1)
					identite=identite.echange(i+1,j+1)
				if M.tableau[i*n+i]!=1:
					scalaire=1/M.tableau[i*n+i]
					M=M.mult_ligne(i+1,scalaire)
					identite=identite.mult_ligne(i+1,scalaire)
				for j in xrange(i-1,-1,-1):
					scalaire=-M.tableau[j*n+i]
					M=M.cblineaire(j+1,i+1,scalaire)
					identite=identite.cblineaire(1+j,i+1,scalaire)
		if inversibilite:
			return {"inverse":identite,"permut":permut,"inversibilite":inversibilite}
		else:
			#Par defaut, si la matrice n'est pas inversible bah on renvoie 0 pour pas decevoir
			return {"inverse":matrice(n,n,[0 for i in range(n**2)]),"permut":permut,"inversibilite":inversibilite}

	def inverse(self):
		"""Methode de calcul de l'inverse d'une matrice"""
		return self.gauss(True)["inverse"]

	def reorganise(self):
		"""Methode pour mettre un carre inversible en haut a gauche"""

		#Si la matrice n'est pas carre on la complete pour rentrer dans gauss
		if self.nbligne < self.nbcolonne :
			M = matrice(self.nbcolonne,self.nbcolonne,self.tableau + [0 for i in range(self.nbcolonne*(self.nbcolonne - self.nbligne))])
		elif self.nbligne>self.nbcolonne :
			M = matrice(self.nbligne,self.nbligne,self.transpose().tableau + [0 for i in range(self.nbligne*(self.nbligne - self.nbcolonne))]).transpose()
		else :
			M=self
		#on initialise la matrice resultat a tableau
		Gauss = M.gauss(False)

		#Toutes les lignes et colonnes permutees par gauss sont dans permut et on retourne la matrice
		for triple in Gauss["permut"]:
			M=M.echange(triple[0]+1,triple[1]+1)
			M=M.echange_colonnes(triple[0]+1,triple[2]+1)

		return {"tasse":M.bloc(1,1,self.nbligne,self.nbcolonne),"permut":Gauss["permut"]}

	def bloc(self,debutLigne,debutColonne,finLigne,finColonne):
		"""Methode qui forme une matrice bloc de self, bornes incluses"""
		n = self.nbcolonne
		largeur=finColonne - debutColonne +1
		hauteur = finLigne - debutLigne +1
		tableau = []
		for i in range(hauteur):
			tableau+=self.tableau[debutColonne-1+n*(i+debutLigne-1):finColonne+n*(i+debutLigne-1)]
		return matrice(hauteur,largeur,tableau)

	def MtoGalois(M,mod):
		"""Transforme une matrice d'entier en elt de galois avec p le modulo"""
		resultat=[]
		for i in M.tableau:
			resultat.append(elt(i,mod))
		return matrice(M.nbligne,M.nbcolonne,resultat)

	#Au dela de cette ligne de code ne se trouvent que des methodes a appliquer sur des matrices a coefficients dans Z/2Z via Galois
	#On ne garantit aucun resultat dans le cas contraire

	def RendInversible(self):
		"""Methode qui renvoie une matrice inversible proche de self, quand self est a coefficient dans elt 2"""
		
		if self.nbligne == self.nbcolonne :
			inversibilite=True
			n=self.nbligne

			#M (resp S) est une copie qui va subir le pivot de Gauss (resp subir les echanges de lignes)
			M=self.copie()	
			S=self.copie()

			#Liste des echanges de ligne
			Ech=[]

			#boucle de descente, i représente le numero de la diagonale recherchee de la ligne 1(0) a n(n-1)
			for i in xrange(n):
				j=i

				#Recherche d'une ligne dont le coefficient i soit non nul
				while j<n and M.tableau[n*j+i]==0:
					j+=1

				#Si tous les coeff i sont nuls alors on on modifie la matrice initiale en ajoutant 1 en case [i,i]
				if j==n:	
					M.tableau[i*n+i]+=elt(1)
					S.tableau[i*n+i]+=elt(1)

				#Si i!=j, alors on doit echanger les lignes i+1 et j+1 et on retient les échanges
				if i!=j and j!=n:
					M=M.echange(i+1,j+1)
					S=S.echange(i+1,j+1)
					Ech.append([i+1,j+1])

				#Si le coefficient diagonnal !=1 on le rend egal a un par multiplication par son inverse
				if M.tableau[i*n+i]!=1:
					scalaire=1/M.tableau[i*n+i]
					M=M.mult_ligne(i+1,scalaire)

				#Propagation : pour toutes les lignes sous la ligne i on rend les coefficients i nuls
				for j in xrange(i+1,n):
					scalaire=-M.tableau[j*n+i]
					M=M.cblineaire(j+1,i+1,scalaire)

			#On refait les échanges sur la matrice S pour retrouver self avec les coeff changés pour qu'elle soit inversible
			for x in xrange(len(Ech)-1,-1,-1):
				S=S.echange(Ech[x][0],Ech[x][1])
			return S
		else :
			print "On n'inverse que des matrices carrees"

def me2np(self):
	"""Convertit notre belle matrice vers Numpy si elle est binaire"""
	trans = []
	for i in range(self.nbligne):
			trans.append([c.valeur for c in self.tableau[i*self.nbcolonne:(i+1)*self.nbcolonne:] ])
	return np.matrix(trans,dtype=bool)

def np2me(self):
	trans = self.getA1()
	ligne,colonne = np.shape(self)

	resultat = []
	for i in trans:
		if i :
			resultat.append(elt(1,2))
		else:
			resultat.append(elt(0,2))
	return matrice(ligne,colonne,resultat)


def M_coller(C1,C2,C3,C4):
	"""Methode pour coller des blocs sur une matrice"""
	taille = C1.nbligne

	resultat = []
	for i in xrange(taille):
		resultat += C1.tableau[i*taille:(i+1)*taille]
		resultat += C2.tableau[i*taille:(i+1)*taille]
	for i in xrange(taille):
		resultat += C3.tableau[i*taille:(i+1)*taille]
		resultat += C4.tableau[i*taille:(i+1)*taille]
	return matrice(2*taille,2*taille,resultat)



def permutation(taille):
	"""Methode de generation d'une matrice de permutation aleatoire, a coefficients dans Galois"""

	tableau = [elt(0,2) for i in range(taille**2)]
	libre = range(taille)
	for i in range(taille)[::-1]:
		tableau[i*taille + libre.pop(randint(0,i))] = elt(1,2)
	return matrice(taille,taille,tableau)

def inversible(taille):
	"""Methode de generation aleatoire d'une matriceinversible dans Galois"""

	tableau = []
	for i in xrange(taille**2):
		tableau.append(elt(randint(0,1)))
	return matrice(taille,taille,tableau).RendInversible()

def strassen(A,B):
	"""Supposons que self et autre sont carrees de taille puissance de 2"""
	taille = A.nbligne
	mid = taille//2	

	if taille > 32:
		M1 = strassen( (A.bloc(1,1,mid,mid) + A.bloc(mid+1,mid+1,taille,taille)) , (B.bloc(1,1,mid,mid) + B.bloc(mid+1,mid+1,taille,taille)) )
		M2 = strassen( (A.bloc(mid+1,1,taille,mid) + A.bloc(mid+1,mid+1,taille,taille)) , (B.bloc(1,1,mid,mid)) )
		M3 = strassen( (A.bloc(1,1,mid,mid)) , (B.bloc(1,mid+1,mid,taille) - B.bloc(mid+1,mid+1,taille,taille)) )
		M4 = strassen( (A.bloc(mid+1,mid+1,taille,taille)) , (B.bloc(mid+1,1,taille,mid) - B.bloc(1,1,mid,mid)) )
		M5 = strassen( (A.bloc(1,1,mid,mid) + A.bloc(1,mid+1,mid,taille)) , (B.bloc(mid+1,mid+1,taille,taille)) )
		M6 = strassen( (A.bloc(mid+1,1,taille,mid) - A.bloc(1,1,mid,mid)) , (B.bloc(1,1,mid,mid) + B.bloc(1,mid+1,mid,taille)) )
		M7 = strassen( (A.bloc(1,mid+1,mid,taille) - A.bloc(mid+1,mid+1,taille,taille)) , (B.bloc(mid+1,1,taille,mid) + B.bloc(mid+1,mid+1,taille,taille)) )

		C1 = M1 + M4 - M5 + M7
		C2 = M3 + M5
		C3 = M2 +M4
		C4 = M1 -M2 +M3 +M6

		return M_coller(C1,C2,C3,C4)
	else:
		return A*B

A = matrice(3,3,[1,0,0,0,1,0,0,1,1]).MtoGalois(2)