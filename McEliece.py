#*-coding:Utf-8 -*
#!/usr/bin/python3.2
"""Corps du programme a executer, le main quoi
On se contentera pour l'instant d'un programme en console"""

#Tailles suggerees par McEliece : n = 1024, k = 524, t = 50

from Classes.clef import *
from time import time

#Constantes a utiliser
correction = 4
mod = 499# 1 + x + x**3 + x**6 + x**7

def  crypt():
	"""Fonction correspondant au choix a : cryptage"""

	f_source = raw_input('Quel est le message a crypter ? ')
	pub_key = raw_input('Quelle clef voulez vous utiliser ? ')
	f_cible = raw_input('Quelle est le fichier ou je dois ecrire le resultat ? ')

	try:
		#Chargement de la clef et cryptage
		avant = time()
		pub_key = clef().load(pub_key)
		pub_key.chiffrer(f_source,f_cible)
		print 'Chiffrage reussi en  ' + str(time() - avant) + 's'
		print
	except IOError:
		print "Echec a l'ouverture de la clef ou du fichier source, veuiller recommencer."
		print

def decrypt():
	"""Fonction correspondant au choix b : decrypter"""

	f_source = raw_input('Quel est le message a decrypter ? ')
	priv_key = raw_input('Quelle clef voulez vous utiliser ? ')
	f_cible = raw_input('Quelle est le fichier ou je dois ecrire le resultat ? ')

	try:
		#Chargement de la clef et decryptage
		avant = time()
		priv_key = clef().load(priv_key)
		priv_key.dechiffrer(f_source,f_cible)
		print 'Dechiffrage reussi en ' + str(time() - avant)+ 's'
		print
	except IOError:
		print "Echec a l'ouverture de la clef ou du fichier source, veuiller recommencer."
		print

def new_keys():
	"""Fonction qui construit une nouvelle paire de clef"""
	f_pub = raw_input("Ou souhaitez vous enregistrer votre clef publique ? ")
	f_priv = raw_input("Ou souhaitez vous enregistrer votre clef privee ? ")

	avant = time()
	priv_key = clef_privee().new(mod,correction)
	pub_key = clef_publique().new(priv_key)
	print 'Clefs generees en ' + str(time() - avant)+ 's'

	#Enregistrement des clefs
	priv_key.save(f_priv)
	pub_key.save(f_pub)
	print "Clefs imprimees"

def new_key():
	"""Fonction qui batit la clef d'un simple code correcteur"""
	f_cor = raw_input("Ou souhaitez vous enregistrer votre clef ? ")

	avant = time()
	cor_key = clef_correcteur().new(mod,correction)
	print 'Clef generee en ' + str(time() - avant)+ 's'

	#Enregistrement des clefs
	cor_key.save(f_cor)
	print "Clefs imprimees"

print "*--------------------*"
print "| TIPE sur Mc Eliece |"
print "*--------------------*"
print
print 'Avertissement :'
print "Faites attention aux fichiers que vous citez"
print "Aucune protection ne garantit leur integrite dans ce programme"
print

possible = {'a' : crypt, 'b':decrypt, 'c' : new_keys, 'd' : new_key}

choix = ''
while choix != 'q':
	print "a : Crypter"
	print "b : Decrypter"
	print "c : Nouvelle paire de clefs, pour le cryptage"
	print "d : Nouvelle clef juste pour créer un code correcteur"
	print 'q : Quitter'
	choix = raw_input("Que choisissez vous ? ").lower()

	if choix in possible:
		possible[choix]()