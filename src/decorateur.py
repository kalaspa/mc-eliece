#*-coding:Utf-8 -*
#!/usr/bin/python3.2
"""Fichier contenant des decorateur, usage pointu et optionnel, surtout pour le fun et les tests"""

import time
 
def controler_temps(nb_secs):
	"""Controle le temps mis par une fonction pour s'exécuter.
	Si le temps d'exécution est supérieur à nb_secs, on affiche une alerte"""
     
	def decorateur(fonction_a_executer):
		"""Notre decorateur. C'est lui qui est appelé directement LORS
		DE LA DEFINITION de notre fonction (fonction_a_executer)"""

		def fonction_modifiee(*parametres_non_nommes, **parametres_nommes):
			"""Fonction renvoyee par notre décorateur. Elle se charge
			de calculer le temps mis par la fonction à s'exécuter"""
			tps_avant = time.time() # Avant d'exécuter la fonction
			valeur_renvoyee = fonction_a_executer(*parametres_non_nommes, **parametres_nommes) # On exécute la fonction
			tps_apres = time.time()
			tps_execution = tps_apres - tps_avant
			if tps_execution >= nb_secs:
				print("La fonction {0} a mis {1} pour s'exécuter".format(fonction_a_executer, tps_execution))
			return valeur_renvoyee
		return fonction_modifiee
	return decorateur

def ignorer(fonction):
	def fonction_modifiee(*parametres_non_nommes, **parametres_nommes):
		pass
	return fonction_modifiee