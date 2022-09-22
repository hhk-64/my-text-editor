from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os


class MainWindow(QWidget):

	def __init__(self):
		super().__init__()

		self.setMinimumSize(720, 480)
		self.setWindowTitle("Text Editor")
		self.setWindowIcon(self.style().standardIcon(getattr(QStyle, "SP_FileIcon")))

		self.layout = QHBoxLayout()

		self.textBuffer = ["", False]


		self.menuBar = QMenuBar(self)

		self.FileMenu = self.menuBar.addMenu("File")
		self.FileMenu.NewFileAction = self.FileMenu.addAction("New File...")
		self.FileMenu.OpenFileAction = self.FileMenu.addAction("Open File...")
		self.FileMenu.addSeparator()

		self.FileMenu.SaveAction = self.FileMenu.addAction("Save")
		self.FileMenu.SaveAction.setDisabled(True)

		self.menuBar.setFixedSize(self.width(), self.menuBar.sizeHint().height())


		self.TextArea = QPlainTextEdit(self)
		self.TextArea.move(QPoint(0, 0+self.menuBar.height()))
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height())
		self.TextArea.textChanged.connect(self.CheckSaveBuffer)


		self.FileMenu.NewFileAction.triggered.connect(self.CreateFile)
		self.FileMenu.OpenFileAction.triggered.connect(self.OpenFile)
	


	def resizeEvent(self, event):
		self.menuBar.setFixedSize(self.width(), self.menuBar.sizeHint().height())
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height())
		return super(MainWindow, self).resizeEvent(event)
	
	def textChanged(self):
		if self.TextArea.toPlainText() != self.textBuffer: self.FileMenu.SaveAction.setDisabled(False)
		elif self.TextArea.toPlainText() == self.textBuffer: self.FileMenu.SaveAction.setDisabled(True)
	

	@Slot()
	def CreateFile(self):
		f = QFileDialog.getSaveFileName(self, "Create a new file", filter="Text Files (*.txt)")[0]
		if f != "":
			with open(f, "w", encoding="UTF-8") as fl:
				pass
	
	@Slot()
	def OpenFile(self):
		f = QFileDialog.getOpenFileName(self, "Open a file", filter="Text Files (*.txt)")[0]
		if f != "":
			with open(f, "r", encoding="UTF-8") as fl:
				content = fl.read()
				self.TextArea.setPlainText(content)
				self.TextArea.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
				self.textBuffer = content, True
	
	@Slot()
	def CheckSaveBuffer(self):
		if self.textBuffer[1] == False: return
		
		if self.TextArea.toPlainText() != self.textBuffer: self.FileMenu.SaveAction.setDisabled(False)
		elif self.TextArea.toPlainText() == self.textBuffer: self.FileMenu.SaveAction.setDisabled(True)