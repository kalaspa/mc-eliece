#*-coding:Utf-8 -*
#!/usr/bin/python3.2
"""Fichier contenant une classe de Corps fini de Galois, puissance d'un nombre premier, pour p=2 depassé par galois.py"""

from poly import *
from decorateur import*
from arith import *

class ZpZ(arith):
	"""Classe d element de Z/pZ"""

	def __init__(self,valeur,p=2):
		"""Initialisation de l'element"""
		try:
			if type(p)!=type(1):
				raise TypeError("Le modulo doit etre un entier")
			self.modulo=p
			if type(valeur)!=type(1):
				raise TypeError("La valeur doit etre un entier")
			self.valeur = valeur % p
		except TypeError as ex:
			print ex

		except:
			print("Il y a une erreur dans l'affectation,")

	def __repr__(self):
		"""Representation de l'element"""
		try :
			return str(self.valeur)
		except AttributeError:
			return ""

	def __eq__(self,autre):
		"""Definition de l'egalite de deux elements"""
		try:
			return self.valeur==autre.valeur
		except AttributeError:
			return self.valeur==autre

	def __add__(self,autre):
		"""Methode d'addition"""
		try:
			if self.modulo != autre.modulo:
				raise TypeError("Les deux variables n'ont pas le meme modulo")
			return ZpZ(self.valeur + autre.valeur,self.modulo)
		except TypeError as ex:
			print(ex)
		except AttributeError:
			return ZpZ(self.valeur + autre,self.modulo)


	def __mul__(self,autre):
		"""Methode de multiplication"""
		try:
			if self.modulo != autre.modulo:
				raise TypeError("Différence dans les modulo")
			return ZpZ(self.valeur * autre.valeur,self.modulo)
		except TypeError as ex:
			print(ex)
		except AttributeError:
			return ZpZ(self.valeur * autre,self.modulo)


	def __pow__(self,indice):
		"""Methode pour les puissances modulaires en mode exporapido"""
		if indice==0:
			return ZpZ(1,self.modulo)
		else:
			if indice==1:
				return self
			else:
				N=self ** (indice//2)
				if indice%2 == 0:
					return N*N
				else:
					return self*N*N
	
	def euclide(self):
		"""Algorithme d'euclide"""
		a = self.valeur
		b = self.modulo
		r = a
		r1 = b
		u = 1
		v = 0
		u1 = 0
		v1 = 1
		while (r1 != 0):
			q = r//r1
			rs = r
			us = u
			vs = v
			r = r1
			u = u1
			v = v1
			r1 = rs - q *r1
			u1 = us - q*u
			v1 = vs - q*v1
		return [r, u, v] # tels que a*u + b*v = r et r = pgcd (a, b)

	def __div__(self,autre):	#peut s'appeler aussi truediv suivant les versions de python
		"""Methode de division dans Z/pZ"""
		try:
			if self.modulo != autre.modulo:
				raise TypeError("Erreur dans le modulo des variables")
			if self.valeur == 0:
				raise ZeroDivisionError
			l = autre.euclide()
			return self * l[1]
		except AttributeError:
			print("On va eviter de diviser par autre chose qu'un element du corps")
		except TypeError as ex:
			print(ex)

	def __rdiv__(self,autre):
		"""Methode de division dans l'autre sens, c'est à dire int/ZpZ"""
		l = self.euclide()
		return ZpZ(autre * l[1],self.modulo)

def toZpZ(self,p=2):
	"""Methode de conversion du polynome en polynome sur ZpZ"""
	try:
		for i in xrange(self.degre()+1):
			if type(self[i])==int:
				self[i]=ZpZ(self[i],p)
		return self
	except AttributeError:
		print("Dans toZpZ, erreur d'attribut")

#@controler_temps(5)
def logpoly(P,p=2):  #P idéal dans ZpZ, p modulo
	"""Passage de la forme logarithmique à la forme polynomiale"""
	L=[polynome([ZpZ(1,p)])]		#A cause d'un probleme d'indexation a partir de 0
	try:	
		for d in xrange(p**P.degre()-2):
			X=polynome([ZpZ(0,p) for i in range(d+1)])
			X[d+1]=ZpZ(1,p)
			R=X%P
			toZpZ(R,p) #useless
			L.append(R)
		return L
	except AttributeError:
		print("Dans logpoly, erreur d'attribut")

def base(B,p=2): #conversion en base p de la représentation d'un polynôme, p modulo
	"""Ecriture en base 10 d'un nombre en base p"""
	nbdec=0
	for i in xrange(B.degre(),-1,-1):
		nbdec=nbdec*p+B[i].valeur
	return nbdec

def decomp(n,p=2):
	"""Conversion d'un entier en base 10 dans la base p"""
	decom=polynome([])
	i=0
	while n!=0:
		decom[i]=n%p
		n=n//p
		i+=1
	return decom

def polylog(L,p=2): #passage de la forme polynomiale a la forme logarithmique
	"""Passage de la forme polynomiale à la forme logarithmique"""
	try:
		Inv=[0 for i in range(len(L)+1)]
		Inv[0]=-1   #A voir
		for i in xrange(len(L)):
			Inv[base(L[i],p)]=i  #La représentation en base p d'une addition nous donne ensuite la puissance de alpha
		return Inv
	except:
		print("Dans polylog, erreur")

class corps(object):
	"""Classe servant a initialiser un corps fini de cardinal puissance de p"""

	def __init__(self,ideal,p=2):
		self.p=p
		self.ideal=toZpZ(ideal,p)
		self.LogPoly=logpoly(ideal,p)			#tableau indexé par les puissances de alpha qui renvoie un polynome
		self.PolyLog=polylog(self.LogPoly,p)		#tableau indexé par l'image des polynomes par la fonction base qui renvoie la puissance de alpha correspondante

	def __eq__(self,autre):
		"""Methode d'egalite"""
		try:
			return (self.p==autre.p) & (self.ideal == autre.ideal)
		except AttributeError:
			print("Il faut comparer 2 corps entre eux.")
	
	def __ne__(self,autre):
		"""Methode de difference entre 2 elements"""
		return not(self==autre)

class element(arith):
	"""Classe d element du corps de Galois, nécessite la déclaration d'un corps de reference F constant de la classe corps"""
	
	def __init__(self,valeur,F): 
		"""Methode d'initialisation de l'element du corps F """
		try:
			if type(valeur)!=type(polynome([])):
				raise TypeError("La valeur doit etre un polynome")
			if type(F)!=type(corps(polynome([1,1]))):
				raise TypeError("F doit etre un corps")
			self.valeur=toZpZ(valeur,F.p) % F.ideal	#valeur doit etre un polynome
			self.F=F
		except TypeError as ex:
			print ex
		except AttributeError:
			print("F n'a pas ete correctement initialisé")

	def __repr__(self):
		"""Methode de representation du polynome """
		try:
			return str(base(self.valeur,self.F.p)) + "g"
		except AttributeError:
			print("Dans l'affichage de l'element, erreur")
			return ""

	def __getitem__(self,index):
		"""Permet d'acceder au coefficient de l'élement dans sa forme polynomiale"""
		try:
			return self.valeur[index]
		except IndexError:
			return 0
		except TypeError:
			print("Un index doit etre un entier")

	def __eq__(self,autre):
		"""Methode d'egalite entre elements ou entre un element et un polynome"""
		try:
			if self.F != autre.F:
				raise TypeError("Les corps sont differents")
			return self.valeur == autre.valeur
		except AttributeError:
			return self.valeur == autre
		except TypeError as ex:
			print ex
			return False

	#@controler_temps(0.002)
	def __add__(self,autre):
		"""methode d'addition de 2 elements"""
		try:
			if self.F != autre.F:
				raise TypeError("Les corps sont differents")
			return element((self.valeur + autre.valeur)%self.F.ideal,self.F)
		except AttributeError:
			return element((self.valeur + autre)%self.F.ideal,self.F)
		except TypeError as ex:
			print ex 

	def log(self):
		"""Methode de passage a la forme logarithmique, renvoie une puissance de alpha"""
		try:
			return self.F.PolyLog[base(self.valeur,self.F.p)]
		except AttributeError:
			print("Dans log, erreur d'attribut.")

	#@controler_temps(0.002)
	def __mul__(self,autre):
		"""Methode de multiplication de 2 elements"""
		try:
			if self.F != autre.F:
				raise TypeError("Les corps sont differents")
			if self.log()==-1 or autre.log()==-1:		#c'est a dire si un element est nul
				return element(polynome([]),self.F)
			LogAns= (self.log() + autre.log())%(self.F.p**self.F.ideal.degre() -1)
			return element(self.F.LogPoly[LogAns],self.F)
		except AttributeError:
			return element(autre * self.valeur,self.F)
		except TypeError as ex:
			print ex

	def __pow__(self,indice):
		"""Methode pour les puissances modulaires en mode exporapido"""
		try:
			if type(indice)!=type(0):
				raise TypeError("On ne fait que des puissances entières")
			if self.log()==-1:
				return element(polynome([]),self.F)
			return element(self.F.LogPoly[self.log()*indice % (self.F.p**self.F.ideal.degre()-1)],self.F)
		except AttributeError:
			print("Dans pow, erreur d'attribut")
		except TypeError as ex:
			print(ex)

	def __rdiv__(self,autre):
		"""Methode de passage a l'inverse, en supposant que autre est un entier, ce qui devrait toujours etre le cas"""
		if self.log()==-1:
			raise ZeroDivisionError
		LogAns = (self.F.p**self.F.ideal.degre()-1 - self.log())%(self.F.p**self.F.ideal.degre()-1)
		return autre * element(self.F.LogPoly[LogAns],self.F)

	def __div__(self,autre):
		"""Methode de quotient de 2 elements"""
		if type(self)==type(autre):
			return self * (1/autre)
		else :
			print("erreur de type")
			return element(polynome([]),F)

def PtoGalois(self,F):
	"""Methode de conversion du polynome en polynome sur un corps de Galois"""
	for i in xrange(self.degre()+1):
		if type(self[i])==int:
			self[i]=element(decomp(self[i],F.p),F)
	return self