#!/usr/bin/env python3
import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from Window import Ui_MainWindow
 
class Texty(Ui_MainWindow):
	def __init__(self, window):
		Ui_MainWindow.__init__(self)
		self.setupUi(window)

		self.window = window
		self.curFile = None

		self.window.setWindowTitle("Texty - Untitled")
 
		# self.textBrowser.textChanged.connect(self.onTextChange)

		# http://pyqt.sourceforge.net/Docs/PyQt4/qkeysequence.html#StandardKey-enum
		self.actionNew.triggered.connect(self.onNew)
		self.actionNew.setShortcut(QtGui.QKeySequence.New)

		self.actionOpen.triggered.connect(self.onOpen)
		self.actionOpen.setShortcut(QtGui.QKeySequence.Open)

		self.actionSave.triggered.connect(self.onSave)
		self.actionSave.setShortcut(QtGui.QKeySequence.Save)

		self.actionSave_as.triggered.connect(self.onSave_as)
		self.actionSave_as.setShortcut(QtGui.QKeySequence.SaveAs)
 
	def loadFile(self, path):
		with open(path, "r") as f:
			self.textBrowser.setPlainText(f.read())

	def saveFile(self, path, content):
		with open(path, "w") as f:
			f.write(content)


	def onNew(self):
		self.curFile = None
		self.window.setWindowTitle("Texty - Untitled")
		self.textBrowser.setPlainText("")

	def onOpen(self):
		newPath, _ = QtWidgets.QFileDialog.getOpenFileName(self.window) or None
		if newPath:
			self.curFile = newPath
			self.window.setWindowTitle("Texty - " + "<{}>".format(self.curFile) if self.curFile is not None else "Untitled")
			self.loadFile(self.curFile)


	def onSave(self):
		if self.curFile is None:
			self.onSave_as()
		else:
			self.saveFile(self.curFile, self.textBrowser.toPlainText())

	def onSave_as(self):
		newPath, _ = QtWidgets.QFileDialog.getSaveFileName(self.window) or None
		if newPath:
			self.curFile = newPath
			self.window.setWindowTitle("Texty - " + "<{}>".format(self.curFile) if self.curFile is not None else "Untitled")
			self.saveFile(self.curFile, self.textBrowser.toPlainText())
 
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	win = QtWidgets.QMainWindow()
 
	prog = Texty(win)
 
	win.show()
	sys.exit(app.exec_())