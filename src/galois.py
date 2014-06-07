#*-coding:Utf-8 -*
#!/usr/bin/python3.2

"""Fichier Python contenant une classe simplifiée d'elements de corps de Galois avec p=2"""
from arith import *


def d(n,p):
	return len(bin(n)) - len(bin(p))

class elt(arith):
	"""Classe de l'element en question"""

	def __init__(self,n,p=2):
		"""Initialisation"""
		diff = d(n,p)
		while diff>= 0:
			n ^= p<<diff
			diff = d(n,p)
		self.valeur = n
		self.modulo = p

	def __repr__(self):
		"""Methode de représentation, similaire a int"""
		return str(self.valeur)

	def __eq__(self,autre):
		"""Methode d'egalite"""
		try:
			return self.valeur == autre.valeur
		except:
			return self.valeur == autre

	def int(self):
		"""Methode renvoyant un entier, a n'utiliser qu avec precaution, par exemple quand mod = 2"""
		return self.valeur

	def __neg__(self):
		"""Methode d'egalite, avec p=2 la caracteristique est de 2 donc self est egal a son inverse"""
		return self

	def __add__(self,autre):
		"""Methode d'addition par un autre elt ou par un scalaire"""
		try:
			return elt(self.valeur ^ autre.valeur,self.modulo)
		except AttributeError:
			return elt(self.valeur ^ autre,self.modulo)

	def __mul__(self,autre):
		"""Methode de multiplication"""
		a=self.valeur
		try:	
			b=autre.valeur
		except:
			b=abs(autre)
		resultat=0
		i=0
		while a!=0:
			resultat^=(a&1)*(b<<i)
			i+=1
			a=a>>1
		return elt(resultat,self.modulo)

	def __pow__(self,n):
		"""Exporapido"""
		if n == 0:
			return elt(1,self.modulo)
		elif n & 1 ==0:
			temp = self ** (n//2)
			return temp * temp
		else:
			temp = self ** (n//2)
			return self * temp * temp

	def __rdiv__(self,entier=1):
		"""Passage a l'oppose"""
		if self.valeur == 0:
			raise ZeroDivisionError
		else:
			return entier * self ** (2**d(self.modulo,0)-2)

	def __div__(self,autre):
		"""Methode de division dans le corps"""
		return self * (1/autre)

	def iter(self,n):
		"""Methode d'iteration de l'addition"""
		resultat = 0
		for i in range(n):
			resultat += self
		return resultat