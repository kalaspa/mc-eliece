#*-coding:Utf-8 -*
#!/usr/bin/python3.2
"""Fichier contenant une classe de polynomes """

from galois import *
from arith import *

class polynome(arith):
	"""Classe de polynomes"""

	def __init__(self,liste):
		"""Initialisation de l'objet"""
		try:
			self.liste=liste[::]
		except TypeError:
			print("Un polynome recoit une liste en facteur")

	def __repr__(self):
		"""Representation du polynome lorsqu'il est appelé par print ou autre"""
		string=""
		if self.liste == []:
			return "0"
		for indice in xrange(len(self.liste)):
			if self.liste[indice]!=0:
				if string=='':
					string="{0}*X^{1}".format(self.liste[indice],indice)
				else:
					string+=" + {0}*X^{1}".format(self.liste[indice],indice)
		return string

	def __getitem__(self,index):
		"""Permet d'acceder au coefficient de degre index par polynome[index]"""
		try:
			return self.liste[index]
		except IndexError:
			return 0
		except TypeError:
			print("Un index doit etre un entier")

	def __setitem__(self,index,valeur):
		"""Methode d'attribution d'une valeur a un coefficient par polynome[index]="""
		try:
			self.liste[index]=valeur+0
		except IndexError:
			while index>= len(self.liste)-1:
				self.liste.append(0)
			self.liste[index]=valeur+0
		except TypeError:
			print("Un index doit etre un entier")

	def __eq__(self,autre):
		"""Methode d'egalite entre les polynomes ou avec un scalaire"""
		try:
			return self.reduction().liste== autre.reduction().liste
		except AttributeError:
			return (self[0]==autre) and (len(self.reduction().liste)<=1)

	def copie(self):
		"""Methode de copie de poynome"""
		resultat = self.liste[:]
		return polynome(resultat)

	def reduction(self):
		"""Enleve les coefficients dominants nuls"""
		dominant=0
		while self.liste!=[] and dominant==0: #Tant que le polynome est non nul et qu'il a un coefficient dominant nul, on le couic
			dominant = self.liste.pop()        #le pop recupere et enleve la derniere valeur de la liste cf les piles
		if not(dominant==0):
			self.liste.append(dominant)     #On rajoute le pauvre coefficient non nul qu'on a enleve
		return self

	def degre(self):
		"""Determine le degre du polynome"""
		return len(self.reduction().liste)-1

	def __add__(self,autre):
		"""Somme de polynomes, ou avec un scalaire"""
		try:
			if self.degre()<autre.degre():  #ordonnancement des polynomes en fonction de leur degré
				resultat=autre.liste[::]  #notre resultat prend la valeur du plus grand polynome
				r2=self.liste
			else:
				resultat=self.liste[::]
				r2=autre.liste
			for indice in xrange(len(r2)):
				resultat[indice]+=r2[indice]  #On lui ajoute les coefficients du petit
			return polynome(resultat).reduction()
		except AttributeError:
			try:
				resultat = self.liste[::] #Addition à un scalaire
				resultat[0]+=autre
				return polynome(resultat)
			except IndexError:
				self.liste=[autre]
				resultat=self.liste
				return polynome(resultat)

	def __mul__(self,autre):
		"""Multiplication d'un polynome avec un scalaire ou un autre polynome"""
		try:
			#Multiplication par un polynome
			resultat = [0 for i in range(self.degre() + autre.degre()+1)]
			for i in xrange(self.degre()+1):
				for j in xrange(autre.degre()+1):
					resultat[i+j]+=self.liste[i]*autre.liste[j]
			return polynome(resultat).reduction()
		except AttributeError:
			#multiplication par un scalaire, donc un entier ou un reel
			resultat=self.liste[:]
			for indice in xrange(len(resultat)):
				resultat[indice]*=autre
			return polynome(resultat).reduction()

	def division(self,autre):
		"""Algorithme de division euclidienne"""
		reste = self.copie()
		quotient,aux,b=polynome([]),polynome([]),autre.degre()
		while reste.degre() >=b:
			r=reste.degre()
			aux[r-b]=reste[r]/autre[b]
			a=aux[r-b]
			restebis=[0 for i in xrange(r+1)]
			restebis[:r-b:]=reste.liste[:r-b:]
			restebis[r-b::]=[reste[i]-autre[i-r+b]*a for i in range(r-b,r)]
			reste=polynome(restebis)
			quotient += aux
			aux = polynome([])
		return {"reste":reste,"quotient":quotient}

	def __floordiv__(self,autre):
		"""Methode de division euclidienne des polynomes : quotient"""
		return self.division(autre)["quotient"]

	def __mod__(self,autre):
		"""Methode de division euclidienne des polynomes : reste"""
		return self.division(autre)["reste"]

	def __call__(self,x):
		"""Methode de calcul de P(x)"""
		resultat = 0
		for i in xrange(len(self.liste)):
			resultat += self[i] * (x**i)
		return resultat

	def __pow__(self,indice):
		"""Methode pour les puissances de poynome"""
		if indice == 0:
			return polynome([1])
		elif indice==1:
			return self
		else:
			N=self ** (indice//2)
			if indice % 2 == 0:
				return N*N
			else:
				return self*N*N

	def powmod(self,indice,P):
		"""Methode d'exponentiation rapide modulo"""
		if indice == 0:
			return polynome([1])
		elif indice==1:
			return self
		else:
			N=self.powmod(indice//2,P)
			if indice%2 == 0:
				return N*N %P
			else:
				return self*N*N %P

	def PtoGalois(P,mod):
		"""Transforme un polynome d'entiers en polynome de Galois"""
		resultat = []
		for i in P.liste :
			resultat.append(elt(i,mod))
		return polynome(resultat)

def pgcd(a,b):
	"""Methode de calcul du PGCD de deux polynomes, nombres"""
	while b != 0:
		a,b = b,a%b
	return a