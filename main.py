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
		self.unsavedChanges = False

		self.window.setWindowTitle("Texty - Untitled[*]")
 
		self.textBrowser.textChanged.connect(self.onTextChange)

		# http://pyqt.sourceforge.net/Docs/PyQt4/qkeysequence.html#StandardKey-enum
		self.actionNew.triggered.connect(self.onNew)
		self.actionNew.setShortcut(QtGui.QKeySequence.New)

		self.actionOpen.triggered.connect(self.onOpen)
		self.actionOpen.setShortcut(QtGui.QKeySequence.Open)

		self.actionSave.triggered.connect(self.onSave)
		self.actionSave.setShortcut(QtGui.QKeySequence.Save)

		self.actionSaveAs.triggered.connect(self.onSave_as)
		self.actionSaveAs.setShortcut(QtGui.QKeySequence.SaveAs)

		self.window.closeEvent = self.closeEvent


	def closeEvent(self, event):
		if self.unsavedChanges:
			msgBox = QtWidgets.QMessageBox()
			msgBox.setText('There are unsave changes\n\n')
			msgBox.setStyleSheet("font-weight: normal;");
			msgBox.addButton(QtWidgets.QPushButton("Save"), QtWidgets.QMessageBox.YesRole)
			msgBox.addButton(QtWidgets.QPushButton("Discard"), QtWidgets.QMessageBox.NoRole)
			msgBox.addButton(QtWidgets.QPushButton("Cancel"), QtWidgets.QMessageBox.RejectRole)
			ret = msgBox.exec_()
			if ret == 0:
				# save
				if self.onSave():
					event.accept()
				else:
					event.ignore()
			elif ret == 2:
				# cancel
				event.ignore()
 

	def setTitle(self, path):
		self.window.setWindowFilePath(path)
		self.window.setWindowTitle("Texty - " + ("<{}>".format(os.path.basename(path)) if path is not None else "Untitled") + "[*]")

	def setChanged(self, state):
		self.unsavedChanges = state
		self.window.setWindowModified(state)

	def loadFile(self, path):
		with open(path, "r") as f:
			self.textBrowser.setPlainText(f.read())
		self.setChanged(False)

	def saveFile(self, path, content):
		with open(path, "w") as f:
			f.write(content)
		self.setChanged(False)
		return True

	def onTextChange(self):
		self.setChanged(True)

	def onNew(self):
		self.curFile = None
		self.textBrowser.setPlainText("")
		self.setChanged(False)
		self.setTitle(None)

	def onOpen(self):
		newPath, _ = QtWidgets.QFileDialog.getOpenFileName(self.window) or None
		if newPath:
			self.curFile = newPath
			self.setTitle(self.curFile)
			self.loadFile(self.curFile)


	def onSave(self):
		if self.curFile is None:
			return self.onSave_as()
		else:
			return self.saveFile(self.curFile, self.textBrowser.toPlainText())

	def onSave_as(self):
		newPath, _ = QtWidgets.QFileDialog.getSaveFileName(self.window) or None
		if newPath:
			self.curFile = newPath
			self.setTitle(self.curFile)
			self.saveFile(self.curFile, self.textBrowser.toPlainText())
			return True
		return False
 
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	win = QtWidgets.QMainWindow()
 
	prog = Texty(win)
 
	win.show()
	sys.exit(app.exec_())