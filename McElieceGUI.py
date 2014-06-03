#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial 

This program creates a skeleton of
a classic GUI application with a menubar,
toolbar, statusbar and a central widget. 

author: Jan Bodnar
website: zetcode.com 
last edited: August 2011
"""

import sys
from PySide import QtGui, QtCore
import McEliece
import time

class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()
		
		self.initUI()
		
	def initUI(self):               

		btn_1 = QtGui.QPushButton("Chiffrer")
		btn_1.clicked.connect(self.chiffrer)
		btn_2 = QtGui.QPushButton("Dechiffrer")
		btn_2.clicked.connect(self.dechiffrer)
		btn_3 = QtGui.QPushButton("Creer clefs")
		btn_3.clicked.connect(self.creerClefs)
		btn_4 = QtGui.QPushButton("Quitter")
		btn_4.clicked.connect(self.close)

		self.txt1 = QtGui.QLineEdit("Clef_publique")
		self.txt1.setToolTip("Clef publique permettant le chiffrage")
		self.txt2 = QtGui.QLineEdit("Clef_privee")
		self.txt2.setToolTip("Clef privee permettant le dechiffrage")
		self.txt3 = QtGui.QLineEdit("Fichier_a_traiter")
		self.txt3.setToolTip("Fichier a chiffrer ou a dechiffrer")
		self.txt4 = QtGui.QLineEdit("Fichier_cible")
		self.txt4.setToolTip("Fichier ou sera stocke le resultat")
		"""
		btn_5 = QtGui.QPushButton("Parcourir")
		btn_5.clicked.connect(self.fDialog)
		btn_6 = QtGui.QPushButton("Parcourir")
		btn_6.clicked.connect(self.fDialog)
		btn_7 = QtGui.QPushButton("Parcourir")
		btn_7.clicked.connect(self.fDialog)
		btn_8 = QtGui.QPushButton("Parcourir")
		btn_8.clicked.connect(self.fDialog)"""

		grid = QtGui.QGridLayout()
		grid.addWidget(btn_1,0,0)
		grid.addWidget(btn_2,1,0)
		grid.addWidget(btn_3,2,0)
		grid.addWidget(btn_4,3,0)
		grid.addWidget(self.txt1,0,1)
		grid.addWidget(self.txt2,1,1)
		grid.addWidget(self.txt3,2,1)
		grid.addWidget(self.txt4,3,1)
		"""grid.addWidget(btn_5,0,2)
		grid.addWidget(btn_6,1,2)
		grid.addWidget(btn_7,2,2)
		grid.addWidget(btn_8,3,2)"""

		self.setLayout(grid)
		
		self.setGeometry(300, 300, 350, 250)
		self.setWindowTitle('Mc Eliece')    
		self.show()

	def chiffrer(self):
		pub_key =self.txt1.text()
		f_source = self.txt3.text()
		f_cible = self.txt4.text()
		try:
			#Chargement de la clef et cryptage
			avant = time.time()
			try:
				pub_key = McEliece.clef_publique().load(pub_key)
			except:
				pub_key = McEliece.clef_correcteur().load(pub_key)
			pub_key.chiffrer(f_source,f_cible)
			print 'Chiffrage reussi en  ' + str(time.time() - avant) + 's'
			print
		except IOError:
			print "Echec a l'ouverture de la clef ou du fichier source, veuillez recommencer."
			print

	def dechiffrer(self):
		priv_key =self.txt2.text()
		f_source = self.txt3.text()
		f_cible = self.txt4.text()
		try:
			#Chargement de la clef et decryptage
			avant = time.time()
			try:
				priv_key = McEliece.clef_correcteur().load(priv_key)
			except:
				priv_key = McEliece.clef_privee().load(priv_key)
			priv_key.dechiffrer(f_source,f_cible)
			print 'Dechiffrage reussi en ' + str(time.time() - avant)+ 's'
			print
		except IOError:
			print "Echec a l'ouverture de la clef ou du fichier source, veuillez recommencer."
			print

	def creerClefs(self):
		pub_key = self.txt1.text()
		priv_key = self.txt2.text()
		avant = time.time()
		priv_key = McEliece.clef_privee().new(mod,correction)
		pub_key = McEliece.clef_publique().new(priv_key)
		print 'Clefs generees en ' + str(time.time() - avant)+ 's'

		#Enregistrement des clefs
		priv_key.save(f_priv)
		pub_key.save(f_pub)
		print "Clefs imprimees"		
		
def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()