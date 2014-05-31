#*-coding:Utf-8 -*
#!/usr/bin/python3.2

from matrice import *
from galois import *
from poly import *

def derivation(P,mod):
	"""Methode de derivation de polynome dans un corps de Galois"""

	resultat = []
	for i in P.liste[1::]:
		if i != 0:
			resultat.append(i.iter(len(resultat) + 1))
		else:
			resultat.append(0)
	return polynome(resultat)

def berlekamp(P,mod=2):
	"""Algorithme de Berlekamp pour tester l'irreductibilite d'un polynome"""

	#Initialisation des outils
	card = 2**d(mod,0)
	tableau = []
	degre = P.degre()

	#On regarde pour les racines doubles
	D = pgcd(P,derivation(P,mod))
	if D != 1:
		return False

	#On fabrique la matrice de l'application Q -> Q^card modulo P
	calc = polynome([elt(1,mod)])
	X = polynome([0,elt(1,mod)])
	X = X.powmod(card,P)
	for i in xrange(degre):
		tableau += calc.liste + [0 for k in range(degre-1 - calc.degre())]
		calc = calc * X % P

	#On regarde si la matrice qu'on a construite a 1 comme valeur propre
	#On regarde donc si elle meme - Id possede un vecteur non trivial comme vecteur propre
	M = matrice(degre,degre,tableau)
	I =[0 for i in range(degre**2)]
	I[::degre+1] = [elt(1,mod) for i in range(degre)]
	I = matrice(degre,degre ,I)

	rang = len((M-I).gauss(False)["permut"])
	return degre - rang == 1


def P_irreductible(t,mod):
	"""Methode pour generer un polynome irreductible de degre t pour Goppa"""
	
	card = 2**(d(mod,0))
	X = polynome([0,0,elt(1,mod)])
	j=0
	while not(berlekamp(X,mod)):
		X = [elt(1,mod)]
		for i in range(t-1):
			X.append(elt(randint(1,card),mod))
		X.append(elt(1,mod))
		X = polynome(X)
		j+=1
	#print j
	return X


def parite(g,support,mod):
	"""Methode de calcul de la matrice de parite a partir de g et du support"""

	#Initialisation des variables
	dg = g.degre()
	dmod = d(mod,0)
	card = 2**dmod
	M = [0 for i in xrange(dg*card*dmod)]
	L = [0 for i in xrange(dg*card)]

	#Fabrication de la matrice de parite dans galois cf p.99 04cc
	for i in xrange(card): 
		h=1/g(support[i])
		for j in xrange(dg):
			L[i+j*card]=h
			h *= support[i]

	#Transformation de la matrice dans Z/2Z
	for i in xrange(len(L)):
		for j in xrange(dmod):
			M[i% card + ((i//card)*dmod + j)*card] = elt(L[i].valeur>>j & 1,2)
			
	M = matrice(dmod*dg,card,M)
	return M

def generatrice(parite):
	"""Methode pour donner la generatrice en fonction de la matrice de parite passee a reorganise, en supposant nbligne < nbcolonne"""
	
	dic = parite.reorganise()
	M = dic["tasse"]
	rang = len(dic["permut"])
	
	#On decompose M en produit par bloc U,V puis W,Z avec U carre inversible de dim rang
	U = M.bloc(1,1,rang,rang)
	V = M.bloc(1,rang+1,rang,M.nbcolonne)
	#Uinv=U.inverse()
	Uinv = np2me(me2np(U).getI())
	
	#On a K de dim n dans le noyau, on le decompose en X,Y de dim resp rang, nbcolonne - rang
	#La relation fondamentale est X = - U^-1VY
	#On stocke la transposee de G dans tableau
	tableau = []
	
	for i in range(M.nbcolonne - rang):
		Y = matrice(M.nbcolonne - rang,1,[elt(((i+1)//(k+1)) * ((k+1)//(i+1)),2) for k in range(M.nbcolonne-rang)])
		X = Uinv*(V*Y)
		tableau += X.tableau + Y.tableau
		
	#On a construit la matrice G' telle que MG'=0 mais M est la tassee
	G = matrice(M.nbcolonne-rang,M.nbcolonne,tableau).transpose()

	#On utilise que permut donne acces a P tq M=LHC, L chgt de lignes et C chgt de colonne
	#MG'=0 LHCG=0 comme L inversible on a G = CG, on applique les chgts de colonnes de M en ligne pour G'
	for triple in dic["permut"][::-1]:
		G=G.echange(triple[0]+1,triple[2]+1)
	return G

def decodage(generatrice):
	"""Methode pour donner la matrice k,n de decodage telle DG=Ik"""
	
	dic = generatrice.reorganise()
	M = dic["tasse"]
	rang = len(dic["permut"])

	#Normalement si G' est bien concue, elle est de rang k mais autant verifier
	if rang != generatrice.nbcolonne:
		print "Toi tu vas avoir des problemes !"

	#On decompose G' en U,V avec U k,k et V n-k,k bien qu on ne se preoccupe pas de V
	U = M.bloc(1,1,rang,rang)
	#Uinv = U.inverse()
	Uinv = np2me(me2np(U).getI())

	#La matrice D' de decodage est de taille k,n et composée d'abord de Uinv
	tab = Uinv.transpose().tableau
	tab +=[0 for i in range(rang * (generatrice.nbligne - rang))]
	D = matrice(generatrice.nbligne,rang,tab).transpose()

	#On retrouve D en remelangeant le tout
	for triple in dic["permut"][::-1]:
		D=D.echange_colonnes(triple[0]+1,triple[1]+1)
		D =D.echange(triple[0]+1,triple[2]+1)
	return D


def euclide(S,g,mod):
	r = []
	u = []
	v = []
	r.append(g.copie())
	r.append(S.copie())
	u.append(polynome([elt(1,mod)]))
	u.append(polynome([elt(0,mod)]))
	v.append(polynome([elt(0,mod)]))
	v.append(polynome([elt(1,mod)]))
	i = 1
	while r[i].degre() >= g.degre()//2:
		q = r[i-1] // r[i]
		r.append(r[i-1] - q*r[i])
		u.append(u[i-1] - q*u[i])
		v.append(v[i-1] - q*v[i])
		i+=1
	return [v[i],r[i]]
	

def fi(g,support,mod):
	"""Methode retournant la liste des fi necessaires au calcul du syndrome"""

	t = g.degre()
	resultat = []
	for i in support:
		f = polynome([])
		for k in range(t):
			for j in range(t-k):
				f[k] += g.liste[k+j+1] * (i**j)
		f *= elt(1,mod)/ g(i)
		resultat.append(f)
	return resultat

def syndrome(g,mot,support,L_fi,mod):

	#L_fi = fi(g,support,mod)
	synd = polynome([])
	for i in range(mot.nbligne):
		if mot.tableau[i] !=0:
			synd += L_fi[i]
	return synd % g

def corrige(g,mot,support,L_fi,mod):
	"""Methode pour enlever les erreurs d'un message"""

	inter = mot.copie()
	localisateur =euclide(syndrome(g,mot,support,L_fi,mod) ,g,mod)[0]
	for i in xrange(mot.nbligne):
		if localisateur(support[i]) == 0 :
			inter.tableau[i] += elt(1,2)
	return inter