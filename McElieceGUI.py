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
from PySide import QtGui
import McEliece

class Test(QtGui.QMainWindow):
	
	def __init__(self):
		super(Test, self).__init__()
		
		self.initUI()
		
	def initUI(self):               
		
		#textEdit = QtGui.QTextEdit()
		#self.setCentralWidget(textEdit)

		chiffrerAction = QtGui.QAction('Chiffrer', self)
		chiffrerAction.setShortcut('C')
		chiffrerAction.triggered.connect(self.chiffrer)

		dechiffrerAction = QtGui.QAction('Dechiffrer', self)
		dechiffrerAction.setShortcut('D')
		dechiffrerAction.triggered.connect(self.dechiffrer)

		creerClefsAction = QtGui.QAction('Generer des clefs aleatoirement', self)
		creerClefsAction.setShortcut('E')
		creerClefsAction.triggered.connect(self.creerclefs)

		exitAction = QtGui.QAction('Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(self.close)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(chiffrerAction)
		fileMenu.addAction(dechiffrerAction)
		fileMenu.addAction(creerClefsAction)
		fileMenu.addAction(exitAction)

		#toolbar = self.addToolBar('Exit')
		#toolbar.addAction(exitAction)
		
		self.setGeometry(300, 300, 350, 250)
		self.setWindowTitle('Main window')    
		self.show()
		
		
def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = Test()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()