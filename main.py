#!/usr/bin/env python3
import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
 
class Texty(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QDialog.__init__(self)

		self.window = uic.loadUi("Window.ui")
		self.curFile = None
		self.unsavedChanges = False

		self._setTitle(None)
 
		self.window.textBrowser.textChanged.connect(self._onTextChange)

		# http://pyqt.sourceforge.net/Docs/PyQt4/qkeysequence.html#StandardKey-enum
		self.window.actionNew.triggered.connect(self._onNew)
		self.window.actionNew.setShortcut(QtGui.QKeySequence.New)

		self.window.actionOpen.triggered.connect(self._onOpen)
		self.window.actionOpen.setShortcut(QtGui.QKeySequence.Open)

		self.window.actionSave.triggered.connect(self._onSave)
		self.window.actionSave.setShortcut(QtGui.QKeySequence.Save)

		self.window.actionSaveAs.triggered.connect(self._onSave_as)
		self.window.actionSaveAs.setShortcut(QtGui.QKeySequence.SaveAs)

		self.window.closeEvent = self._closeEvent


	def _closeEvent(self, event):
		if self.unsavedChanges:
			msgBox = QtWidgets.QMessageBox()
			msgBox.setText('There are unsave changes\n')
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
 

	def _setTitle(self, path):
		self.window.setWindowFilePath(path)
		self.window.setWindowTitle("Texty - " + ("<{}>".format(os.path.basename(path)) if path is not None else "Untitled") + "[*]")

	def _setChanged(self, state):
		self.unsavedChanges = state
		self.window.setWindowModified(state)

	def _loadFile(self, path):
		with open(path, "r") as f:
			self.window.textBrowser.setPlainText(f.read())
		self._setChanged(False)

	def _saveFile(self, path, content):
		with open(path, "w") as f:
			f.write(content)
		self._setChanged(False)
		return True

	def _onTextChange(self):
		self._setChanged(True)

	def _onNew(self):
		self.curFile = None
		self.window.textBrowser.setPlainText("")
		self._setChanged(False)
		self._setTitle(None)

	def _onOpen(self):
		newPath, _ = QtWidgets.QFileDialog.getOpenFileName(self.window) or None
		if newPath:
			self.curFile = newPath
			self._setTitle(self.curFile)
			self._loadFile(self.curFile)


	def _onSave(self):
		if self.curFile is None:
			return self._onSave_as()
		else:
			return self._saveFile(self.curFile, self.window.textBrowser.toPlainText())

	def _onSave_as(self):
		newPath, _ = QtWidgets.QFileDialog.getSaveFileName(self.window) or None
		if newPath:
			self.curFile = newPath
			self._setTitle(self.curFile)
			self._saveFile(self.curFile, self.window.textBrowser.toPlainText())
			return True
		return False
 
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
 
	prog = Texty()
 
	prog.window.show()
	sys.exit(app.exec_())
