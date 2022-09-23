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
		self.curFile = ""


		self.menuBar = QMenuBar(self)

		self.FileMenu = self.menuBar.addMenu("File")

		self.FileMenu.NewFileAction = self.FileMenu.addAction("New File...")
		self.FileMenu.NewFileAction.triggered.connect(self.CreateFile)

		self.FileMenu.OpenFileAction = self.FileMenu.addAction("Open File...")
		self.FileMenu.OpenFileAction.triggered.connect(self.OpenFile)

		self.FileMenu.addSeparator()

		self.FileMenu.SaveAction = self.FileMenu.addAction("Save")
		self.FileMenu.SaveAction.triggered.connect(self.SaveFile)
		self.FileMenu.SaveAction.setDisabled(True)

		self.FileMenu.SaveAsAction = self.FileMenu.addAction("Save As...")
		self.FileMenu.SaveAsAction.triggered.connect(self.SaveFileAs)

		self.menuBar.setFixedSize(self.width(), self.menuBar.sizeHint().height())


		self.curFileDisplay = QLabel("No File opened", self)
		self.curFileDisplay.setStyleSheet("padding-left: 2px")
		self.curFileDisplay.setFixedSize(self.width(), 25)
		self.curFileDisplay.move(0, self.height()-self.curFileDisplay.sizeHint().height())


		self.TextArea = QPlainTextEdit(self)
		self.TextArea.move(QPoint(0, 0+self.menuBar.height()))
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height()-self.curFileDisplay.height())
		self.TextArea.textChanged.connect(self.CheckSaveBuffer)
	


	def resizeEvent(self, event):
		self.menuBar.setFixedSize(self.width(), self.menuBar.sizeHint().height())
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height()-self.curFileDisplay.height())
		self.curFileDisplay.setFixedSize(self.width(), 25)
		self.curFileDisplay.move(0, self.height()-self.curFileDisplay.sizeHint().height())
		return super(MainWindow, self).resizeEvent(event)
	

	
	@Slot()
	def CreateFile(self):
		f = QFileDialog.getSaveFileName(self, "Create a new file", filter="Text Files (*.txt)")[0]
		if f == "": return
		
		with open(f, "w", encoding="UTF-8") as fl:
			self.textBuffer = ["", True]
			self.curFile = f
			self.curFileDisplay.setText(self.curFile)
	
	@Slot()
	def OpenFile(self):
		f = QFileDialog.getOpenFileName(self, "Open a file", filter="Text Files (*.txt)")[0]
		if f != "":
			with open(f, "r", encoding="UTF-8") as fl:
				content = fl.read()
				self.TextArea.setPlainText(content)
				self.textBuffer = [content, True]
				self.curFile = f
				self.curFileDisplay.setText(self.curFile)
	
	@Slot()
	def CheckSaveBuffer(self):
		if self.textBuffer[1] == False: return
		
		if self.TextArea.toPlainText() != self.textBuffer[0]: self.FileMenu.SaveAction.setDisabled(False)
		elif self.TextArea.toPlainText() == self.textBuffer[0]: self.FileMenu.SaveAction.setDisabled(True)
	
	@Slot()
	def SaveFile(self):
		if self.curFile == "": return

		with open(self.curFile, "w", encoding="UTF-8") as fl:
			content = self.TextArea.toPlainText()
			fl.write(content)
			self.textBuffer[0] = content
			self.FileMenu.SaveAction.setDisabled(True)
	
	@Slot()
	def SaveFileAs(self):
		f = QFileDialog.getSaveFileName(self, "Save File As", filter="Text Files (*.txt)")[0]
		if f == "": return
		
		with open(f, "w", encoding="UTF-8") as fl:
			content = self.TextArea.toPlainText()
			fl.write(content)
			self.textBuffer = [content, True]
			self.curFile = f
			self.curFileDisplay.setText(self.curFile)