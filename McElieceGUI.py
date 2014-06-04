#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore, QtWebKit
import McEliece
import time

#Constantes a utiliser
correction = 4
mod = 499# 1 + x + x**3 + x**6 + x**7

def tests(a,b):
	pass

class MainWindow(QtGui.QWidget):
	
	def __init__(self):
		super(MainWindow, self).__init__()
		self.initUI()
		
	def initUI(self):

		#Première colonne de boutons
		btn_1 = QtGui.QPushButton("Chiffrer")
		btn_1.clicked.connect(self.chiffrer)
		btn_2 = QtGui.QPushButton("Dechiffrer")
		btn_2.clicked.connect(self.dechiffrer)
		btn_3 = QtGui.QPushButton("Creer clefs")
		btn_3.clicked.connect(self.creerClefs)
		btn_4 = QtGui.QPushButton("Quitter")
		btn_4.clicked.connect(self.close)

		#Seconde colonne de champs
		self.txt1 = QtGui.QLineEdit("Clef_publique")
		self.txt1.setToolTip("Clef publique permettant le chiffrage")
		self.txt2 = QtGui.QLineEdit("Clef_privee")
		self.txt2.setToolTip("Clef privee permettant le dechiffrage")
		self.txt3 = QtGui.QLineEdit("Fichier_a_traiter")
		self.txt3.setToolTip("Fichier a chiffrer ou a dechiffrer")
		self.txt4 = QtGui.QLineEdit("Fichier_cible")
		self.txt4.setToolTip("Fichier ou sera stocke le resultat")

		#Troisième colonne avec les boutons parcourir
		
		btn_5 = QtGui.QPushButton("Parcourir...")
		btn_5.clicked.connect(self.findFichierA)
		btn_6 = QtGui.QPushButton("Parcourir...")
		btn_6.clicked.connect(self.findFichierB)
		"""btn_7 = QtGui.QPushButton("Sources")
		btn_7.clicked.connect(self.sources)
		btn_8 = QtGui.QPushButton("Parcourir")
		btn_8.clicked.connect(self.fDialog)"""


		#Formation du layout en grille
		grid = QtGui.QGridLayout()
		grid.addWidget(btn_1,2,0)
		grid.addWidget(btn_2,2,1)
		grid.addWidget(btn_3,2,2)
		grid.addWidget(btn_4,3,1)
		grid.addWidget(self.txt1,0,0)
		grid.addWidget(self.txt2,1,0)
		grid.addWidget(self.txt3,0,1)
		grid.addWidget(self.txt4,1,1)
		grid.addWidget(btn_5,0,2)
		grid.addWidget(btn_6,1,2)
		"""grid.addWidget(btn_7,3,2)
		grid.addWidget(btn_8,3,2)"""

		self.setLayout(grid)
		
		self.setGeometry(300, 300, 450, 200)
		self.setWindowTitle('Mc Eliece')    
		self.show()

	def chiffrer(self):
		f_pub =self.txt1.text()
		f_source = self.txt3.text()
		f_cible = self.txt4.text()
		try:
			#Chargement de la clef et cryptage
			avant = time.time()
			try:
				pub_key = McEliece.clef_publique().load(f_pub)
			except:
				pub_key = McEliece.clef_correcteur().load(f_pub)
			pub_key.chiffrer(f_source,f_cible)
			print 'Chiffrage reussi en  ' + str(time.time() - avant) + 's'
			print
		except IOError:
			print "Echec a l'ouverture de la clef ou du fichier source, veuillez recommencer."
			print

	def dechiffrer(self):
		f_priv =self.txt2.text()
		f_source = self.txt3.text()
		f_cible = self.txt4.text()
		try:
			#Chargement de la clef et decryptage
			avant = time.time()
			try:
				priv_key = McEliece.clef_correcteur().load(f_priv)
			except:
				priv_key = McEliece.clef_privee().load(f_priv)
			priv_key.dechiffrer(f_source,f_cible)
			print 'Dechiffrage reussi en ' + str(time.time() - avant)+ 's'
			print
		except IOError:
			print "Echec a l'ouverture de la clef ou du fichier source, veuillez recommencer."
			print

	def creerClefs(self):
		f_pub = self.txt1.text()
		f_priv = self.txt2.text()
		avant = time.time()
		priv_key = McEliece.clef_privee().new(mod,correction)
		pub_key = McEliece.clef_publique().new(priv_key)
		print 'Clefs generees en ' + str(time.time() - avant)+ 's'

		#Enregistrement des clefs
		priv_key.save(f_priv)
		pub_key.save(f_pub)
		print "Clefs imprimees"

	def findFichierA(self):
		f_name =  QtGui.QFileDialog.getOpenFileName( self, 'Open file','/home/akamine/Documents/Code/TIPE/mc-eliece' )[0]
		self.txt3.setText( f_name )

	def findFichierB(self):
		f_name =  QtGui.QFileDialog.getSaveFileName( self, 'Save file','/home/akamine/Documents/Code/TIPE/mc-eliece' )[0]
		self.txt4.setText( f_name )


def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()