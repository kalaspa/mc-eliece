# -*-coding:Utf-8 -*
#!/usr/bin/python3.2
"""Module pour la generation de nombres pseudo-aleatoires par l'algorithme Blum Blum Shub (bbs) """
import random

def primdeterm(n):
	"""Test de primalite deterministe """
	if n == 2:
		return True
	else:
		if n%2 == 0:
			return False
		for i in range(3,int(n**0.5+2),2):
			if n%i == 0:
				return False
		return True


def miller(n,a,d,s):
	""" Test de Miller-Rabin a iterer avec la fonction primprob"""
	if pow(a,d,n) == 1:
		return True
	else:
		for r in range(s):
			if pow(a,(2**r) * d,n) == n-1:
				return True
		return False

def primprob(n,k=20):
	"""Test de primalite de Miller-Rabin"""
	s = 0
	d = n-1
	while d % 2 == 0:
		d/=2
		s+=1
	for i in range(k):
		if not miller(n,random.randint(1,n-1),d,s):
			return False
	return True

def isprime(n):
	"""Test de primalite general distribuant un algo deterministe ou probabiliste en fonction de la taille de n """
	if n < 10**8:
		return primdeterm(n)
	else:
		return primprob(n)

def pgcd(a,b):
	"""Algorithme d'Euclide pour le calcul du pgcd """
	while b != 0:
		a,b = b,a%b
	return a

def gen_premier_bbs(bits):
	"""Fabrique un des nombres premiers utilises par l'algorithme """
	b1,b2 = 2 ** (bits -1),2 ** bits -1
	p = random.randint(b1,b2)
	while not(isprime(p)) or p % 4 != 3:
		p = random.randint(b1,b2)
	return p

def gen_graine(M):
	"""Fabrique la graine de l'algorithme """
	graine = random.randint(1,M-1)
	while pgcd(graine,M)!=1:
		graine = random.randint(1,M-1)
	return graine

def bbs(l):
	"""Generateur d'un bit pseudo-aleatorie """
	M,graine = l[0],l[1]
	while True :
		graine = pow(graine,2,M)
		yield graine & 1

def rand(l,sup,min = 0):
	"""Generateur d'un entier aleatoire entre min et sup """
	nombre_de_bits,s = 0,sup-min
	while s != 0:
		s = s >> 1
		nombre_de_bits +=1
	G=bbs(l)
	while True:
		s = '0b'
		for i in range(nombre_de_bits):
			s+=str(G.next())
		if int(s,0) <= sup-min:
			yield int(s,0) + min


def initialise(bits):
	"""Fonction qui initialise tous les generateurs bbs sous forme d'un tableau a 2 entrees"""
	M = gen_premier_bbs(bits) * gen_premier_bbs(bits)
	graine = gen_graine(M)
	return [M,graine]