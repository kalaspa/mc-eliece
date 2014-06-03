#*-coding:Utf-8 -*
#!/usr/bin/python3.2

"""Fichier contenant la classe generale d'objet algébriques contenant + * et eventuellement /"""

class arith(object):
	"""Classe generique contenant les methodes redondantes"""

	def __ne__(self,autre):
		"""Definition de !="""
		return not(self == autre)

	def __radd__(self,autre):
		"""Addition dans l'autre sens"""
		return self + autre

	def __iadd__(self,autre):
		"""Methode de +="""
		return self + autre

	def __rmul__(self,autre):
		"""Multiplication dans l'autre sens"""
		return self * autre

	def __imul__(self,autre):
		"""Methode de *="""
		return self * autre

	def __sub__(self,autre):
		"""Methode de soustraction"""
		return self + (-1 * autre)

	def __rsub__(self,autre):
		"""Methode de soustraction dans l'autre sens"""
		return autre +(-1 * self)

	def __neg__(self):
		"""Methode de passage a l'opposé"""
		return -1 * self